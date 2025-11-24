# AI Provider Configuration Guide

This guide explains how to configure different AI providers for the AI-enhanced Playwright framework.

## Supported Providers

- **Google Gemini** (default) - Fast and cost-effective
- **OpenAI ChatGPT** - GPT-4, GPT-3.5 Turbo
- **Anthropic Claude** - Claude 3 family
- **Grok** - xAI's Grok model

## Quick Start

### 1. Choose Your Provider

Set the `AI_PROVIDER` environment variable in your `.env` file:

```bash
AI_PROVIDER=gemini  # or openai, anthropic, grok
```

### 2. Set API Key

Add the corresponding API key for your chosen provider.

## Provider-Specific Configuration

### Google Gemini (Default)

**Get API Key:** https://makersuite.google.com/app/apikey

**.env Configuration:**
```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-lite-preview-02-05  # Optional
```

**Installation:**
```bash
pip install ai-playwright  # Gemini included by default
```

---

### OpenAI ChatGPT

**Get API Key:** https://platform.openai.com/api-keys

**.env Configuration:**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini  # Optional, default: gpt-4o-mini
```

**Available Models:**
- `gpt-4o` - Most capable, higher cost
- `gpt-4o-mini` - Balanced performance and cost (recommended)
- `gpt-4-turbo` - Previous generation
- `gpt-3.5-turbo` - Fastest, lowest cost

**Installation:**
```bash
pip install ai-playwright[openai]
```

---

### Anthropic Claude

**Get API Key:** https://console.anthropic.com/

**.env Configuration:**
```bash
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Optional
```

**Available Models:**
- `claude-3-5-sonnet-20241022` - Best balance (recommended)
- `claude-3-opus-20240229` - Most capable
- `claude-3-haiku-20240307` - Fastest, lowest cost

**Installation:**
```bash
pip install ai-playwright[anthropic]
```

---

### Grok (xAI)

**Get API Key:** https://x.ai/

**.env Configuration:**
```bash
AI_PROVIDER=grok
GROK_API_KEY=your-grok-api-key
GROK_MODEL=grok-beta  # Optional
```

**Installation:**
```bash
pip install ai-playwright[openai]  # Grok uses OpenAI-compatible API
```

---

### Azure OpenAI

**Get API Key:** From your Azure Portal

**.env Configuration:**
```bash
AI_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4  # Your deployment name
AZURE_OPENAI_API_VERSION=2024-02-15-preview  # Optional
```

**Installation:**
```bash
pip install ai-playwright[openai]
```

---

### Ollama (Local LLM)

**Setup:**
1. Download Ollama from https://ollama.com/
2. Run `ollama pull llama3` (or your preferred model)
3. Start Ollama: `ollama serve`

**.env Configuration:**
```bash
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434  # Default
OLLAMA_MODEL=llama3  # Default
```

**Installation:**
```bash
pip install ai-playwright[ollama]
```

---

## Programmatic Configuration

You can also configure the provider programmatically:

### Using Provider Name

```python
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent

# Create healer with specific provider
healer = HealerAgent(provider="openai")

# Use in AIPage
ai_page = AIPage(page)
ai_page.healer = healer
```

### Using Custom Provider Instance

```python
from ai_playwright.core.model_providers import OpenAIProvider, AnthropicProvider
from ai_playwright.core.healer import HealerAgent

# Create custom provider
provider = OpenAIProvider(api_key="your-key", model="gpt-4o")

# Use in healer
healer = HealerAgent(provider=provider)
```

### In conftest.py

```python
import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent

@pytest.fixture(scope="function")
def ai_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        ai_page_instance = AIPage(page)
        
        # Configure custom provider
        ai_page_instance.healer = HealerAgent(provider="openai", model="gpt-4o")
        
        yield ai_page_instance
        browser.close()
```

## Install All Providers

To install support for all providers:

```bash
pip install ai-playwright[all-providers]
```

## Cost Comparison

| Provider | Model | Speed | Cost | Recommended For |
|----------|-------|-------|------|-----------------|
| Gemini | gemini-2.0-flash-lite | ⚡⚡⚡ | 💰 | Default choice |
| OpenAI | gpt-4o-mini | ⚡⚡ | 💰💰 | Best balance |
| OpenAI | gpt-4o | ⚡ | 💰💰💰 | Complex healing |
| Anthropic | claude-3-haiku | ⚡⚡⚡ | 💰 | Fast healing |
| Anthropic | claude-3-5-sonnet | ⚡⚡ | 💰💰 | High accuracy |
| Grok | grok-beta | ⚡⚡ | 💰💰 | Alternative |

## Troubleshooting

### Provider Not Found Error
```
ValueError: Unknown provider: xyz
```
**Solution:** Check `AI_PROVIDER` value. Must be one of: `gemini`, `openai`, `anthropic`, `grok`

### Missing API Key Error
```
ValueError: OPENAI_API_KEY is required for OpenAIProvider
```
**Solution:** Set the appropriate API key in your `.env` file

### Import Error
```
ImportError: openai package is required for OpenAIProvider
```
**Solution:** Install the provider package:
```bash
pip install ai-playwright[openai]
```

## Best Practices

1. **Use Environment Variables**: Never hardcode API keys
2. **Start with Gemini**: It's included by default and cost-effective
3. **Test Locally**: Verify provider works before CI/CD
4. **Monitor Costs**: Set up billing alerts for your AI provider
5. **Rate Limits**: Be aware of provider rate limits in CI/CD

## Example .env Files

### Development (Gemini)
```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=AIza...
```

### CI/CD (OpenAI)
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

### Production (Claude)
```bash
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```
