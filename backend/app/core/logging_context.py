from contextvars import ContextVar

# Async-safe request correlation ID holder
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    """Retrieve the current request correlation ID from context."""
    return request_id_ctx_var.get()


def set_request_id(request_id: str) -> None:
    """Set the request correlation ID in the context."""
    request_id_ctx_var.set(request_id)
