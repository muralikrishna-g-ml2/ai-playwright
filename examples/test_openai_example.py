"""
Example test using OpenAI ChatGPT
"""
import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent


@pytest.fixture(scope="function")
def ai_page():
    """Fixture using OpenAI provider"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        # Configure to use OpenAI
        ai_page.healer = HealerAgent(provider="openai", model="gpt-4o-mini")
        
        yield ai_page
        browser.close()


def test_example_with_openai(ai_page):
    """
    Example test that will use AI healing with OpenAI ChatGPT.
    
    Prerequisites:
    - Install: pip install ai-playwright[openai]
    - Set OPENAI_API_KEY in .env file
    - Run: pytest examples/test_openai_example.py -v
    """
    # Navigate to a page
    ai_page.goto("https://example.com")
    
    # Use semantic locators - they will auto-heal if they break
    ai_page.get_by_role("link", name="More information").click()
    
    # Verify navigation
    assert "iana" in ai_page.url.lower()
