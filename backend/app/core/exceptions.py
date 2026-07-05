import logging
from typing import Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class SentinelException(Exception):
    """Base exception for all errors in Sentinel AI."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class DomainException(SentinelException):
    """Raised when a business rule or invariant is violated."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="DOMAIN_RULE_VIOLATION",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class NotFoundException(SentinelException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class DatabaseException(SentinelException):
    """Raised when a database operations fails."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
        )


class AuthenticationException(SentinelException):
    """Raised during failed login, expired tokens, or permission issues."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="UNAUTHENTICATED",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class AgentException(SentinelException):
    """Raised when an AI Agent or workflow execution encounters an error."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="AGENT_EXECUTION_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers standard handlers to intercept Sentinel exceptions and return standardized payloads."""

    @app.exception_handler(SentinelException)
    async def sentinel_exception_handler(
        request: Request, exc: SentinelException
    ) -> JSONResponse:
        logger.error(
            f"SentinelException: Code={exc.code}, Message='{exc.message}', Status={exc.status_code}",
            exc_info=exc.status_code >= 500,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details or {},
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.critical("Unhandled server exception encountered", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please contact system support.",
                    "details": str(exc) if app.debug else {},
                }
            },
        )
