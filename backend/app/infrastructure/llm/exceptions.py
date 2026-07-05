from typing import Any


class LLMException(Exception):
    """Base exception for all LLM client failures."""

    def __init__(self, message: str, provider: str, details: Any = None):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.details = details


class LLMTimeoutException(LLMException):
    """Raised when LLM client calls exceed deadlines."""

    pass


class LLMRateLimitException(LLMException):
    """Raised when request rate limits are hit on providers."""

    pass


class LLMProviderException(LLMException):
    """Raised when the LLM engine returns client errors or internal crashes."""

    pass
