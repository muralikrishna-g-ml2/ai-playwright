# AI-Enhanced Playwright Framework

A self-healing test automation framework that uses Google Gemini AI to automatically fix broken locators in Playwright tests.

## Features

- 🤖 **AI-Powered Self-Healing**: Automatically fixes broken locators using Google Gemini AI
- 🎯 **Full Playwright API Support**: All locator methods (get_by_role, get_by_label, etc.)
- 📝 **Automatic Change Logging**: Documents all healing actions for code updates
- 🔗 **Locator Chaining**: Supports filter, and_, or_, first, last, nth operations
- 🚀 **Easy Integration**: Drop-in replacement for standard Playwright

## Installation

```bash
pip install ai-playwright
```

### Prerequisites

1. Install Playwright browsers:
```bash
playwright install
```

2. Set up your Google Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

Get your API key from: https://makersuite.google.com/app/apikey

## Quick Start

### 1. Create a conftest.py

```python
import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage

@pytest.fixture(scope="function")
def ai_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield AIPage(page)
        browser.close()
```

### 2. Write Your Tests

```python
def test_login(ai_page):
    ai_page.goto("https://example.com/login")
    
    # Use any Playwright locator method - they all support self-healing!
    ai_page.get_by_label("Email").fill("user@example.com")
    ai_page.get_by_label("Password").fill("password123")
    ai_page.get_by_role("button", name="Sign In").click()
    
    # If locators break, AI will automatically fix them
    assert ai_page.get_by_text("Welcome").is_visible()
```

### 3. Run Your Tests

```bash
pytest tests/
```

## Supported Locator Methods

All Playwright locator methods are supported with self-healing:

### Semantic Locators (Recommended)
- `get_by_role(role, name=...)` - Locate by ARIA role
- `get_by_label(text)` - Locate form controls by label
- `get_by_placeholder(text)` - Locate inputs by placeholder
- `get_by_text(text)` - Locate by text content
- `get_by_alt_text(text)` - Locate images by alt text
- `get_by_title(text)` - Locate by title attribute
- `get_by_test_id(test_id)` - Locate by data-testid

### CSS/XPath Locators
- `locator(selector)` - CSS or XPath selector

### Chaining Methods
- `filter(has_text=..., has=...)` - Filter locators
- `and_(locator)` - Intersection of locators
- `or_(locator)` - Union of locators
- `first`, `last`, `nth(index)` - List operations

## How It Works

1. **Test Runs**: Your test executes normally using Playwright
2. **Failure Detected**: When a locator fails (TimeoutError), the framework captures the page state
3. **AI Analysis**: Google Gemini AI analyzes the HTML and suggests alternative locators
4. **Auto-Healing**: The test retries with the new locator
5. **Logging**: Changes are logged to `healing_report.json` for review

## Healing Report

All healing actions are logged to `healing_report.json`:

```json
[
    {
        "timestamp": "2025-11-23T15:38:04.953400",
        "test_name": "tests/test_login.py::test_user_login",
        "original_locator": "#submit-btn",
        "new_locator": "#continue-btn",
        "error_message": "Locator.click: Timeout 2000ms exceeded..."
    }
]
```

Use this report to update your test code with the corrected locators.

## Advanced Usage

### Custom Healing Logic

```python
from ai_playwright import HealerAgent, AIPage

# Use custom API key
healer = HealerAgent(api_key="your-custom-key")
ai_page = AIPage(page)
ai_page.healer = healer
```

### Custom Logging

```python
from ai_playwright import ChangeLogger

logger = ChangeLogger(log_file="custom_healing.json")
ai_page.logger = logger
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY` - Your Google Gemini API key (required)

### Playwright Configuration

The framework works with standard Playwright configuration. Set timeouts as needed:

```python
ai_page.set_default_timeout(5000)  # 5 seconds
```

## Best Practices

1. **Use Semantic Locators**: Prefer `get_by_role`, `get_by_label` over CSS selectors
2. **Review Healing Reports**: Regularly check `healing_report.json` and update tests
3. **Set Appropriate Timeouts**: Balance between test speed and healing accuracy
4. **Keep API Key Secure**: Use environment variables, never commit to version control

## Limitations

- Requires active internet connection for AI healing
- API rate limits apply (Google Gemini free tier)
- Healing works best with well-structured HTML

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/ai-playwright/issues
- Documentation: https://github.com/yourusername/ai-playwright/wiki
