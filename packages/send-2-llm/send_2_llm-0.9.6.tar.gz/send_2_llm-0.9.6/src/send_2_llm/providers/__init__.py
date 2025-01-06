"""Provider package."""

from .base import BaseLLMProvider
from .factory import ProviderFactory
from .manager import LLMManager

# Import only OpenAI provider by default
from .openai_provider import OpenAIProviderV2

__all__ = [
    "BaseLLMProvider",
    "ProviderFactory",
    "LLMManager",
    "OpenAIProviderV2",
]

def get_provider(provider_type: str):
    """Get provider class by type."""
    from ..types import ProviderType
    
    # Convert string to ProviderType
    try:
        provider_enum = ProviderType(provider_type)
    except ValueError:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    # Create factory and get provider class
    factory = ProviderFactory()
    provider_info = factory.get_provider_info(provider_enum)
    if not provider_info:
        raise ValueError(f"Provider {provider_type} not registered")
    return provider_info.provider_class 