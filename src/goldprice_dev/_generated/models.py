# Generated from spec/goldprice/live/openapi.json sha256 7483e916b388f8b1a6b5c5689b0180ad8914fec2e5f28a0ffdaf041075039f65. Do not edit.
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from .._decode import (
    read_bool,
    read_cursor,
    read_decimal,
    read_int,
    read_list,
    read_object,
    read_str,
)
from .._meta import ResponseMeta


@dataclass(frozen=True, slots=True, kw_only=True)
class Bar:
    bar_start: str
    close: str | None = None
    high: str | None = None
    is_closed: bool
    low: str | None = None
    open: str | None = None
    volume: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class BarsMeta:
    count: int
    source_id: str | None = None
    tier: str


@dataclass(frozen=True, slots=True, kw_only=True)
class BarsResponse:
    bars: list[Bar]
    interval: str
    meta_: BarsMeta
    next_cursor: str | None = None
    symbol: str
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class CaratResponse:
    currency: str
    price_gram_10k: Decimal
    price_gram_14k: Decimal
    price_gram_16k: Decimal
    price_gram_18k: Decimal
    price_gram_20k: Decimal
    price_gram_21k: Decimal
    price_gram_22k: Decimal
    price_gram_24k: Decimal
    timestamp: str
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class ConvertResponse:
    amount: Decimal
    from_: str
    rate: Decimal
    result: str
    timestamp: str
    to: str
    unit: str
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class HistoryMeta:
    count: int
    ohlc_note: str
    tier: str


@dataclass(frozen=True, slots=True, kw_only=True)
class HistoryResponse:
    from_: str
    interval: str
    meta_: HistoryMeta
    series: list[HistorySeriesEntry]
    symbol: str
    to: str
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class HistorySeriesEntry:
    close: str | None = None
    date: str
    high: str | None = None
    is_closed: bool | None = None
    is_stale: bool
    low: str | None = None
    open: str | None = None
    volume: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class LatestBarResponse:
    bar: Bar | None = None
    interval: str
    meta_: BarsMeta
    symbol: str
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class LatestRatioResponse:
    denominator: str
    interval: str | None = None
    meta_: RatiosMeta
    numerator: str
    pair: str
    point: RatioPoint | None = None
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class RatioPoint:
    date: str
    denominator_close: str
    numerator_close: str
    ratio: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RatiosMeta:
    count: int
    tier: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RatiosResponse:
    denominator: str
    interval: str | None = None
    meta_: RatiosMeta
    next_cursor: str | None = None
    numerator: str
    pair: str
    points: list[RatioPoint]
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceEntry:
    display_name: str | None = None
    informational: bool | None = None
    is_stale: bool | None = None
    license: str | None = None
    price: Decimal | None = None
    source: str
    unit: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class SpotListResponse:
    symbols: list[SpotResponse]
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class SpotResponse:
    ask: str | None = None
    bid: str | None = None
    ch: str | None = None
    chp: str | None = None
    computed_at: str | None = None
    contract_type: str
    divergence_bps: int | None = None
    divergence_flag: bool | None = None
    high_price: Decimal | None = None
    is_stale: bool
    live_quality: str | None = None
    low_price: Decimal | None = None
    open_price: Decimal | None = None
    open_time: int | None = None
    prev_close_price: Decimal | None = None
    price: Decimal | None = None
    price_gram_10k: Decimal | None = None
    price_gram_14k: Decimal | None = None
    price_gram_16k: Decimal | None = None
    price_gram_18k: Decimal | None = None
    price_gram_20k: Decimal | None = None
    price_gram_21k: Decimal | None = None
    price_gram_22k: Decimal | None = None
    price_gram_24k: Decimal | None = None
    quote_currency: str
    sources: list[SourceEntry] | None = None
    symbol: str
    unit: str
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class UsagePublic:
    active_streams: int | None = None
    calls_this_month: int
    calls_today: int
    max_streams: int | None = None
    meta: ResponseMeta = field(default_factory=ResponseMeta, compare=False)


def decode_Bar(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> Bar:
    data = read_object(value)
    return Bar(
        bar_start=read_str(data["bar_start"]),
        close=read_str(data["close"]) if data.get("close") is not None else None,
        high=read_str(data["high"]) if data.get("high") is not None else None,
        is_closed=read_bool(data["is_closed"]),
        low=read_str(data["low"]) if data.get("low") is not None else None,
        open=read_str(data["open"]) if data.get("open") is not None else None,
        volume=read_str(data["volume"]) if data.get("volume") is not None else None,
    )


def decode_BarsMeta(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> BarsMeta:
    data = read_object(value)
    return BarsMeta(
        count=read_int(data["count"]),
        source_id=read_str(data["source_id"])
        if data.get("source_id") is not None
        else None,
        tier=read_str(data["tier"]),
    )


def decode_BarsResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> BarsResponse:
    data = read_object(value)
    return BarsResponse(
        bars=[decode_Bar(item0) for item0 in read_list(data["bars"])],
        interval=read_str(data["interval"]),
        meta_=decode_BarsMeta(data["meta"]),
        next_cursor=read_cursor(data["next_cursor"])
        if data.get("next_cursor") is not None
        else None,
        symbol=read_str(data["symbol"]),
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_CaratResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> CaratResponse:
    data = read_object(value)
    return CaratResponse(
        currency=read_str(data["currency"]),
        price_gram_10k=read_decimal(data["price_gram_10k"]),
        price_gram_14k=read_decimal(data["price_gram_14k"]),
        price_gram_16k=read_decimal(data["price_gram_16k"]),
        price_gram_18k=read_decimal(data["price_gram_18k"]),
        price_gram_20k=read_decimal(data["price_gram_20k"]),
        price_gram_21k=read_decimal(data["price_gram_21k"]),
        price_gram_22k=read_decimal(data["price_gram_22k"]),
        price_gram_24k=read_decimal(data["price_gram_24k"]),
        timestamp=read_str(data["timestamp"]),
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_ConvertResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> ConvertResponse:
    data = read_object(value)
    return ConvertResponse(
        amount=read_decimal(data["amount"]),
        from_=read_str(data["from"]),
        rate=read_decimal(data["rate"]),
        result=read_str(data["result"]),
        timestamp=read_str(data["timestamp"]),
        to=read_str(data["to"]),
        unit=read_str(data["unit"]),
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_HistoryMeta(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> HistoryMeta:
    data = read_object(value)
    return HistoryMeta(
        count=read_int(data["count"]),
        ohlc_note=read_str(data["ohlc_note"]),
        tier=read_str(data["tier"]),
    )


def decode_HistoryResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> HistoryResponse:
    data = read_object(value)
    return HistoryResponse(
        from_=read_str(data["from"]),
        interval=read_str(data["interval"]),
        meta_=decode_HistoryMeta(data["meta"]),
        series=[
            decode_HistorySeriesEntry(item0) for item0 in read_list(data["series"])
        ],
        symbol=read_str(data["symbol"]),
        to=read_str(data["to"]),
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_HistorySeriesEntry(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> HistorySeriesEntry:
    data = read_object(value)
    return HistorySeriesEntry(
        close=read_str(data["close"]) if data.get("close") is not None else None,
        date=read_str(data["date"]),
        high=read_str(data["high"]) if data.get("high") is not None else None,
        is_closed=read_bool(data["is_closed"])
        if data.get("is_closed") is not None
        else None,
        is_stale=read_bool(data["is_stale"]),
        low=read_str(data["low"]) if data.get("low") is not None else None,
        open=read_str(data["open"]) if data.get("open") is not None else None,
        volume=read_str(data["volume"]) if data.get("volume") is not None else None,
    )


def decode_LatestBarResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> LatestBarResponse:
    data = read_object(value)
    return LatestBarResponse(
        bar=decode_Bar(data["bar"]) if data.get("bar") is not None else None,
        interval=read_str(data["interval"]),
        meta_=decode_BarsMeta(data["meta"]),
        symbol=read_str(data["symbol"]),
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_LatestRatioResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> LatestRatioResponse:
    data = read_object(value)
    return LatestRatioResponse(
        denominator=read_str(data["denominator"]),
        interval=read_str(data["interval"])
        if data.get("interval") is not None
        else None,
        meta_=decode_RatiosMeta(data["meta"]),
        numerator=read_str(data["numerator"]),
        pair=read_str(data["pair"]),
        point=decode_RatioPoint(data["point"])
        if data.get("point") is not None
        else None,
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_RatioPoint(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> RatioPoint:
    data = read_object(value)
    return RatioPoint(
        date=read_str(data["date"]),
        denominator_close=read_str(data["denominator_close"]),
        numerator_close=read_str(data["numerator_close"]),
        ratio=read_str(data["ratio"]),
    )


def decode_RatiosMeta(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> RatiosMeta:
    data = read_object(value)
    return RatiosMeta(
        count=read_int(data["count"]),
        tier=read_str(data["tier"]),
    )


def decode_RatiosResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> RatiosResponse:
    data = read_object(value)
    return RatiosResponse(
        denominator=read_str(data["denominator"]),
        interval=read_str(data["interval"])
        if data.get("interval") is not None
        else None,
        meta_=decode_RatiosMeta(data["meta"]),
        next_cursor=read_cursor(data["next_cursor"])
        if data.get("next_cursor") is not None
        else None,
        numerator=read_str(data["numerator"]),
        pair=read_str(data["pair"]),
        points=[decode_RatioPoint(item0) for item0 in read_list(data["points"])],
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_SourceEntry(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> SourceEntry:
    data = read_object(value)
    return SourceEntry(
        display_name=read_str(data["display_name"])
        if data.get("display_name") is not None
        else None,
        informational=read_bool(data["informational"])
        if data.get("informational") is not None
        else None,
        is_stale=read_bool(data["is_stale"])
        if data.get("is_stale") is not None
        else None,
        license=read_str(data["license"]) if data.get("license") is not None else None,
        price=read_decimal(data["price"]) if data.get("price") is not None else None,
        source=read_str(data["source"]),
        unit=read_str(data["unit"]) if data.get("unit") is not None else None,
    )


def decode_SpotListResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> SpotListResponse:
    data = read_object(value)
    return SpotListResponse(
        symbols=[decode_SpotResponse(item0) for item0 in read_list(data["symbols"])],
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_SpotResponse(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> SpotResponse:
    data = read_object(value)
    return SpotResponse(
        ask=read_str(data["ask"]) if data.get("ask") is not None else None,
        bid=read_str(data["bid"]) if data.get("bid") is not None else None,
        ch=read_str(data["ch"]) if data.get("ch") is not None else None,
        chp=read_str(data["chp"]) if data.get("chp") is not None else None,
        computed_at=read_str(data["computed_at"])
        if data.get("computed_at") is not None
        else None,
        contract_type=read_str(data["contract_type"]),
        divergence_bps=read_int(data["divergence_bps"])
        if data.get("divergence_bps") is not None
        else None,
        divergence_flag=read_bool(data["divergence_flag"])
        if data.get("divergence_flag") is not None
        else None,
        high_price=read_decimal(data["high_price"])
        if data.get("high_price") is not None
        else None,
        is_stale=read_bool(data["is_stale"]),
        live_quality=read_str(data["live_quality"])
        if data.get("live_quality") is not None
        else None,
        low_price=read_decimal(data["low_price"])
        if data.get("low_price") is not None
        else None,
        open_price=read_decimal(data["open_price"])
        if data.get("open_price") is not None
        else None,
        open_time=read_int(data["open_time"])
        if data.get("open_time") is not None
        else None,
        prev_close_price=read_decimal(data["prev_close_price"])
        if data.get("prev_close_price") is not None
        else None,
        price=read_decimal(data["price"]) if data.get("price") is not None else None,
        price_gram_10k=read_decimal(data["price_gram_10k"])
        if data.get("price_gram_10k") is not None
        else None,
        price_gram_14k=read_decimal(data["price_gram_14k"])
        if data.get("price_gram_14k") is not None
        else None,
        price_gram_16k=read_decimal(data["price_gram_16k"])
        if data.get("price_gram_16k") is not None
        else None,
        price_gram_18k=read_decimal(data["price_gram_18k"])
        if data.get("price_gram_18k") is not None
        else None,
        price_gram_20k=read_decimal(data["price_gram_20k"])
        if data.get("price_gram_20k") is not None
        else None,
        price_gram_21k=read_decimal(data["price_gram_21k"])
        if data.get("price_gram_21k") is not None
        else None,
        price_gram_22k=read_decimal(data["price_gram_22k"])
        if data.get("price_gram_22k") is not None
        else None,
        price_gram_24k=read_decimal(data["price_gram_24k"])
        if data.get("price_gram_24k") is not None
        else None,
        quote_currency=read_str(data["quote_currency"]),
        sources=[decode_SourceEntry(item0) for item0 in read_list(data["sources"])]
        if data.get("sources") is not None
        else None,
        symbol=read_str(data["symbol"]),
        unit=read_str(data["unit"]),
        meta=meta if meta is not None else ResponseMeta(),
    )


def decode_UsagePublic(
    value: object, meta: ResponseMeta | None = None, raw_body: bytes = b""
) -> UsagePublic:
    data = read_object(value)
    return UsagePublic(
        active_streams=read_int(data["active_streams"])
        if data.get("active_streams") is not None
        else None,
        calls_this_month=read_int(data["calls_this_month"]),
        calls_today=read_int(data["calls_today"]),
        max_streams=read_int(data["max_streams"])
        if data.get("max_streams") is not None
        else None,
        meta=meta if meta is not None else ResponseMeta(),
    )
