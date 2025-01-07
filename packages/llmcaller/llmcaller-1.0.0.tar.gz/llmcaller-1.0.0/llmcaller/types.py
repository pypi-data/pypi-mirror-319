"""Type definitions for the LLMCaller SDK."""

from typing import Dict, Optional, TypedDict, Union
from typing_extensions import NotRequired

class Usage(TypedDict):
    """Usage statistics for an LLM request."""
    prompt_tokens: NotRequired[int]
    completion_tokens: NotRequired[int]
    total_tokens: NotRequired[int]

class LLMResponse(TypedDict):
    """Response from an LLM provider."""
    content: str
    model: str
    provider: str
    usage: NotRequired[Usage]

class ModelPricing(TypedDict):
    """Pricing information for a model."""
    input: float
    output: float

class ModelInfo(TypedDict):
    """Information about an LLM model."""
    id: str
    name: str
    provider: str
    capabilities: list[str]
    max_tokens: NotRequired[int]
    pricing: NotRequired[ModelPricing]

class ModelList(TypedDict):
    """List of models for a provider."""
    provider: str
    models: list[ModelInfo]

class LLMRequest(TypedDict, total=False):
    """Request parameters for LLM generation."""
    prompt: str  # Required
    provider: str
    model: str
    system_prompt: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
