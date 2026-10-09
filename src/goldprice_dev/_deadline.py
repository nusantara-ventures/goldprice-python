"""Per-attempt synchronous I/O deadlines, without threads or event loops."""

from collections.abc import Callable, Iterable
from contextvars import ContextVar
from ssl import SSLContext
from typing import Protocol, cast

import httpx

RESPONSE_STARTED = "goldprice_dev.response_started"
SocketOption = tuple[int, int, int | bytes] | tuple[int, int, None, int]


class Deadline:
    def __init__(self, timeout: float, clock: Callable[[], float]) -> None:
        self.clock = clock
        self.expires = clock() + timeout

    def remaining(self) -> float:
        return max(0.0, self.expires - self.clock())


active_deadline: ContextVar[Deadline | None] = ContextVar(
    "goldprice_dev_deadline", default=None
)


def io_timeout(timeout: float | None) -> float | None:
    deadline = active_deadline.get()
    if deadline is None:
        return timeout
    remaining = deadline.remaining()
    if remaining <= 0:
        raise httpx.ReadTimeout("Attempt deadline exceeded")
    return remaining if timeout is None else min(timeout, remaining)


class NetworkStream(Protocol):
    def read(self, max_bytes: int, timeout: float | None = None) -> bytes: ...
    def write(self, buffer: bytes, timeout: float | None = None) -> None: ...
    def close(self) -> None: ...
    def start_tls(
        self,
        ssl_context: SSLContext,
        server_hostname: str | None = None,
        timeout: float | None = None,
    ) -> "NetworkStream": ...
    def get_extra_info(self, info: str) -> object: ...


class NetworkBackend(Protocol):
    def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        local_address: str | None = None,
        socket_options: Iterable[SocketOption] | None = None,
    ) -> NetworkStream: ...
    def connect_unix_socket(
        self,
        path: str,
        timeout: float | None = None,
        socket_options: Iterable[SocketOption] | None = None,
    ) -> NetworkStream: ...
    def sleep(self, seconds: float) -> None: ...


class _Stream:
    def __init__(self, inner: NetworkStream) -> None:
        self.inner = inner

    def read(self, max_bytes: int, timeout: float | None = None) -> bytes:
        return self.inner.read(max_bytes, timeout=io_timeout(timeout))

    def write(self, buffer: bytes, timeout: float | None = None) -> None:
        self.inner.write(buffer, timeout=io_timeout(timeout))

    def close(self) -> None:
        self.inner.close()

    def start_tls(
        self,
        ssl_context: SSLContext,
        server_hostname: str | None = None,
        timeout: float | None = None,
    ) -> "_Stream":
        return _Stream(
            self.inner.start_tls(
                ssl_context,
                server_hostname=server_hostname,
                timeout=io_timeout(timeout),
            )
        )

    def get_extra_info(self, info: str) -> object:
        return self.inner.get_extra_info(info)


class _Backend:
    def __init__(self, inner: NetworkBackend) -> None:
        self.inner = inner

    def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        local_address: str | None = None,
        socket_options: Iterable[SocketOption] | None = None,
    ) -> NetworkStream:
        return _Stream(
            self.inner.connect_tcp(
                host,
                port,
                timeout=io_timeout(timeout),
                local_address=local_address,
                socket_options=socket_options,
            )
        )

    def connect_unix_socket(
        self,
        path: str,
        timeout: float | None = None,
        socket_options: Iterable[SocketOption] | None = None,
    ) -> NetworkStream:
        return _Stream(
            self.inner.connect_unix_socket(
                path, timeout=io_timeout(timeout), socket_options=socket_options
            )
        )

    def sleep(self, seconds: float) -> None:
        self.inner.sleep(seconds)


class _Pool(Protocol):
    _network_backend: NetworkBackend


class _ClientTransports(Protocol):
    _transport: httpx.BaseTransport
    _mounts: dict[object, httpx.BaseTransport | None]


def install_deadlines(client: httpx.Client) -> None:
    """Adapt native pools, including environment and explicit proxy pools.

    This is the sole boundary using transport internals. The underlying HTTP codec
    caches the body timeout, so mutating the request timeout between chunks alone
    does not bound slow responses. Native-codec tests verify this adapter against
    the locked dependency. Injected transports can read request timeout extensions.
    """
    transports = cast(_ClientTransports, client)
    for transport in (transports._transport, *transports._mounts.values()):
        if isinstance(transport, httpx.HTTPTransport):
            pool = cast(_Pool, transport._pool)
            if not isinstance(pool._network_backend, _Backend):
                pool._network_backend = _Backend(pool._network_backend)


def read_response(
    response: httpx.Response, request: httpx.Request, deadline: Deadline
) -> httpx.Response:
    if response.is_stream_consumed:
        return response
    timeouts = cast(dict[str, float | None], request.extensions["timeout"])
    chunks = []
    for chunk in response.iter_raw():
        chunks.append(chunk)
        # Do not raise after a received chunk: it may be the last one. A next
        # network read is where expiry becomes a transport failure.
        timeouts["read"] = deadline.remaining()
    return httpx.Response(
        response.status_code,
        headers=response.headers,
        content=b"".join(chunks),
        request=request,
    )
