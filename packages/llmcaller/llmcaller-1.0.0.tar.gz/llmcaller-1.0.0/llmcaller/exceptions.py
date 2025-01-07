"""Custom exceptions for the LLMCaller SDK."""

class LLMCallerError(Exception):
    """Base exception for LLMCaller errors."""
    pass

class APIError(LLMCallerError):
    """Exception raised when API request fails."""
    
    def __init__(self, status: int, status_text: str, message: str = None):
        self.status = status
        self.status_text = status_text
        super().__init__(message or f"API error: {status} {status_text}")

class ValidationError(LLMCallerError):
    """Exception raised when request validation fails."""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message)

class UnsupportedProviderError(LLMCallerError):
    """Exception raised when provider is not supported."""
    
    def __init__(self, provider: str):
        self.provider = provider
        super().__init__(f"Provider '{provider}' is not supported")

class ModelNotFoundError(LLMCallerError):
    """Exception raised when model is not found."""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        super().__init__(f"Model '{model}' not found for provider '{provider}'")
