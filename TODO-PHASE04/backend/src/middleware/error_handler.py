"""
Global error handling middleware for FastAPI.
Catches all exceptions and formats as standard ErrorResponse.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler that catches all unhandled exceptions.
    Formats errors as standard ErrorResponse and logs errors.
    """
    # Log the error
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Also print to console for debugging
    import traceback
    print(f"\n========== ERROR ==========")
    print(f"Exception: {exc}")
    print(f"Traceback:")
    traceback.print_exc()
    print(f"===========================\n")

    # Return 500 Internal Server Error
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
            }
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    Returns 400 Bad Request with field-level error details.
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({"field": field, "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input",
                "details": errors,
            }
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    Handle HTTP exceptions (404, 401, etc.).
    Formats as standard ErrorResponse.
    """
    # If detail is already a dict with error structure, use it
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    # Otherwise, create standard error format
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        500: "INTERNAL_ERROR",
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_codes.get(exc.status_code, "HTTP_ERROR"),
                "message": str(exc.detail),
            }
        },
    )
