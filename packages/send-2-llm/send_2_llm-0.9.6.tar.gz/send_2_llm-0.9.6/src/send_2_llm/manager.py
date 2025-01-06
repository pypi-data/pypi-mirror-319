"""
LLM Manager - main interface for send_2_llm library.
Provides centralized management of all components.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from .types import (
    LLMRequest,
    LLMResponse,
    ProviderType,
    ProviderAPIError,
    ProviderError
)
from .security.manager import SecurityManager
from .validation.input_validator import InputValidator
from .stability.circuit_breaker import CircuitBreaker
from .stability.rate_limiter import RateLimiter
from .monitoring.metrics import Monitoring
from .providers.factory import ProviderFactory, ProviderInfo

logger = logging.getLogger(__name__)

class LLMManager:
    """Main interface for managing LLM operations."""
    
    def __init__(
        self,
        provider_factory: Optional[ProviderFactory] = None,
        rate_limiter: Optional[RateLimiter] = None,
        circuit_breaker: Optional[CircuitBreaker] = None,
        monitoring: Optional[Monitoring] = None
    ):
        """Initialize LLM Manager with all required components."""
        self.security = SecurityManager()
        self.validator = InputValidator()
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.monitoring = monitoring or Monitoring()
        self.provider_factory = provider_factory or ProviderFactory()
        
    def get_available_providers(self) -> List[ProviderInfo]:
        """Get list of available providers with their info."""
        return self.provider_factory.get_registered_providers()
        
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate response using specified provider with all safety checks.
        
        Args:
            request: LLMRequest object containing all request parameters
            
        Returns:
            LLMResponse object containing generated text and metadata
            
        Raises:
            SecurityError: If access is denied
            ValidationError: If input validation fails
            ProviderError: If provider is unavailable
            RateLimitError: If rate limit is exceeded
        """
        provider = request.provider_type
        model = request.model
        
        # Validate security access
        if not self.security.validate_access(provider, model):
            raise SecurityError(f"Access denied for {provider.value} with model {model}")
            
        # Validate input parameters
        self.validator.validate_prompt(request.prompt)
        self.validator.validate_parameters(
            provider=provider,
            model=model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p
        )
        
        # Check circuit breaker
        if not self.circuit_breaker.is_available(provider):
            raise ProviderError(f"Provider {provider.value} is currently unavailable")
            
        # Check rate limit
        await self.rate_limiter.acquire(provider)
        
        try:
            # Get provider instance
            provider_instance = self.provider_factory.create_provider(
                provider,
                model=model
            )
            
            # Start monitoring
            with self.monitoring.track_request(provider, model):
                # Generate response
                response = await provider_instance._generate(request)
                
                # Record success
                self.circuit_breaker.record_success(provider)
                
                return response
                
        except Exception as e:
            # Record failure
            self.circuit_breaker.record_error(provider)
            # Re-raise with context
            raise ProviderError(f"Generation failed: {str(e)}")
            
    async def list_models(self, provider: ProviderType) -> list[str]:
        """List available models for specified provider."""
        if not self.security.validate_api_key(provider):
            raise SecurityError(f"No valid API key for {provider.value}")
            
        provider_instance = self.provider_factory.create_provider(provider)
        return await provider_instance.list_models() 