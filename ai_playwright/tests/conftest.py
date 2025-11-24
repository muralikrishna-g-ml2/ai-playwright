import pytest
from playwright.sync_api import sync_playwright
from ai_playwright.core.wrapper import AIPage

@pytest.fixture(scope="function")
def ai_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield AIPage(page)
        browser.close()
