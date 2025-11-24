"""
Example test using Google Gemini (default provider)
"""
import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage


@pytest.fixture(scope="function")
def ai_page():
    """Fixture using default Gemini provider"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield AIPage(page)
        browser.close()


def test_example_with_gemini(ai_page):
    """
    Example test that will use AI healing with Gemini.
    
    Prerequisites:
    - Set GEMINI_API_KEY in .env file
    - Run: pytest examples/test_gemini_example.py -v
    """
    # Navigate to a page
    ai_page.goto("https://example.com")
    
    # Use semantic locators - they will auto-heal if they break
    ai_page.get_by_role("link", name="More information").click()
    
    # Verify navigation
    assert "iana" in ai_page.url.lower()
