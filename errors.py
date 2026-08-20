"""Standard error envelope + global exception handlers - Module 3.2 / 3.3 / 3.4."""

from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.core.logging_config import logger

# Stable, specific error codes consumers can branch on - Appendix B.1
CODE_BY_STATUS = {
    400: "VALIDATION_ERROR",
    401: "UNAUTHENTICATED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    410: "GONE",
    412: "PRECONDITION_FAILED",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMITED",
    500: "INTERNAL_ERROR",
    503: "NOT_READY",
}

MESSAGE_BY_CODE = {
    "UNAUTHENTICATED": "Missing or invalid credentials",
    "FORBIDDEN": "You do not have permission to perform this action",
    "NOT_FOUND": "The requested resource does not exist",
    "CONFLICT": "The request conflicts with the current state of the resource",
    "GONE": "This resource/version has been retired",
    "PRECONDITION_FAILED": "The resource was modified since you last read it (stale ETag)",
    "RATE_LIMITED": "Too many requests - slow down",
    "VALIDATION_ERROR": "Request failed validation",
    "INTERNAL_ERROR": "An unexpected error occurred",
    "NOT_READY": "Service is not ready to accept traffic",
}


def _envelope(code: str, message: str, request: Request, details=None) -> dict:
    body = {
        "error": {
            "code": code,
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        }
    }
    if details is not None:
        body["error"]["details"] = details
    return body


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=_envelope("VALIDATION_ERROR", "Request failed validation", request, exc.errors()),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # exc.detail is used as the stable error code when raised as
        # HTTPException(status_code=401, detail="UNAUTHENTICATED") elsewhere
        # in the app; otherwise fall back to a status-derived code.
        detail = exc.detail if isinstance(exc.detail, str) else None
        code = detail if detail in MESSAGE_BY_CODE else CODE_BY_STATUS.get(exc.status_code, "ERROR")
        message = MESSAGE_BY_CODE.get(code, detail or "Request failed")
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(code, message, request),
            headers=getattr(exc, "headers", None) or {},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(
            "unhandled_error",
            extra={"request_id": getattr(request.state, "request_id", None), "route": request.url.path},
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content=_envelope("INTERNAL_ERROR", "An unexpected error occurred", request),
        )
