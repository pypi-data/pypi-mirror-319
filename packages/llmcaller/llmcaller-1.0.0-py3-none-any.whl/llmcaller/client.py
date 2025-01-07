"""LLMCaller client implementations."""

import json
from typing import AsyncGenerator, Dict, Generator, Optional, Union
import aiohttp
import requests
import sseclient

from .exceptions import APIError, ValidationError
from .types import LLMRequest, LLMResponse, ModelInfo, ModelList

class BaseClient:
    """Base class for LLMCaller clients."""

    def __init__(
        self,
        base_url: str = "http://localhost:3000",
        api_key: Optional[str] = None,
        default_provider: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        """Initialize the client.
        
        Args:
            base_url: API base URL
            api_key: API key for authentication
            default_provider: Default LLM provider
            default_model: Default model for the provider
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {api_key}"} if api_key else {})
        }
        self.default_provider = default_provider
        self.default_model = default_model

    def _validate_request(self, request: Dict) -> None:
        """Validate request parameters.
        
        Args:
            request: Request parameters
            
        Raises:
            ValidationError: If validation fails
        """
        if not request.get('prompt', '').strip():
            raise ValidationError("Prompt is required", "prompt")

        if 'temperature' in request:
            temp = request['temperature']
            if not isinstance(temp, (int, float)) or temp < 0 or temp > 1:
                raise ValidationError("Temperature must be between 0 and 1", "temperature")

        if 'max_tokens' in request:
            tokens = request['max_tokens']
            if not isinstance(tokens, int) or tokens <= 0:
                raise ValidationError("Max tokens must be greater than 0", "max_tokens")

    def _prepare_request(self, request: Dict) -> Dict:
        """Prepare request parameters.
        
        Args:
            request: Request parameters
            
        Returns:
            Prepared request parameters
        """
        prepared = {
            **request,
            "provider": request.get("provider") or self.default_provider,
            **({"model": request.get("model") or self.default_model}
               if self.default_model else {}),
        }
        return {k: v for k, v in prepared.items() if v is not None}

class AsyncLLMCaller(BaseClient):
    """Asynchronous implementation of LLMCaller client."""

    async def generate(self, request: Union[LLMRequest, Dict]) -> LLMResponse:
        """Generate a completion asynchronously.
        
        Args:
            request: Request parameters
            
        Returns:
            Generated response
            
        Raises:
            APIError: If the API request fails
            ValidationError: If request validation fails
        """
        self._validate_request(request)
        payload = self._prepare_request(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/v1/generate",
                headers=self.headers,
                json=payload
            ) as response:
                if not response.ok:
                    raise APIError(
                        response.status,
                        response.reason,
                        await response.text()
                    )
                return await response.json()

    async def generate_stream(
        self, request: Union[LLMRequest, Dict]
    ) -> AsyncGenerator[LLMResponse, None]:
        """Stream completions asynchronously.
        
        Args:
            request: Request parameters
            
        Yields:
            Chunks of the generated response
            
        Raises:
            APIError: If the API request fails
            ValidationError: If request validation fails
        """
        self._validate_request(request)
        payload = self._prepare_request(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/v1/generate/stream",
                headers=self.headers,
                json=payload
            ) as response:
                if not response.ok:
                    raise APIError(response.status, response.reason)

                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        yield data

    async def list_models(self, provider: str) -> ModelList:
        """Get information about available models for a provider.
        
        Args:
            provider: Provider name
            
        Returns:
            Model information
            
        Raises:
            APIError: If the API request fails
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/v1/models/{provider}",
                headers=self.headers
            ) as response:
                if not response.ok:
                    raise APIError(response.status, response.reason)
                return await response.json()

    async def get_model_info(self, provider: str, model_id: str) -> ModelInfo:
        """Get detailed information about a specific model.
        
        Args:
            provider: Provider name
            model_id: Model identifier
            
        Returns:
            Model details
            
        Raises:
            APIError: If the API request fails
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/v1/models/{provider}/{model_id}",
                headers=self.headers
            ) as response:
                if not response.ok:
                    raise APIError(response.status, response.reason)
                return await response.json()

class LLMCaller(BaseClient):
    """Synchronous implementation of LLMCaller client."""

    def generate(self, request: Union[LLMRequest, Dict]) -> LLMResponse:
        """Generate a completion synchronously.
        
        Args:
            request: Request parameters
            
        Returns:
            Generated response
            
        Raises:
            APIError: If the API request fails
            ValidationError: If request validation fails
        """
        self._validate_request(request)
        payload = self._prepare_request(request)

        response = requests.post(
            f"{self.base_url}/v1/generate",
            headers=self.headers,
            json=payload
        )
        
        if not response.ok:
            raise APIError(response.status_code, response.reason, response.text)
        
        return response.json()

    def generate_stream(
        self, request: Union[LLMRequest, Dict]
    ) -> Generator[LLMResponse, None, None]:
        """Stream completions synchronously.
        
        Args:
            request: Request parameters
            
        Yields:
            Chunks of the generated response
            
        Raises:
            APIError: If the API request fails
            ValidationError: If request validation fails
        """
        self._validate_request(request)
        payload = self._prepare_request(request)

        response = requests.post(
            f"{self.base_url}/v1/generate/stream",
            headers=self.headers,
            json=payload,
            stream=True
        )
        
        if not response.ok:
            raise APIError(response.status_code, response.reason)

        client = sseclient.SSEClient(response)
        for event in client.events():
            if event.data:
                yield json.loads(event.data)

    def list_models(self, provider: str) -> ModelList:
        """Get information about available models for a provider.
        
        Args:
            provider: Provider name
            
        Returns:
            Model information
            
        Raises:
            APIError: If the API request fails
        """
        response = requests.get(
            f"{self.base_url}/v1/models/{provider}",
            headers=self.headers
        )
        
        if not response.ok:
            raise APIError(response.status_code, response.reason)
        
        return response.json()

    def get_model_info(self, provider: str, model_id: str) -> ModelInfo:
        """Get detailed information about a specific model.
        
        Args:
            provider: Provider name
            model_id: Model identifier
            
        Returns:
            Model details
            
        Raises:
            APIError: If the API request fails
        """
        response = requests.get(
            f"{self.base_url}/v1/models/{provider}/{model_id}",
            headers=self.headers
        )
        
        if not response.ok:
            raise APIError(response.status_code, response.reason)
        
        return response.json()
