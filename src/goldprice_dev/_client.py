"""Connection-owning synchronous and asynchronous clients."""

import asyncio
import random
import time
from collections.abc import Awaitable, Callable, Mapping
from types import TracebackType
from typing import TypeVar

import httpx

from ._generated.operations import (
    LIVE_SPEC_SHA,
    AsyncStableOperations,
    StableOperations,
)
from ._transport import AsyncTransport, Settings, SyncTransport

SyncClient = TypeVar("SyncClient", bound="Goldprice")
AsyncClient = TypeVar("AsyncClient", bound="AsyncGoldprice")


class Goldprice(StableOperations):
    """Share one client across threads and close it when finished."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        proxy: str | None = None,
        timeout: float = 30,
        max_retries: int = 2,
        max_retry_wait: float = 30,
        extra_headers: Mapping[str, str] | None = None,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        random_fraction: Callable[[], float] = random.random,
    ) -> None:
        settings = Settings(
            api_key=api_key,
            base_url=base_url,
            proxy=proxy,
            timeout=timeout,
            max_retries=max_retries,
            max_retry_wait=max_retry_wait,
            extra_headers=extra_headers,
            clock=clock,
            random_fraction=random_fraction,
            spec_sha=LIVE_SPEC_SHA,
        )
        self._transport = SyncTransport(settings, transport=transport, sleep=sleep)
        super().__init__(self._transport)

    def __repr__(self) -> str:
        return "Goldprice(api_key=<redacted>)"

    def close(self) -> None:
        self._transport.http.close()

    def __enter__(self: SyncClient) -> SyncClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


class AsyncGoldprice(AsyncStableOperations):
    """Use one client per event loop and close it with async with."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        proxy: str | None = None,
        timeout: float = 30,
        max_retries: int = 2,
        max_retry_wait: float = 30,
        extra_headers: Mapping[str, str] | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        clock: Callable[[], float] = time.monotonic,
        random_fraction: Callable[[], float] = random.random,
    ) -> None:
        settings = Settings(
            api_key=api_key,
            base_url=base_url,
            proxy=proxy,
            timeout=timeout,
            max_retries=max_retries,
            max_retry_wait=max_retry_wait,
            extra_headers=extra_headers,
            clock=clock,
            random_fraction=random_fraction,
            spec_sha=LIVE_SPEC_SHA,
        )
        self._transport = AsyncTransport(settings, transport=transport, sleep=sleep)
        super().__init__(self._transport)

    def __repr__(self) -> str:
        return "AsyncGoldprice(api_key=<redacted>)"

    async def aclose(self) -> None:
        await self._transport.http.aclose()

    async def __aenter__(self: AsyncClient) -> AsyncClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()
