"""
Examples for using different AI providers with the AI-enhanced Playwright framework.

This file demonstrates how to configure and use each supported AI provider.
"""

# ============================================================================
# Example 1: Using Google Gemini (Default)
# ============================================================================

# .env file:
# AI_PROVIDER=gemini
# GEMINI_API_KEY=your-gemini-api-key

# conftest.py
import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage

@pytest.fixture(scope="function")
def ai_page_gemini():
    """Default Gemini provider - no extra config needed"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield AIPage(page)  # Uses Gemini by default
        browser.close()


# ============================================================================
# Example 2: Using OpenAI ChatGPT
# ============================================================================

# .env file:
# AI_PROVIDER=openai
# OPENAI_API_KEY=sk-proj-...
# OPENAI_MODEL=gpt-4o-mini

# conftest.py
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent

@pytest.fixture(scope="function")
def ai_page_openai():
    """Using OpenAI ChatGPT"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        # Explicitly set OpenAI provider
        ai_page.healer = HealerAgent(provider="openai", model="gpt-4o-mini")
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 3: Using Anthropic Claude
# ============================================================================

# .env file:
# AI_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# conftest.py
@pytest.fixture(scope="function")
def ai_page_claude():
    """Using Anthropic Claude"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        ai_page.healer = HealerAgent(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022"
        )
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 4: Using Grok (xAI)
# ============================================================================

# .env file:
# AI_PROVIDER=grok
# GROK_API_KEY=your-grok-key

# conftest.py
@pytest.fixture(scope="function")
def ai_page_grok():
    """Using Grok from xAI"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        ai_page.healer = HealerAgent(provider="grok")
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 5: Using Azure OpenAI
# ============================================================================

# .env file:
# AI_PROVIDER=azure
# AZURE_OPENAI_API_KEY=your-azure-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT=gpt-4
# AZURE_OPENAI_API_VERSION=2024-02-15-preview

# conftest.py
@pytest.fixture(scope="function")
def ai_page_azure():
    """Using Azure OpenAI"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        ai_page.healer = HealerAgent(provider="azure")
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 6: Using Ollama (Local LLM)
# ============================================================================

# Prerequisites:
# 1. Install Ollama: https://ollama.com/
# 2. Pull a model: ollama pull llama3
# 3. Start Ollama: ollama serve

# .env file:
# AI_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3

# conftest.py
@pytest.fixture(scope="function")
def ai_page_ollama():
    """Using local Ollama"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        ai_page.healer = HealerAgent(provider="ollama", model="llama3")
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 7: Dynamic Provider Selection
# ============================================================================

import os

@pytest.fixture(scope="function")
def ai_page_dynamic():
    """Dynamically select provider based on environment"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        
        # Provider is automatically selected from AI_PROVIDER env var
        # No need to explicitly set healer if using env vars
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 8: Custom Provider Instance
# ============================================================================

from ai_playwright.core.model_providers import OpenAIProvider, OllamaProvider

@pytest.fixture(scope="function")
def ai_page_custom():
    """Using custom provider instance with specific settings"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Create custom provider with specific configuration
        custom_provider = OpenAIProvider(
            api_key="your-specific-key",
            model="gpt-4o"
        )
        
        ai_page = AIPage(page)
        ai_page.healer = HealerAgent(provider=custom_provider)
        
        yield ai_page
        browser.close()


# ============================================================================
# Example 9: Multiple Providers in Same Test Suite
# ============================================================================

# You can have different fixtures for different test files
# tests/test_with_gemini.py uses ai_page_gemini
# tests/test_with_openai.py uses ai_page_openai
# tests/test_with_ollama.py uses ai_page_ollama

# test_login.py
def test_login_with_gemini(ai_page_gemini):
    """Test using Gemini"""
    ai_page_gemini.goto("https://example.com/login")
    ai_page_gemini.get_by_label("Email").fill("user@example.com")
    ai_page_gemini.get_by_role("button", name="Sign In").click()

def test_login_with_openai(ai_page_openai):
    """Test using OpenAI"""
    ai_page_openai.goto("https://example.com/login")
    ai_page_openai.get_by_label("Email").fill("user@example.com")
    ai_page_openai.get_by_role("button", name="Sign In").click()

def test_login_with_ollama(ai_page_ollama):
    """Test using local Ollama - no API costs!"""
    ai_page_ollama.goto("https://example.com/login")
    ai_page_ollama.get_by_label("Email").fill("user@example.com")
    ai_page_ollama.get_by_role("button", name="Sign In").click()


# ============================================================================
# Example 10: Fallback Strategy
# ============================================================================

@pytest.fixture(scope="function")
def ai_page_with_fallback():
    """Try primary provider, fallback to secondary"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page = AIPage(page)
        
        # Try to use OpenAI, fallback to Gemini if not available
        try:
            ai_page.healer = HealerAgent(provider="openai")
        except ValueError:
            print("OpenAI not configured, falling back to Gemini")
            ai_page.healer = HealerAgent(provider="gemini")
        
        yield ai_page
        browser.close()
