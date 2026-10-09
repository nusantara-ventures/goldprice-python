"""Lazy iteration retains filters and stops only at the end of a page chain."""

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import TypeVar

from ._decode import read_cursor, read_list
from .errors import DecodeError

T = TypeVar("T")


def iterate(
    page: Callable[[str | None], tuple[list[T], str | None]], cursor: str | None
) -> Iterator[T]:
    while True:
        items, cursor = page(cursor)
        yield from items
        if cursor is None:
            return


async def iterate_async(
    page: Callable[[str | None], Awaitable[tuple[list[T], str | None]]],
    cursor: str | None,
) -> AsyncIterator[T]:
    while True:
        items, cursor = await page(cursor)
        for item in items:
            yield item
        if cursor is None:
            return


def unknown_page(
    raw: dict[str, object],
    items_field: str,
    cursor_field: str,
    decode: Callable[[object], T],
    raw_body: bytes,
) -> tuple[list[T], str | None]:
    """Future page tags retain raw item variants while using the page envelope."""
    try:
        items = [decode(item) for item in read_list(raw[items_field])]
        cursor = raw.get(cursor_field)
        return items, read_cursor(cursor) if cursor is not None else None
    except (KeyError, ValueError, TypeError):
        raise DecodeError(raw_body) from None
