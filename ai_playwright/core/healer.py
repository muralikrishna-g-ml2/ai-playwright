import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class HealerAgent:
    """
    AI-powered test healing agent using Google Gemini.
    
    This class uses Google's Gemini AI to analyze failed test locators and suggest
    alternative locators that can successfully locate the intended element.
    
    Attributes:
        api_key (str): Google Gemini API key
        model: Configured Gemini generative model instance
    
    Raises:
        ValueError: If GOOGLE_API_KEY or GEMINI_API_KEY environment variable is not set
    
    Example:
        >>> healer = HealerAgent()
        >>> new_locator = healer.heal(page_html, "#old-button", "TimeoutError")
        >>> print(new_locator)  # "#new-button"
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the HealerAgent with Google Gemini AI.
        
        Args:
            api_key (str, optional): Google Gemini API key. If not provided,
                will attempt to read from GOOGLE_API_KEY or GEMINI_API_KEY
                environment variables.
        
        Raises:
            ValueError: If no API key is found in parameters or environment
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable is required for HealerAgent")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')

    def heal(self, page_content, failed_locator, error_message):
        """
        Analyze a failed locator and suggest an alternative.
        
        Uses Google Gemini AI to analyze the page HTML and suggest a new locator
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
        
        Analyze the HTML and suggest a NEW, robust Playwright locator (CSS or XPath) that corresponds to the element intended by the original locator.
        
        RULES:
        1. Look for elements with similar IDs, classes, or text content.
        2. If the ID changed (e.g. 'submit-btn' -> 'continue-btn'), suggest the new ID.
        3. If the text is similar (e.g. 'Submit' -> 'Continue'), suggest the new element.
        4. Return ONLY the locator string.
        5. Only return "ELEMENT_MISSING" if there is absolutely no interactive element that could be the target.
        
        Return ONLY the new locator string. Do not add markdown formatting.
        """
        
        try:
            response = self.model.generate_content(prompt)
            new_locator = response.text.strip()
            # Remove backticks if present
            if new_locator.startswith("`") and new_locator.endswith("`"):
                new_locator = new_locator[1:-1]
            return new_locator
        except Exception as e:
            print(f"Healer Agent failed: {e}")
            return None
