from typing import AsyncGenerator
from app.core.config import settings
from app.infrastructure.llm.factory import LLMProviderFactory
from app.infrastructure.llm.router import LLMRouter

# Instantiates LLM Provider Client based on configurations
provider = LLMProviderFactory.create_provider(settings)
router = LLMRouter(provider=provider, secondary_model=settings.llm.secondary_model)


async def get_llm() -> AsyncGenerator[LLMRouter, None]:
    """Dependency provider yielding the configured LLMRouter client instance."""
    yield router
