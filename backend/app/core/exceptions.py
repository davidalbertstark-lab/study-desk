from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.responses import error_response
from app.modules.auth.exceptions import AuthException


# ==========================
# HTTP EXCEPTIONS
# ==========================
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=str(exc.detail)
        )
    )


# ==========================
# VALIDATION ERRORS (422)
# ==========================
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Validation failed",
            errors=exc.errors()
        )
    )


# ==========================
# INTERNAL SERVER ERRORS
# ==========================
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Internal server error"
        )
    )


async def auth_exception_handler(request, exc: AuthException):
    return JSONResponse(
        status_code=400,
        content=error_response(
            message=exc.message,
            errors={
                "code": exc.code
            }
        )
    )