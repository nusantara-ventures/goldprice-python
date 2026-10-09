"""Response metadata comes exclusively from HTTP headers."""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RateLimit:
    limit: int | None = None
    remaining: int | None = None
    reset: str | None = None


@dataclass(frozen=True, slots=True)
class ResponseMeta:
    request_id: str | None = None
    quota: RateLimit | None = None
    short: RateLimit | None = None

    @classmethod
    def from_headers(cls, headers: Mapping[str, str]) -> "ResponseMeta":
        lower = {key.lower(): value for key, value in headers.items()}

        def rate(prefix: str) -> RateLimit | None:
            def integer(key: str) -> int | None:
                try:
                    return int(lower[prefix + key])
                except (KeyError, ValueError):
                    return None

            limit = integer("limit")
            remaining = integer("remaining")
            reset = lower.get(prefix + "reset")
            if limit is None and remaining is None and reset is None:
                return None
            return RateLimit(limit, remaining, reset)

        return cls(
            lower.get("x-request-id"), rate("x-ratelimit-"), rate("x-ratelimit-short-")
        )
