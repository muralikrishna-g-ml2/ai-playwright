"""
Example test using Ollama (Local LLM)
"""
import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent


@pytest.fixture(scope="function")
def ai_page():
    """Fixture using local Ollama provider"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        # Configure to use local Ollama
        ai_page.healer = HealerAgent(provider="ollama", model="llama3")
        
        yield ai_page
        browser.close()


def test_example_with_ollama(ai_page):
    """
    Example test that will use AI healing with local Ollama.
    
    Prerequisites:
    1. Install Ollama: https://ollama.com/
    2. Pull model: ollama pull llama3
    3. Start Ollama: ollama serve
    4. Install: pip install ai-playwright[ollama]
    5. Run: pytest examples/test_ollama_example.py -v
    
    Benefits:
    - Completely offline
    - No API costs
    - Privacy - data stays local
    """
    # Navigate to a page
    ai_page.goto("https://example.com")
    
    # Use semantic locators - they will auto-heal if they break
    ai_page.get_by_role("link", name="More information").click()
    
    # Verify navigation
    assert "iana" in ai_page.url.lower()
