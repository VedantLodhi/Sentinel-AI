from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    """Standard role-content pair representing conversational turns."""

    role: str = Field(pattern="^(system|user|assistant|tool)$")
    content: str


class LLMRequest(BaseModel):
    """Configuration payload for prompting an LLM interface."""

    messages: List[LLMMessage]
    model: Optional[str] = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    json_mode: bool = False
    extra_params: Dict[str, Any] = Field(default_factory=dict)


class TokenUsage(BaseModel):
    """Token reporting metrics for cost and trace tracking."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    """Unified response envelope returned by all internal LLM interfaces."""

    text: str
    model: str
    usage: TokenUsage = Field(default_factory=TokenUsage)
    raw: Any = None
