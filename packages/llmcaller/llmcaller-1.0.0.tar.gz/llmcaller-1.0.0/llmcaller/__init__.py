"""LLMCaller SDK - A unified interface for LLM providers."""

from .client import AsyncLLMCaller, LLMCaller
from .exceptions import (
    LLMCallerError,
    APIError,
    ValidationError,
    UnsupportedProviderError,
    ModelNotFoundError,
)
from .types import (
    LLMRequest,
    LLMResponse,
    ModelInfo,
    ModelList,
    ModelPricing,
    Usage,
)

__version__ = "1.0.0"
__all__ = [
    # Main client classes
    "AsyncLLMCaller",
    "LLMCaller",
    
    # Exceptions
    "LLMCallerError",
    "APIError",
    "ValidationError",
    "UnsupportedProviderError",
    "ModelNotFoundError",
    
    # Type definitions
    "LLMRequest",
    "LLMResponse",
    "ModelInfo",
    "ModelList",
    "ModelPricing",
    "Usage",
]

# Default client instance for convenience
default_client = LLMCaller()
