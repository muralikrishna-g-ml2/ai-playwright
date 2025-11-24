"""
Model provider abstraction for supporting multiple AI services.

This module provides a unified interface for different AI model providers,
allowing users to choose their preferred AI service for test healing.
"""

from abc import ABC, abstractmethod
import os
from typing import Optional


class ModelProvider(ABC):
    """
    Abstract base class for AI model providers.
    
    All model providers must implement the generate() method to provide
    a consistent interface for the HealerAgent.
    """
    
    @abstractmethod
    def generate(self, prompt: str) -> Optional[str]:
        """
        Generate a response from the AI model.
        
        Args:
            prompt (str): The prompt to send to the AI model
        
        Returns:
            Optional[str]: The generated response, or None if generation fails
        """
        pass


class GeminiProvider(ModelProvider):
    """
    Google Gemini AI provider.
    
    Uses Google's Generative AI API for healing suggestions.
    
    Environment Variables:
        GEMINI_API_KEY or GOOGLE_API_KEY: API key for Google Gemini
        GEMINI_MODEL: Model name (default: gemini-2.0-flash-lite-preview-02-05)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Gemini provider.
        
        Args:
            api_key (str, optional): Gemini API key
            model (str, optional): Model name to use
        """
        import google.generativeai as genai
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY is required for GeminiProvider")
        
        self.model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite-preview-02-05")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate response using Gemini."""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini generation failed: {e}")
            return None


class OpenAIProvider(ModelProvider):
    """
    OpenAI (ChatGPT) provider.
    
    Uses OpenAI's API for healing suggestions.
    
    Environment Variables:
        OPENAI_API_KEY: API key for OpenAI
        OPENAI_MODEL: Model name (default: gpt-4o-mini)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key (str, optional): OpenAI API key
            model (str, optional): Model name to use
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package is required for OpenAIProvider. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAIProvider")
        
        self.model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key)
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate response using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a test automation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            return None


class AnthropicProvider(ModelProvider):
    """
    Anthropic (Claude) provider.
    
    Uses Anthropic's API for healing suggestions.
    
    Environment Variables:
        ANTHROPIC_API_KEY: API key for Anthropic
        ANTHROPIC_MODEL: Model name (default: claude-3-5-sonnet-20241022)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key (str, optional): Anthropic API key
            model (str, optional): Model name to use
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package is required for AnthropicProvider. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for AnthropicProvider")
        
        self.model_name = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.client = Anthropic(api_key=self.api_key)
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate response using Anthropic Claude."""
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Anthropic generation failed: {e}")
            return None


class AzureOpenAIProvider(ModelProvider):
    """
    Azure OpenAI provider.
    
    Uses Azure's OpenAI deployment for healing suggestions.
    
    Environment Variables:
        AZURE_OPENAI_API_KEY: API key for Azure OpenAI
        AZURE_OPENAI_ENDPOINT: Endpoint URL (e.g. https://my-resource.openai.azure.com/)
        AZURE_OPENAI_API_VERSION: API version (default: 2024-02-15-preview)
        AZURE_OPENAI_DEPLOYMENT: Deployment name (model)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, endpoint: Optional[str] = None):
        """
        Initialize Azure OpenAI provider.
        
        Args:
            api_key (str, optional): Azure API key
            model (str, optional): Deployment name
            endpoint (str, optional): Azure endpoint URL
        """
        try:
            from openai import AzureOpenAI
        except ImportError:
            raise ImportError("openai package is required for AzureOpenAIProvider. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if not self.api_key or not self.endpoint:
            raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are required for AzureOpenAIProvider")
        
        self.deployment_name = model or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate response using Azure OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a test automation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Azure OpenAI generation failed: {e}")
            return None


class OllamaProvider(ModelProvider):
    """
    Ollama (Local LLM) provider.
    
    Uses local Ollama instance for healing suggestions.
    
    Environment Variables:
        OLLAMA_BASE_URL: Base URL for Ollama (default: http://localhost:11434)
        OLLAMA_MODEL: Model name (default: llama3)
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Ollama provider.
        
        Args:
            api_key (str, optional): Not used for Ollama, included for compatibility
            base_url (str, optional): Ollama base URL
            model (str, optional): Model name to use
        """
        try:
            import requests
        except ImportError:
            raise ImportError("requests package is required for OllamaProvider. Install with: pip install requests")
        
        # api_key is ignored for Ollama (local), but accepted for compatibility
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = model or os.getenv("OLLAMA_MODEL", "llama3")
        self.api_url = f"{self.base_url}/api/generate"
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate response using local Ollama."""
        import requests
        import json
        
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "system": "You are a test automation expert. Return ONLY the locator string."
            }
            
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            print(f"Ollama generation failed: {e}")
            print(f"Ensure Ollama is running at {self.base_url} and model '{self.model_name}' is pulled.")
            return None


def create_provider(provider_name: Optional[str] = None, api_key: Optional[str] = None, model: Optional[str] = None) -> ModelProvider:
    """
    Factory function to create the appropriate model provider.
    
    Args:
        provider_name (str, optional): Name of provider ('gemini', 'openai', 'anthropic', 'azure', 'ollama')
        api_key (str, optional): API key for the provider
        model (str, optional): Model name to use
    
    Returns:
        ModelProvider: Configured model provider instance
    
    Raises:
        ValueError: If provider_name is invalid or required API key is missing
    
    Example:
        >>> provider = create_provider("openai")
        >>> response = provider.generate("What is 2+2?")
    """
    provider_name = provider_name or os.getenv("AI_PROVIDER", "gemini")
    provider_name = provider_name.lower()
    
    providers = {
        "gemini": GeminiProvider,
        "google": GeminiProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "claude": AnthropicProvider,
        "azure": AzureOpenAIProvider,
        "azure_openai": AzureOpenAIProvider,
        "ollama": OllamaProvider,
        "local": OllamaProvider,
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}. Choose from: {', '.join(providers.keys())}")
    
    provider_class = providers[provider_name]
    
    # Handle specific init signatures if needed, but mostly they take api_key and model
    # Ollama doesn't need api_key but accepts it (ignored) to match signature
    return provider_class(api_key=api_key, model=model)
