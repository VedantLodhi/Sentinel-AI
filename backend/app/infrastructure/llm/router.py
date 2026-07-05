import logging
import time
from typing import List, Optional
from app.infrastructure.llm.provider import BaseLLMProvider
from app.infrastructure.llm.models import LLMMessage, LLMRequest, LLMResponse
from app.infrastructure.llm.exceptions import LLMException

logger = logging.getLogger(__name__)


class LLMRouter:
    """Orchestrator routing prompt execution across configured LLM models.

    Acts as the entrypoint for all AI components, providing model fallback logic
    and metric tracing.
    """

    def __init__(
        self, provider: BaseLLMProvider, secondary_model: Optional[str] = None
    ) -> None:
        self.provider = provider
        self.secondary_model = secondary_model

    async def generate(
        self,
        messages: List[LLMMessage],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Execute a text generation prompt. Falls back to secondary model if primary model fails."""
        start_time = time.perf_counter()
        request = LLMRequest(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=json_mode,
        )

        try:
            response = await self.provider.generate(request)
            latency = time.perf_counter() - start_time
            logger.info(
                f"LLM Success: Model='{response.model}' "
                f"Tokens={response.usage.total_tokens} "
                f"Latency={latency:.2f}s"
            )
            return response

        except LLMException as primary_err:
            # If a secondary fallback model is defined, attempt recovery
            if self.secondary_model and request.model != self.secondary_model:
                logger.warning(
                    f"LLM primary model failure: {primary_err}. "
                    f"Attempting fallback routing to secondary model: '{self.secondary_model}'"
                )
                fallback_request = LLMRequest(
                    messages=messages,
                    model=self.secondary_model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    json_mode=json_mode,
                )
                try:
                    fallback_response = await self.provider.generate(fallback_request)
                    latency = time.perf_counter() - start_time
                    logger.info(
                        f"LLM Fallback Success: Model='{fallback_response.model}' "
                        f"Tokens={fallback_response.usage.total_tokens} "
                        f"Latency={latency:.2f}s"
                    )
                    return fallback_response
                except Exception as fallback_err:
                    logger.critical(f"LLM fallback model failed: {fallback_err}")
                    raise fallback_err
            else:
                raise primary_err
