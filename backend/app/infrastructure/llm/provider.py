import logging
from abc import ABC, abstractmethod
import httpx
import litellm
from app.infrastructure.llm.models import LLMRequest, LLMResponse, TokenUsage
from app.infrastructure.llm.exceptions import LLMProviderException, LLMTimeoutException

logger = logging.getLogger(__name__)

# Suppress litellm noisy telemetry warnings
litellm.telemetry = False
litellm.num_retries = 1


class BaseLLMProvider(ABC):
    """Abstract interface defining required behaviors for LLM service adapters."""

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Process messages and configuration to return a unified response block."""
        pass

    @abstractmethod
    async def check_ready(self) -> bool:
        """Ping the LLM service connection endpoint to assert system readiness."""
        pass


class LiteLLMProvider(BaseLLMProvider):
    """Concrete implementation of BaseLLMProvider routing via LiteLLM."""

    def __init__(self, api_base: str, default_model: str) -> None:
        self.api_base = api_base
        self.default_model = default_model

    async def generate(self, request: LLMRequest) -> LLMResponse:
        model = request.model or self.default_model
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        # Configure connection base if querying local Ollama instance
        api_base = None
        if (
            "ollama" in model
            or "localhost" in self.api_base
            or "ollama" in self.api_base
        ):
            api_base = self.api_base

        try:
            logger.debug(
                f"LiteLLMProvider: generating completion via model '{model}' at base '{api_base or 'cloud'}'"
            )
            response = await litellm.acompletion(
                model=model,
                messages=messages,
                api_base=api_base,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                response_format={"type": "json_object"} if request.json_mode else None,
                **request.extra_params,
            )

            text = response.choices[0].message.content or ""
            usage_data = getattr(response, "usage", None)
            usage = TokenUsage()

            if usage_data:
                usage = TokenUsage(
                    prompt_tokens=getattr(usage_data, "prompt_tokens", 0),
                    completion_tokens=getattr(usage_data, "completion_tokens", 0),
                    total_tokens=getattr(usage_data, "total_tokens", 0),
                )

            return LLMResponse(text=text, model=model, usage=usage, raw=response)
        except httpx.TimeoutException as e:
            raise LLMTimeoutException(
                f"LLM request timed out: {e}", provider="litellm", details=str(e)
            )
        except Exception as e:
            logger.error(f"LiteLLM request failed: {e}", exc_info=True)
            raise LLMProviderException(
                f"Failed to generate text from provider: {e}",
                provider="litellm",
                details=str(e),
            )

    async def check_ready(self) -> bool:
        """Verify the LLM provider service connection is active."""
        # For Ollama / local setups, verify endpoint tags availability
        if "localhost" in self.api_base or "ollama" in self.api_base:
            try:
                async with httpx.AsyncClient(timeout=2.0) as client:
                    response = await client.get(f"{self.api_base}/api/tags")
                    return response.status_code == 200
            except Exception as e:
                logger.error(f"Ollama connection check failed: {e}")
                return False
        # For cloud providers, assume ready if API configurations are loaded
        return True
