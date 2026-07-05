import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.logging_context import request_id_ctx_var


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware responsible for generating and propagating trace request correlation IDs."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Check incoming request headers for a correlation ID
        correlation_id = (
            request.headers.get("X-Request-ID")
            or request.headers.get("X-Correlation-ID")
            or str(uuid.uuid4())
        )

        # Set the correlation ID in the async context variable
        token = request_id_ctx_var.set(correlation_id)

        try:
            response = await call_next(request)
            # Add the correlation ID to the response header
            response.headers["X-Request-ID"] = correlation_id
            return response
        finally:
            # Reset context variable to prevent cross-request leakage
            request_id_ctx_var.reset(token)
