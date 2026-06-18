"""Custom exceptions and exception handlers.

Centralizing exceptions keeps the API contract consistent.
"""
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class AppException(Exception):
    """Base exception for the application."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Internal server error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Resource not found"


class ConflictException(AppException):
    """Resource conflict (e.g. duplicate unique key)."""

    status_code = status.HTTP_409_CONFLICT
    message = "Resource already exists"


class BusinessRuleViolation(AppException):
    """Business rule was violated (e.g. insufficient stock)."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Business rule violation"


class ValidationException(AppException):
    """Domain validation failed."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Validation error"


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "type": exc.__class__.__name__},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": jsonable_encoder(exc.errors()),
                "type": "ValidationError",
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        # Map integrity errors (unique violations, FK violations) to friendly messages
        msg = str(exc.orig) if exc.orig else "Database integrity error"
        if "unique constraint" in msg.lower() or "duplicate key" in msg.lower():
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Resource already exists", "type": "ConflictError"},
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": msg, "type": "IntegrityError"},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error", "type": "DatabaseError"},
        )
