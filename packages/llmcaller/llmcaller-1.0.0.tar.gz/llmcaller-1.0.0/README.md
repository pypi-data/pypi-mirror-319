# LLMCaller Python SDK

A Python SDK for interacting with the LLMCaller API, providing a unified interface for various LLM providers.

## Installation

```bash
pip install llmcaller
```

## Quick Start

```python
from llmcaller import LLMCaller, AsyncLLMCaller

# Synchronous usage
llm = LLMCaller(
    base_url="http://localhost:3000",  # Optional, defaults to http://localhost:3000
    api_key="your-api-key",           # Optional
    default_provider="openai",        # Optional
    default_model="gpt-3.5-turbo"    # Optional
)

# Basic completion
response = llm.generate({
    "prompt": "Explain quantum computing in simple terms",
    "provider": "openai",           # Optional if default_provider is set
    "model": "gpt-3.5-turbo",      # Optional if default_model is set
    "temperature": 0.7
})

print(response["content"])

# Streaming completion
for chunk in llm.generate_stream({
    "prompt": "Write a story about...",
    "system_prompt": "You are a creative writer.",
    "temperature": 0.8
}):
    print(chunk["content"], end="", flush=True)

# Asynchronous usage
import asyncio

async def main():
    async_llm = AsyncLLMCaller()
    
    # Basic completion
    response = await async_llm.generate({
        "prompt": "Explain the theory of relativity",
        "provider": "anthropic",
        "model": "claude-3-opus-20240229"
    })
    print(response["content"])
    
    # Streaming completion
    async for chunk in async_llm.generate_stream({
        "prompt": "Write a Python function to...",
        "system_prompt": "You are a Python expert."
    }):
        print(chunk["content"], end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Unified interface for multiple LLM providers (OpenAI, Anthropic, etc.)
- Both synchronous and asynchronous clients
- Streaming support for real-time responses
- Type hints for better development experience
- Comprehensive error handling
- Model information and capabilities querying

## Error Handling

```python
from llmcaller import APIError, ValidationError

try:
    response = llm.generate({
        "prompt": "",  # Invalid: empty prompt
        "temperature": 2.0  # Invalid: temperature > 1
    })
except ValidationError as e:
    print(f"Validation error: {e.message} (Field: {e.field})")
except APIError as e:
    print(f"API error: {e.status} {e.status_text}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## API Reference

### Configuration

Both `LLMCaller` and `AsyncLLMCaller` accept the following initialization parameters:

```python
def __init__(
    base_url: str = "http://localhost:3000",
    api_key: Optional[str] = None,
    default_provider: Optional[str] = None,
    default_model: Optional[str] = None
)
```

### Methods

#### generate(request: Dict) -> Dict

Generate a completion from the LLM.

```python
request = {
    "prompt": str,           # Required: The input prompt
    "provider": str,         # Optional: LLM provider
    "model": str,           # Optional: Model name
    "system_prompt": str,   # Optional: System prompt
    "temperature": float,   # Optional: Temperature (0-1)
    "max_tokens": int,      # Optional: Maximum tokens
    "top_p": float,        # Optional: Top-p sampling
    "frequency_penalty": float,  # Optional: Frequency penalty
    "presence_penalty": float    # Optional: Presence penalty
}

response = {
    "content": str,
    "model": str,
    "provider": str,
    "usage": {              # Optional
        "prompt_tokens": int,
        "completion_tokens": int,
        "total_tokens": int
    }
}
```

#### generate_stream(request: Dict) -> Generator[Dict, None, None]

Stream completions from the LLM. Same request/response format as `generate()`.

#### list_models(provider: str) -> Dict

Get information about available models for a provider.

#### get_model_info(provider: str, model_id: str) -> Dict

Get detailed information about a specific model.

## License

MIT
