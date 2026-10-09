"""Request encoding and the shared retry policy for both HTTP clients."""

import asyncio
import os
import time
from collections.abc import Awaitable, Callable, Mapping
from decimal import Decimal, InvalidOperation
from typing import TypeVar
from urllib.parse import quote

import httpx

from ._deadline import (
    RESPONSE_STARTED,
    Deadline,
    active_deadline,
    install_deadlines,
    read_response,
)
from ._decode import read_json, read_object
from ._meta import ResponseMeta
from ._version import __version__
from .errors import (
    ApiError,
    BadRequest,
    CursorExpired,
    DecodeError,
    NotFound,
    RateLimited,
    ServiceUnavailable,
    TransportError,
    Unauthorized,
)

T = TypeVar("T")
Query = list[tuple[str, str]]


class Unset:
    """An omitted body field, distinct from an explicitly supplied null."""

    __slots__ = ()


UNSET = Unset()


def encode_path(template: str, values: Mapping[str, str | int]) -> str:
    for name, value in values.items():
        encoded = quote(str(value), safe="")
        if encoded in {".", ".."}:
            raise ValueError("Path parameters must not be dot-only segments")
        template = template.replace("{" + name + "}", encoded)
    return template


def encode_query(
    name: str, value: object, wire: str, *, required: bool, decimal: bool
) -> Query:
    if decimal and value is not None:
        if not isinstance(value, (str, Decimal)):
            raise TypeError(f"{name} must be Decimal or str")
        value = format(value, "f") if isinstance(value, Decimal) else value
    if value is not None and wire in {"comma_join", "repeat"}:
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            raise TypeError(f"{name} must be a list of strings")
        if any(not v or "," in v for v in value):
            raise ValueError(f"{name} items must be nonempty and contain no commas")
    if value is None or (value == "" and name != "cursor") or value == []:
        if required:
            raise ValueError(f"missing query parameter: {name}")
        return []
    if isinstance(value, list):
        items = [str(v) for v in value]
        return (
            [(name, ",".join(items))]
            if wire == "comma_join"
            else [(name, v) for v in items]
        )
    return [(name, str(value).lower() if isinstance(value, bool) else str(value))]


def encode_body(fields: Mapping[str, object]) -> dict[str, object]:
    return {key: value for key, value in fields.items() if not isinstance(value, Unset)}


class Settings:
    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        timeout: float,
        max_retries: int,
        max_retry_wait: float,
        extra_headers: Mapping[str, str] | None,
        random_fraction: Callable[[], float],
        clock: Callable[[], float],
        spec_sha: str,
        proxy: str | None = None,
    ) -> None:
        key = api_key if api_key is not None else os.environ.get("GOLDPRICE_API_KEY")
        if not key:
            raise ValueError("GOLDPRICE_API_KEY is required")
        if timeout <= 0 or max_retries < 0 or max_retry_wait < 0:
            raise ValueError(
                "timeout must be positive; retry settings must be nonnegative"
            )
        self.base_url = (
            base_url
            if base_url is not None
            else os.environ.get("GOLDPRICE_BASE_URL", "https://api.goldprice.dev")
        ).rstrip("/")
        self.proxy = proxy
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_retry_wait = max_retry_wait
        self.random_fraction = random_fraction
        self.clock = clock
        self.headers = {
            "accept": "application/json, application/problem+json",
            "user-agent": f"goldprice-dev-python/{__version__} (spec {spec_sha[:8]})",
            **{
                k.lower(): v
                for k, v in (extra_headers or {}).items()
                if k.lower() != "authorization"
            },
            "authorization": "Bearer " + key,
        }

    def __repr__(self) -> str:
        return f"{type(self).__name__}(api_key=<redacted>)"

    def retry_wait(
        self, method: str, attempt: int, error: ApiError | TransportError
    ) -> float | None:
        if attempt >= self.max_retries:
            return None
        retry_after = None
        if isinstance(error, ApiError):
            retryable = (error.status == 429 and error.code in RETRYABLE_LIMITS) or (
                error.status == 503 and method == "GET"
            )
            retry_after = error.retry_after
        else:
            retryable = method == "GET" and not error.response_received
        if not retryable:
            return None
        if retry_after is not None:
            return retry_after if retry_after <= self.max_retry_wait else None
        return 0.5 * 2.0**attempt * self.random_fraction()


# Short-window limits are retried; quota and unknown 429 codes are not.
RETRYABLE_LIMITS = frozenset({"rate_limit_exceeded", "rate_limited"})


def api_error(response: httpx.Response) -> ApiError:
    try:
        data = read_object(read_json(response.content))
    except (ValueError, TypeError, UnicodeError):
        data = {}

    def string(name: str, default: str = "") -> str:
        value = data.get(name)
        return value if isinstance(value, str) else default

    # Problem documents carry `code`; the shared core also reads the
    # `{"error": code}` and `{"code", "message"}` envelopes other APIs use.
    code = string("code") or string("error") or "unknown"
    error_type = (
        CursorExpired
        if code == "cursor_expired"
        else {
            400: BadRequest,
            401: Unauthorized,
            404: NotFound,
            429: RateLimited,
            503: ServiceUnavailable,
        }.get(response.status_code, ApiError)
    )
    retry_after: int | None
    try:
        retry_after = int(response.headers["retry-after"])
        if retry_after < 0:
            retry_after = None
    except (KeyError, ValueError):
        retry_after = None
    return error_type(
        status=response.status_code,
        code=code,
        title=string("title"),
        detail=string("detail") or string("message"),
        request_id=response.headers.get("x-request-id") or string("request_id") or None,
        instance=string("instance") or None,
        retry_after=retry_after,
        raw_body=response.content,
    )


def decode_response(
    response: httpx.Response, decoder: Callable[[object, ResponseMeta | None, bytes], T]
) -> T:
    try:
        return decoder(
            read_json(response.content),
            ResponseMeta.from_headers(response.headers),
            response.content,
        )
    except (ValueError, KeyError, TypeError, InvalidOperation, UnicodeError):
        raise DecodeError(response.content) from None


class SyncTransport:
    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.settings = settings
        self.base_url = settings.base_url
        self.sleep = sleep
        self.http = httpx.Client(
            transport=transport,
            proxy=settings.proxy,
            follow_redirects=False,
            trust_env=True,
            timeout=httpx.Timeout(
                self.settings.timeout, connect=min(10, self.settings.timeout)
            ),
        )

        install_deadlines(self.http)

    def request(
        self,
        method: str,
        path: str,
        query: Query,
        body: dict[str, object] | None,
        decoder: Callable[[object, ResponseMeta | None, bytes], T],
    ) -> T:
        for attempt in range(self.settings.max_retries + 1):
            failure: ApiError | TransportError
            request = self.http.build_request(
                method,
                self.base_url + path,
                params=tuple(query),
                json=body,
                headers=self.settings.headers,
            )
            deadline = Deadline(self.settings.timeout, self.settings.clock)
            token = active_deadline.set(deadline)
            try:
                response = self.http.send(request, stream=True)
                request.extensions[RESPONSE_STARTED] = True
                try:
                    received = read_response(response, request, deadline)
                finally:
                    response.close()
                response = received
            except httpx.TransportError as cause:
                failure = TransportError(
                    cause,
                    response_received=bool(request.extensions.get(RESPONSE_STARTED)),
                )
            else:
                if response.is_success:
                    return decode_response(response, decoder)
                failure = api_error(response)
            finally:
                active_deadline.reset(token)
            wait = self.settings.retry_wait(method, attempt, failure)
            if wait is None:
                raise failure from None
            self.sleep(wait)
        raise AssertionError("unreachable")


class AsyncTransport:
    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        self.settings = settings
        self.base_url = settings.base_url
        self.sleep = sleep
        self.http = httpx.AsyncClient(
            transport=transport,
            proxy=settings.proxy,
            follow_redirects=False,
            trust_env=True,
            timeout=httpx.Timeout(
                self.settings.timeout, connect=min(10, self.settings.timeout)
            ),
        )

    async def request(
        self,
        method: str,
        path: str,
        query: Query,
        body: dict[str, object] | None,
        decoder: Callable[[object, ResponseMeta | None, bytes], T],
    ) -> T:
        for attempt in range(self.settings.max_retries + 1):
            failure: ApiError | TransportError
            request = self.http.build_request(
                method,
                self.base_url + path,
                params=tuple(query),
                json=body,
                headers=self.settings.headers,
            )
            try:
                response = await asyncio.wait_for(
                    self._attempt(request), self.settings.timeout
                )
            except (httpx.TransportError, asyncio.TimeoutError) as cause:
                failure = TransportError(
                    cause,
                    response_received=bool(request.extensions.get(RESPONSE_STARTED)),
                )
            else:
                if response.is_success:
                    return decode_response(response, decoder)
                failure = api_error(response)
            wait = self.settings.retry_wait(method, attempt, failure)
            if wait is None:
                raise failure from None
            await self.sleep(wait)
        raise AssertionError("unreachable")

    async def _attempt(self, request: httpx.Request) -> httpx.Response:
        response = await self.http.send(request, stream=True)
        request.extensions[RESPONSE_STARTED] = True
        try:
            await response.aread()
            return response
        finally:
            await response.aclose()
