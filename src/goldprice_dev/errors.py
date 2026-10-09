"""Typed failures with server problem fields and original response bytes."""


class GoldpriceError(Exception):
    """Base class for client failures."""

    def __reduce__(self) -> tuple[object, tuple[object, ...]]:
        return _restore_error, (type(self), self.args, self.__dict__)


def _restore_error(
    cls: type[GoldpriceError], args: tuple[object, ...], fields: dict[str, object]
) -> GoldpriceError:
    error = cls.__new__(cls)
    Exception.__init__(error, *args)
    error.__dict__.update(fields)
    return error


class ApiError(GoldpriceError):
    def __init__(
        self,
        *,
        status: int,
        code: str = "unknown",
        title: str = "",
        detail: str = "",
        request_id: str | None = None,
        instance: str | None = None,
        retry_after: int | None = None,
        raw_body: bytes = b"",
    ) -> None:
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail
        self.request_id = request_id
        self.instance = instance
        self.retry_after = retry_after
        self.raw_body = raw_body
        suffix = f" (request_id {request_id})" if request_id else ""
        super().__init__(f"HTTP {status} {code}: {title}{suffix}")

    def __repr__(self) -> str:
        return str(self)


class BadRequest(ApiError):
    pass


class Unauthorized(ApiError):
    pass


class NotFound(ApiError):
    pass


class ServiceUnavailable(ApiError):
    pass


class RateLimited(ApiError):
    @property
    def is_quota_exhausted(self) -> bool:
        return self.code in {"quota_exhausted", "quota_exceeded"}


class CursorExpired(ApiError):
    pass


class TransportError(GoldpriceError):
    def __init__(self, cause: Exception, *, response_received: bool = False) -> None:
        self.cause = cause
        self.response_received = response_received
        super().__init__("Request transport failed")


class DecodeError(GoldpriceError):
    def __init__(self, raw_body: bytes) -> None:
        self.raw_body = raw_body
        super().__init__("Response did not match the contract")
