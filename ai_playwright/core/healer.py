import os
from dotenv import load_dotenv
from .model_providers import create_provider, ModelProvider
from typing import Optional

load_dotenv()

class HealerAgent:
    """
    AI-powered test healing agent using configurable AI models.
    
    This class uses various AI providers (Gemini, OpenAI, Anthropic, Grok) to analyze 
    failed test locators and suggest alternative locators that can successfully locate 
    the intended element.
    
    Attributes:
        provider (ModelProvider): The AI model provider instance
    
    Raises:
        ValueError: If required API key for the selected provider is not set
    
    Example:
        >>> # Use default provider (Gemini)
        >>> healer = HealerAgent()
        
        >>> # Use specific provider
        >>> healer = HealerAgent(provider="openai")
        
        >>> # Use custom provider instance
        >>> from ai_playwright.core.model_providers import OpenAIProvider
        >>> custom_provider = OpenAIProvider(api_key="key", model="gpt-4")
        >>> healer = HealerAgent(provider=custom_provider)
    """
    
    def __init__(self, provider: Optional[str | ModelProvider] = None, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the HealerAgent with an AI model provider.
        
        Args:
            provider (str | ModelProvider, optional): Provider name ('gemini', 'openai', 'anthropic', 'grok')
                or a ModelProvider instance. If None, uses AI_PROVIDER env var or defaults to 'gemini'.
            api_key (str, optional): API key for the provider. If not provided,
                will attempt to read from environment variables.
            model (str, optional): Model name to use. If not provided, uses provider's default.
        
        Raises:
            ValueError: If no API key is found for the selected provider
        
        Examples:
            >>> # Use Gemini (default)
            >>> healer = HealerAgent()
            
            >>> # Use OpenAI ChatGPT
            >>> healer = HealerAgent(provider="openai")
            
            >>> # Use Anthropic Claude with specific model
            >>> healer = HealerAgent(provider="anthropic", model="claude-3-opus-20240229")
            
            >>> # Use custom provider instance
            >>> from ai_playwright.core.model_providers import GrokProvider
            >>> grok = GrokProvider(api_key="your-key")
            >>> healer = HealerAgent(provider=grok)
        """
        # If provider is already a ModelProvider instance, use it directly
        if isinstance(provider, ModelProvider):
            self.provider = provider
        else:
            # Create provider using factory
            self.provider = create_provider(provider_name=provider, api_key=api_key, model=model)

    def heal(self, page_content: str, failed_locator: str, error_message: str) -> Optional[str]:
        """
        Analyze a failed locator and suggest an alternative.
        
        Uses the configured AI provider to analyze the page HTML and suggest a new locator
        that can successfully locate the intended element.
        
        Args:
            page_content (str): HTML content of the page where the locator failed
            failed_locator (str): The locator that failed (e.g., "#submit-btn" or "get_by_role('button', ...)")
            error_message (str): The error message from the failed locator attempt
        
        Returns:
            str or None: A new locator string to try, "ELEMENT_MISSING" if no alternative found,
                or None if the AI request fails
        
        Example:
            >>> healer = HealerAgent()
            >>> html = '<button id="continue-btn">Continue</button>'
            >>> new_loc = healer.heal(html, "#submit-btn", "Timeout exceeded")
            >>> print(new_loc)  # "#continue-btn"
        """
        prompt = f"""
        You are a Test Automation Expert. A Playwright test failed because an element was not found.
        
        Original Locator: `{failed_locator}`
        Error Message: `{error_message}`
        
        Here is the HTML content of the page (truncated if too large):
        ```html
        {page_content[:20000]} 
        ```
        
        Analyze the HTML and suggest a NEW locator that can find the element.
        
        CRITICAL RULES:
        1. Return ONLY a CSS selector or XPath expression
        2. DO NOT return Playwright method names like "get_by_text()" or "get_by_role()"
        3. Look for elements with similar IDs, classes, or text content
        4. If the ID changed (e.g. 'submit-btn' -> 'continue-btn'), return the new ID selector like "#continue-btn"
        5. If you need to match by text, use CSS like: a:has-text("More information") or a[href*="domain"]
        6. Only return "ELEMENT_MISSING" if there is absolutely no interactive element that could be the target
        
        EXAMPLES OF VALID RESPONSES:
        - #continue-btn
        - button.submit
        - a[href="https://iana.org/domains/example"]
        - //button[contains(text(), 'Submit')]
        
        EXAMPLES OF INVALID RESPONSES (DO NOT USE):
        - get_by_text('Learn more')
        - get_by_role('button', name='Submit')
        - page.locator('#btn')
        
        Return ONLY the CSS selector or XPath. No explanations, no code, no markdown.
        """
        
        try:
            response = self.provider.generate(prompt)
            if not response:
                return None
            
            new_locator = response.strip()
            # Remove backticks if present
            if new_locator.startswith("`") and new_locator.endswith("`"):
                new_locator = new_locator[1:-1]
            
            # Validate that it's not a Playwright method
            if "get_by_" in new_locator or "locator(" in new_locator:
                print(f"Warning: AI returned invalid locator format: {new_locator}")
                return None
            
            return new_locator
        except Exception as e:
            print(f"Healer Agent failed: {e}")
            return None
