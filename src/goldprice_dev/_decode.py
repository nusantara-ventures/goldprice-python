"""Strict wire primitives used by generated decoders."""

import json
import re
from decimal import Decimal
from typing import cast


def read_object(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(k, str) for k in value):
        raise ValueError("expected an object")
    return cast(dict[str, object], value)


def read_list(value: object) -> list[object]:
    if not isinstance(value, list):
        raise TypeError("expected an array")
    return cast(list[object], value)


def read_str(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("expected a string")
    return value


def read_int(value: object) -> int:
    if type(value) is not int:
        raise ValueError("expected an integer")
    return value


def read_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise TypeError("expected a boolean")
    return value


def read_decimal(value: object) -> Decimal:
    text = read_str(value)
    if re.fullmatch(r"-?\d+(\.\d+)?", text, re.ASCII) is None:
        raise ValueError("expected a decimal wire string")
    return Decimal(text)


def read_decimal_number(value: object) -> Decimal:
    """A decimal sent as a JSON number; `read_json` keeps its literal as a Decimal."""
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        raise TypeError("expected a JSON number")
    if isinstance(value, Decimal) and not value.is_finite():
        raise ValueError("expected a finite JSON number")
    return Decimal(value)


def reject_number(value: str) -> object:
    raise ValueError("unexpected non-finite JSON number")


def read_json(raw: bytes) -> object:
    return json.loads(raw, parse_float=Decimal, parse_constant=reject_number)


def read_cursor(value: object) -> str:
    cursor = read_str(value)
    if not cursor:
        raise ValueError("next_cursor must not be empty")
    return cursor
