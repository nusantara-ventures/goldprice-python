# Generated from spec/goldprice/live/openapi.json sha256 7483e916b388f8b1a6b5c5689b0180ad8914fec2e5f28a0ffdaf041075039f65. Do not edit.
from __future__ import annotations

import builtins
from collections.abc import AsyncIterator, Iterator
from decimal import Decimal

from .._pagination import iterate, iterate_async
from .._transport import (
    AsyncTransport,
    Query,
    SyncTransport,
    encode_path,
    encode_query,
)
from . import models

LIVE_SPEC_SHA = "7483e916b388f8b1a6b5c5689b0180ad8914fec2e5f28a0ffdaf041075039f65"


class Account:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def usage(self) -> models.UsagePublic:
        """Authed key's day + month call counters

        Stability: stable.

        Returns:
            UsagePublic: Decoded response with header metadata.
        """
        _query: Query = []
        return self._transport.request(
            "GET",
            encode_path("/v1/account/usage", {}),
            _query,
            None,
            models.decode_UsagePublic,
        )


class Bars:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        interval: str | None = None,
        limit: int | None = None,
        symbol: str,
        to: str,
    ) -> models.BarsResponse:
        """OHLCV bar history — cursor-paginated, real data, is_closed label

        Paginated OHLCV bar history from the canonical price_bars store.

        Results are ordered DESC by bar_start (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with bars: [].

        Tier depth gates:
        - Free:  30 days
        - Basic: 1 year
        - Pro+:  full history (daily back to 1996 for XAU/USD; intraday from 2006)

        Intraday intervals (1m, 5m, 15m, 30m, 1h, 2h, 4h) require Pro+; Plus
        gets 1h only.

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns bars older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            interval: Optional query parameter. Bar interval. One of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d.
            limit: Optional query parameter. Max bars per page (1-10000). Default 100.
            symbol: Required query parameter. Symbol in slash or dash form. E.g. \"XAU/USD\", \"XAU-USD-SPOT\", \"GLD\".
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            BarsResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("cursor", cursor, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(
            encode_query("interval", interval, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("limit", limit, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        return self._transport.request(
            "GET", encode_path("/v1/bars", {}), _query, None, models.decode_BarsResponse
        )

    def list_iter(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        interval: str | None = None,
        limit: int | None = None,
        symbol: str,
        to: str,
    ) -> Iterator[models.Bar]:
        """OHLCV bar history — cursor-paginated, real data, is_closed label

        Paginated OHLCV bar history from the canonical price_bars store.

        Results are ordered DESC by bar_start (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with bars: [].

        Tier depth gates:
        - Free:  30 days
        - Basic: 1 year
        - Pro+:  full history (daily back to 1996 for XAU/USD; intraday from 2006)

        Intraday intervals (1m, 5m, 15m, 30m, 1h, 2h, 4h) require Pro+; Plus
        gets 1h only.

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns bars older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            interval: Optional query parameter. Bar interval. One of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d.
            limit: Optional query parameter. Max bars per page (1-10000). Default 100.
            symbol: Required query parameter. Symbol in slash or dash form. E.g. \"XAU/USD\", \"XAU-USD-SPOT\", \"GLD\".
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            Iterator[Bar]: Items yielded lazily across pages.
        """

        def page(
            next_cursor: str | None,
        ) -> tuple[builtins.list[models.Bar], str | None]:
            result = self.list(
                cursor=next_cursor,
                from_=from_,
                interval=interval,
                limit=limit,
                symbol=symbol,
                to=to,
            )
            return [item for item in result.bars], result.next_cursor

        return iterate(page, cursor)

    def latest(
        self, *, interval: str | None = None, symbol: str
    ) -> models.LatestBarResponse:
        """Latest bar for a symbol+interval — the most-recent settled or forming bar

        Return the single most-recent bar for a symbol+interval.

        Ordered by bar_start DESC, returns the first row. Provisional (forming)
        bars are returned with is_closed=False. Empty → 200 with bar: null, never
        404. No tier gate on this endpoint (latest bar is the lightest read;
        depth-gating only applies to ranges).

        Stability: stable.

        Args:
            interval: Optional query parameter. Bar interval. One of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d.
            symbol: Required query parameter. Symbol in slash or dash form. E.g. \"XAU/USD\", \"GLD\".

        Returns:
            LatestBarResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("interval", interval, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=True, decimal=False)
        )
        return self._transport.request(
            "GET",
            encode_path("/v1/bars/latest", {}),
            _query,
            None,
            models.decode_LatestBarResponse,
        )


class Convert:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def carat(self, *, currency: str | None = None) -> models.CaratResponse:
        """Per-gram gold price by karat purity

        Per-gram XAU price for karats 24 / 22 / 21 / 20 / 18 / 16 / 14 / 10.

        Logic: per_gram_24k = spot_xau_usd_per_oz / GRAMS_PER_TROY_OUNCE * fx_rate;
        per_gram_Nk = per_gram_24k * N/24.

        Historical `date` support is not implemented; omit the param or use
        /v1/prices/history + do the math client-side.

        Stability: stable.

        Args:
            currency: Optional query parameter. Quote currency (default USD).

        Returns:
            CaratResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("currency", currency, "single", required=False, decimal=False)
        )
        return self._transport.request(
            "GET",
            encode_path("/v1/carat", {}),
            _query,
            None,
            models.decode_CaratResponse,
        )

    def amount(
        self,
        *,
        amount: Decimal | str | None = None,
        from_: str,
        to: str,
        unit: str | None = None,
    ) -> models.ConvertResponse:
        """Convert between metals, currencies, and units

        Convert an amount between metals, currencies, and units.

        - metal → currency: spot price in that currency via FX cross through USD
        - currency → metal: inverse of the above
        - metal → metal: ratio of USD spot prices
        - currency → currency: FX cross through USD (live rate first, then the
          last stored rate only up to three days old)

        Two-leg source skew: currency → currency conversions resolve EACH leg
        independently through the fresh-first/last-stored chain, so the two
        legs can have different ages (e.g. a fresh EUR rate crossed with an
        older stored THB rate). The response `timestamp` reflects
        the `to` leg only — the `from` leg's timestamp is discarded — so it
        can understate (or overstate) the age of the other half of the cross.
        Both legs share the USD anchor, so cross drift is bounded by the
        staleness of the older leg — never compounded.

        The `unit` param applies to the metal side only (oz / gram / kg).
        Historical conversion via `date` is not supported; use /v1/bars +
        /v1/prices/history for historical spot data.

        Stability: stable.

        Args:
            amount: Optional query parameter. Amount to convert (default 1).
            from_: Required query parameter. Source symbol: XAU, XAG, USD, EUR, …
            to: Required query parameter. Target symbol: USD, EUR, XAU, …
            unit: Optional query parameter. Unit for the metal side: oz | gram | kg (default oz).

        Returns:
            ConvertResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("amount", amount, "single", required=False, decimal=True)
        )
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        _query.extend(
            encode_query("unit", unit, "single", required=False, decimal=False)
        )
        return self._transport.request(
            "GET",
            encode_path("/v1/convert", {}),
            _query,
            None,
            models.decode_ConvertResponse,
        )


class Prices:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def history(
        self,
        *,
        from_: str,
        interval: str | None = None,
        limit: int | None = None,
        symbol: str,
        to: str,
    ) -> models.HistoryResponse:
        """[DEPRECATED — use /v1/bars] Aggregated close history for a symbol — interval ∈ {1d, 1h}.

        Dispatch to the per-interval handler. The handler is the Module
        Interface; per-interval helpers are Deep Modules hiding the
        interval-specific policy + storage shape.

        DEPRECATED in favour of /v1/bars (C4). This endpoint retains the
        legacy close-only series[] wire shape for backward compatibility.
        Deprecation + Sunset + Link headers are injected on every 200 response
        (and on 403 plan_gated, where the caller may need to upgrade before
        migrating). The sunset DATE is founder-controlled (see config
        prices_history_sunset_date) — NOT hardcoded here.

        Stability: stable.

        Args:
            from_: Required query parameter.
            interval: Optional query parameter.
            limit: Optional query parameter.
            symbol: Required query parameter.
            to: Required query parameter.

        Returns:
            HistoryResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(
            encode_query("interval", interval, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("limit", limit, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        return self._transport.request(
            "GET",
            encode_path("/v1/prices/history", {}),
            _query,
            None,
            models.decode_HistoryResponse,
        )

    def list(
        self, *, include: str | None = None, symbol: str | None = None
    ) -> models.SpotListResponse:
        """Latest aggregated price per (symbol, currency, contract_type)

        Stability: stable.

        Args:
            include: Optional query parameter. Comma-separated field groups to include in the response. Tokens: sources, karat, stats, all. Unknown tokens are ignored. Omit for the lean default. The stats group requires authentication.
            symbol: Optional query parameter.

        Returns:
            SpotListResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("include", include, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=False, decimal=False)
        )
        return self._transport.request(
            "GET",
            encode_path("/v1/prices", {}),
            _query,
            None,
            models.decode_SpotListResponse,
        )

    def spot(self, symbol: str, *, include: str | None = None) -> models.SpotResponse:
        """Latest spot price for one symbol — flat shape, no envelope (parity convenience)

        Stability: stable.

        Args:
            symbol: Required path parameter.
            include: Optional query parameter. Comma-separated field groups to include in the response. Tokens: sources, karat, stats, all. Unknown tokens are ignored. Omit for the lean default. The stats group requires authentication.

        Returns:
            SpotResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("include", include, "single", required=False, decimal=False)
        )
        return self._transport.request(
            "GET",
            encode_path("/v1/spot/{symbol}", {"symbol": symbol}),
            _query,
            None,
            models.decode_SpotResponse,
        )


class Ratios:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def latest(self, *, pair: str) -> models.LatestRatioResponse:
        """Latest ratio point for a pair — the most-recent shared-date ratio (Pro+)

        Return the single most-recent shared-date ratio point for a pair.

        Returns 200 with point: null when no shared date exists (e.g. before
        either leg is backfilled) — never 404 on empty (mirrors /v1/bars/latest).

        Stability: stable.

        Args:
            pair: Required query parameter. Pair slug (e.g. 'gold-silver', 'gold-platinum', 'gld-xau').

        Returns:
            LatestRatioResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("pair", pair, "single", required=True, decimal=False)
        )
        return self._transport.request(
            "GET",
            encode_path("/v1/ratios/latest", {}),
            _query,
            None,
            models.decode_LatestRatioResponse,
        )

    def list(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        limit: int | None = None,
        pair: str,
        to: str,
    ) -> models.RatiosResponse:
        """Cross-commodity ratio time-series — date-joined daily closes (Pro+)

        Paginated cross-commodity ratio series from the canonical price_bars store.

        Results are ordered DESC by date (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with points: [].

        A date where either leg has no bar is absent — no forward-fill, no
        fabrication (Invariant #1 honesty).

        Tier depth gates (same as /v1/bars 1d):
        - Free:  30 days (403 plan_gated)
        - Basic: 1 year  (403 plan_gated)
        - Pro+:  full history
        All pairs require Pro+ (all pairs involve a non-XAU or non-spot leg).

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns points older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            limit: Optional query parameter. Max points per page (1-10000). Default 100.
            pair: Required query parameter. Pair slug. Supported: gold-silver, gold-platinum, silver-platinum, gold-palladium, gld-xau.
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            RatiosResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("cursor", cursor, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(
            encode_query("limit", limit, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("pair", pair, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        return self._transport.request(
            "GET",
            encode_path("/v1/ratios", {}),
            _query,
            None,
            models.decode_RatiosResponse,
        )

    def list_iter(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        limit: int | None = None,
        pair: str,
        to: str,
    ) -> Iterator[models.RatioPoint]:
        """Cross-commodity ratio time-series — date-joined daily closes (Pro+)

        Paginated cross-commodity ratio series from the canonical price_bars store.

        Results are ordered DESC by date (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with points: [].

        A date where either leg has no bar is absent — no forward-fill, no
        fabrication (Invariant #1 honesty).

        Tier depth gates (same as /v1/bars 1d):
        - Free:  30 days (403 plan_gated)
        - Basic: 1 year  (403 plan_gated)
        - Pro+:  full history
        All pairs require Pro+ (all pairs involve a non-XAU or non-spot leg).

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns points older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            limit: Optional query parameter. Max points per page (1-10000). Default 100.
            pair: Required query parameter. Pair slug. Supported: gold-silver, gold-platinum, silver-platinum, gold-palladium, gld-xau.
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            Iterator[RatioPoint]: Items yielded lazily across pages.
        """

        def page(
            next_cursor: str | None,
        ) -> tuple[builtins.list[models.RatioPoint], str | None]:
            result = self.list(
                cursor=next_cursor, from_=from_, limit=limit, pair=pair, to=to
            )
            return [item for item in result.points], result.next_cursor

        return iterate(page, cursor)


class StableOperations:
    def __init__(self, transport: SyncTransport) -> None:
        self.account = Account(transport)
        self.bars = Bars(transport)
        self.convert = Convert(transport)
        self.prices = Prices(transport)
        self.ratios = Ratios(transport)
        self.unstable = UnstableOperations(transport)


class UnstableOperations:
    def __init__(self, transport: SyncTransport) -> None:
        pass


class AsyncAccount:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def usage(self) -> models.UsagePublic:
        """Authed key's day + month call counters

        Stability: stable.

        Returns:
            UsagePublic: Decoded response with header metadata.
        """
        _query: Query = []
        return await self._transport.request(
            "GET",
            encode_path("/v1/account/usage", {}),
            _query,
            None,
            models.decode_UsagePublic,
        )


class AsyncBars:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        interval: str | None = None,
        limit: int | None = None,
        symbol: str,
        to: str,
    ) -> models.BarsResponse:
        """OHLCV bar history — cursor-paginated, real data, is_closed label

        Paginated OHLCV bar history from the canonical price_bars store.

        Results are ordered DESC by bar_start (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with bars: [].

        Tier depth gates:
        - Free:  30 days
        - Basic: 1 year
        - Pro+:  full history (daily back to 1996 for XAU/USD; intraday from 2006)

        Intraday intervals (1m, 5m, 15m, 30m, 1h, 2h, 4h) require Pro+; Plus
        gets 1h only.

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns bars older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            interval: Optional query parameter. Bar interval. One of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d.
            limit: Optional query parameter. Max bars per page (1-10000). Default 100.
            symbol: Required query parameter. Symbol in slash or dash form. E.g. \"XAU/USD\", \"XAU-USD-SPOT\", \"GLD\".
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            BarsResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("cursor", cursor, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(
            encode_query("interval", interval, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("limit", limit, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        return await self._transport.request(
            "GET", encode_path("/v1/bars", {}), _query, None, models.decode_BarsResponse
        )

    def list_iter(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        interval: str | None = None,
        limit: int | None = None,
        symbol: str,
        to: str,
    ) -> AsyncIterator[models.Bar]:
        """OHLCV bar history — cursor-paginated, real data, is_closed label

        Paginated OHLCV bar history from the canonical price_bars store.

        Results are ordered DESC by bar_start (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with bars: [].

        Tier depth gates:
        - Free:  30 days
        - Basic: 1 year
        - Pro+:  full history (daily back to 1996 for XAU/USD; intraday from 2006)

        Intraday intervals (1m, 5m, 15m, 30m, 1h, 2h, 4h) require Pro+; Plus
        gets 1h only.

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns bars older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            interval: Optional query parameter. Bar interval. One of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d.
            limit: Optional query parameter. Max bars per page (1-10000). Default 100.
            symbol: Required query parameter. Symbol in slash or dash form. E.g. \"XAU/USD\", \"XAU-USD-SPOT\", \"GLD\".
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            AsyncIterator[Bar]: Items yielded lazily across pages.
        """

        async def page(
            next_cursor: str | None,
        ) -> tuple[builtins.list[models.Bar], str | None]:
            result = await self.list(
                cursor=next_cursor,
                from_=from_,
                interval=interval,
                limit=limit,
                symbol=symbol,
                to=to,
            )
            return [item for item in result.bars], result.next_cursor

        return iterate_async(page, cursor)

    async def latest(
        self, *, interval: str | None = None, symbol: str
    ) -> models.LatestBarResponse:
        """Latest bar for a symbol+interval — the most-recent settled or forming bar

        Return the single most-recent bar for a symbol+interval.

        Ordered by bar_start DESC, returns the first row. Provisional (forming)
        bars are returned with is_closed=False. Empty → 200 with bar: null, never
        404. No tier gate on this endpoint (latest bar is the lightest read;
        depth-gating only applies to ranges).

        Stability: stable.

        Args:
            interval: Optional query parameter. Bar interval. One of: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d.
            symbol: Required query parameter. Symbol in slash or dash form. E.g. \"XAU/USD\", \"GLD\".

        Returns:
            LatestBarResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("interval", interval, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=True, decimal=False)
        )
        return await self._transport.request(
            "GET",
            encode_path("/v1/bars/latest", {}),
            _query,
            None,
            models.decode_LatestBarResponse,
        )


class AsyncConvert:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def carat(self, *, currency: str | None = None) -> models.CaratResponse:
        """Per-gram gold price by karat purity

        Per-gram XAU price for karats 24 / 22 / 21 / 20 / 18 / 16 / 14 / 10.

        Logic: per_gram_24k = spot_xau_usd_per_oz / GRAMS_PER_TROY_OUNCE * fx_rate;
        per_gram_Nk = per_gram_24k * N/24.

        Historical `date` support is not implemented; omit the param or use
        /v1/prices/history + do the math client-side.

        Stability: stable.

        Args:
            currency: Optional query parameter. Quote currency (default USD).

        Returns:
            CaratResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("currency", currency, "single", required=False, decimal=False)
        )
        return await self._transport.request(
            "GET",
            encode_path("/v1/carat", {}),
            _query,
            None,
            models.decode_CaratResponse,
        )

    async def amount(
        self,
        *,
        amount: Decimal | str | None = None,
        from_: str,
        to: str,
        unit: str | None = None,
    ) -> models.ConvertResponse:
        """Convert between metals, currencies, and units

        Convert an amount between metals, currencies, and units.

        - metal → currency: spot price in that currency via FX cross through USD
        - currency → metal: inverse of the above
        - metal → metal: ratio of USD spot prices
        - currency → currency: FX cross through USD (live rate first, then the
          last stored rate only up to three days old)

        Two-leg source skew: currency → currency conversions resolve EACH leg
        independently through the fresh-first/last-stored chain, so the two
        legs can have different ages (e.g. a fresh EUR rate crossed with an
        older stored THB rate). The response `timestamp` reflects
        the `to` leg only — the `from` leg's timestamp is discarded — so it
        can understate (or overstate) the age of the other half of the cross.
        Both legs share the USD anchor, so cross drift is bounded by the
        staleness of the older leg — never compounded.

        The `unit` param applies to the metal side only (oz / gram / kg).
        Historical conversion via `date` is not supported; use /v1/bars +
        /v1/prices/history for historical spot data.

        Stability: stable.

        Args:
            amount: Optional query parameter. Amount to convert (default 1).
            from_: Required query parameter. Source symbol: XAU, XAG, USD, EUR, …
            to: Required query parameter. Target symbol: USD, EUR, XAU, …
            unit: Optional query parameter. Unit for the metal side: oz | gram | kg (default oz).

        Returns:
            ConvertResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("amount", amount, "single", required=False, decimal=True)
        )
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        _query.extend(
            encode_query("unit", unit, "single", required=False, decimal=False)
        )
        return await self._transport.request(
            "GET",
            encode_path("/v1/convert", {}),
            _query,
            None,
            models.decode_ConvertResponse,
        )


class AsyncPrices:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def history(
        self,
        *,
        from_: str,
        interval: str | None = None,
        limit: int | None = None,
        symbol: str,
        to: str,
    ) -> models.HistoryResponse:
        """[DEPRECATED — use /v1/bars] Aggregated close history for a symbol — interval ∈ {1d, 1h}.

        Dispatch to the per-interval handler. The handler is the Module
        Interface; per-interval helpers are Deep Modules hiding the
        interval-specific policy + storage shape.

        DEPRECATED in favour of /v1/bars (C4). This endpoint retains the
        legacy close-only series[] wire shape for backward compatibility.
        Deprecation + Sunset + Link headers are injected on every 200 response
        (and on 403 plan_gated, where the caller may need to upgrade before
        migrating). The sunset DATE is founder-controlled (see config
        prices_history_sunset_date) — NOT hardcoded here.

        Stability: stable.

        Args:
            from_: Required query parameter.
            interval: Optional query parameter.
            limit: Optional query parameter.
            symbol: Required query parameter.
            to: Required query parameter.

        Returns:
            HistoryResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(
            encode_query("interval", interval, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("limit", limit, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        return await self._transport.request(
            "GET",
            encode_path("/v1/prices/history", {}),
            _query,
            None,
            models.decode_HistoryResponse,
        )

    async def list(
        self, *, include: str | None = None, symbol: str | None = None
    ) -> models.SpotListResponse:
        """Latest aggregated price per (symbol, currency, contract_type)

        Stability: stable.

        Args:
            include: Optional query parameter. Comma-separated field groups to include in the response. Tokens: sources, karat, stats, all. Unknown tokens are ignored. Omit for the lean default. The stats group requires authentication.
            symbol: Optional query parameter.

        Returns:
            SpotListResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("include", include, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("symbol", symbol, "single", required=False, decimal=False)
        )
        return await self._transport.request(
            "GET",
            encode_path("/v1/prices", {}),
            _query,
            None,
            models.decode_SpotListResponse,
        )

    async def spot(
        self, symbol: str, *, include: str | None = None
    ) -> models.SpotResponse:
        """Latest spot price for one symbol — flat shape, no envelope (parity convenience)

        Stability: stable.

        Args:
            symbol: Required path parameter.
            include: Optional query parameter. Comma-separated field groups to include in the response. Tokens: sources, karat, stats, all. Unknown tokens are ignored. Omit for the lean default. The stats group requires authentication.

        Returns:
            SpotResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("include", include, "single", required=False, decimal=False)
        )
        return await self._transport.request(
            "GET",
            encode_path("/v1/spot/{symbol}", {"symbol": symbol}),
            _query,
            None,
            models.decode_SpotResponse,
        )


class AsyncRatios:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def latest(self, *, pair: str) -> models.LatestRatioResponse:
        """Latest ratio point for a pair — the most-recent shared-date ratio (Pro+)

        Return the single most-recent shared-date ratio point for a pair.

        Returns 200 with point: null when no shared date exists (e.g. before
        either leg is backfilled) — never 404 on empty (mirrors /v1/bars/latest).

        Stability: stable.

        Args:
            pair: Required query parameter. Pair slug (e.g. 'gold-silver', 'gold-platinum', 'gld-xau').

        Returns:
            LatestRatioResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("pair", pair, "single", required=True, decimal=False)
        )
        return await self._transport.request(
            "GET",
            encode_path("/v1/ratios/latest", {}),
            _query,
            None,
            models.decode_LatestRatioResponse,
        )

    async def list(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        limit: int | None = None,
        pair: str,
        to: str,
    ) -> models.RatiosResponse:
        """Cross-commodity ratio time-series — date-joined daily closes (Pro+)

        Paginated cross-commodity ratio series from the canonical price_bars store.

        Results are ordered DESC by date (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with points: [].

        A date where either leg has no bar is absent — no forward-fill, no
        fabrication (Invariant #1 honesty).

        Tier depth gates (same as /v1/bars 1d):
        - Free:  30 days (403 plan_gated)
        - Basic: 1 year  (403 plan_gated)
        - Pro+:  full history
        All pairs require Pro+ (all pairs involve a non-XAU or non-spot leg).

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns points older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            limit: Optional query parameter. Max points per page (1-10000). Default 100.
            pair: Required query parameter. Pair slug. Supported: gold-silver, gold-platinum, silver-platinum, gold-palladium, gld-xau.
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            RatiosResponse: Decoded response with header metadata.
        """
        _query: Query = []
        _query.extend(
            encode_query("cursor", cursor, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("from", from_, "single", required=True, decimal=False)
        )
        _query.extend(
            encode_query("limit", limit, "single", required=False, decimal=False)
        )
        _query.extend(
            encode_query("pair", pair, "single", required=True, decimal=False)
        )
        _query.extend(encode_query("to", to, "single", required=True, decimal=False))
        return await self._transport.request(
            "GET",
            encode_path("/v1/ratios", {}),
            _query,
            None,
            models.decode_RatiosResponse,
        )

    def list_iter(
        self,
        *,
        cursor: str | None = None,
        from_: str,
        limit: int | None = None,
        pair: str,
        to: str,
    ) -> AsyncIterator[models.RatioPoint]:
        """Cross-commodity ratio time-series — date-joined daily closes (Pro+)

        Paginated cross-commodity ratio series from the canonical price_bars store.

        Results are ordered DESC by date (newest first). Paginate via
        next_cursor — pass it as ?cursor= on the next request. When next_cursor
        is null the result is exhausted. Empty range returns 200 with points: [].

        A date where either leg has no bar is absent — no forward-fill, no
        fabrication (Invariant #1 honesty).

        Tier depth gates (same as /v1/bars 1d):
        - Free:  30 days (403 plan_gated)
        - Basic: 1 year  (403 plan_gated)
        - Pro+:  full history
        All pairs require Pro+ (all pairs involve a non-XAU or non-spot leg).

        Stability: stable.

        Args:
            cursor: Optional query parameter. Opaque keyset pagination cursor from a prior response's next_cursor. When set, returns points older than the cursor within the from/to window.
            from_: Required query parameter. ISO-8601 start (inclusive).
            limit: Optional query parameter. Max points per page (1-10000). Default 100.
            pair: Required query parameter. Pair slug. Supported: gold-silver, gold-platinum, silver-platinum, gold-palladium, gld-xau.
            to: Required query parameter. ISO-8601 end (inclusive).

        Returns:
            AsyncIterator[RatioPoint]: Items yielded lazily across pages.
        """

        async def page(
            next_cursor: str | None,
        ) -> tuple[builtins.list[models.RatioPoint], str | None]:
            result = await self.list(
                cursor=next_cursor, from_=from_, limit=limit, pair=pair, to=to
            )
            return [item for item in result.points], result.next_cursor

        return iterate_async(page, cursor)


class AsyncStableOperations:
    def __init__(self, transport: AsyncTransport) -> None:
        self.account = AsyncAccount(transport)
        self.bars = AsyncBars(transport)
        self.convert = AsyncConvert(transport)
        self.prices = AsyncPrices(transport)
        self.ratios = AsyncRatios(transport)
        self.unstable = AsyncUnstableOperations(transport)


class AsyncUnstableOperations:
    def __init__(self, transport: AsyncTransport) -> None:
        pass
