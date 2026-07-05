from app.core.config.base import AppSettings
from app.infrastructure.llm.provider import BaseLLMProvider, LiteLLMProvider


class LLMProviderFactory:
    """Factory responsible for instantiating concrete LLM providers based on settings."""

    @staticmethod
    def create_provider(settings: AppSettings) -> BaseLLMProvider:
        """Construct provider based on config configurations.

        Standardizes on LiteLLMProvider routing either to local Ollama or fallback cloud setups.
        """
        # Expose factory hook to return mock provider if testing, or instantiate LiteLLM client
        return LiteLLMProvider(
            api_base=settings.llm.api_base, default_model=settings.llm.primary_model
        )
