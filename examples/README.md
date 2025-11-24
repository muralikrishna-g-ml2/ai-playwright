# AI Provider Examples

This directory contains working examples for each supported AI provider.

## Quick Start

### 1. Choose an Example

- **`test_gemini_example.py`** - Google Gemini (default, fastest setup)
- **`test_openai_example.py`** - OpenAI ChatGPT (GPT-4o-mini)
- **`test_ollama_example.py`** - Ollama (local, offline, free)
- **`provider_examples.py`** - All providers with detailed configurations

### 2. Set Up Your Provider

#### Google Gemini (Recommended for beginners)
```bash
# Get API key from: https://makersuite.google.com/app/apikey
echo "GEMINI_API_KEY=your-key-here" > .env
pytest examples/test_gemini_example.py -v
```

#### OpenAI ChatGPT
```bash
# Get API key from: https://platform.openai.com/api-keys
pip install ai-playwright[openai]
echo "OPENAI_API_KEY=your-key-here" > .env
pytest examples/test_openai_example.py -v
```

#### Ollama (Local, Free)
```bash
# Install Ollama
brew install ollama  # macOS
# or download from https://ollama.com/

# Pull and start model
ollama pull llama3
ollama serve  # Keep this running

# Run test
pip install ai-playwright[ollama]
pytest examples/test_ollama_example.py -v
```

## Example Configurations

### Environment-Based (Recommended)

Create a `.env` file:

```bash
# Choose your provider
AI_PROVIDER=gemini  # or openai, anthropic, grok, azure, ollama

# Add corresponding API key
GEMINI_API_KEY=your-gemini-key
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-anthropic-key
```

Then use the default fixture:
```python
@pytest.fixture
def ai_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield AIPage(page)  # Automatically uses AI_PROVIDER
        browser.close()
```

### Programmatic Configuration

```python
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent

# Explicitly set provider
ai_page = AIPage(page)
ai_page.healer = HealerAgent(provider="openai", model="gpt-4o-mini")
```

## All Supported Providers

| Provider | Setup Difficulty | Cost | Speed | Best For |
|----------|-----------------|------|-------|----------|
| **Gemini** | ⭐ Easy | 💰 Free tier | ⚡⚡⚡ Fast | Getting started |
| **OpenAI** | ⭐ Easy | 💰💰 Pay-per-use | ⚡⚡ Medium | Production |
| **Ollama** | ⭐⭐ Medium | 💰 Free | ⚡ Slower | Offline/Privacy |
| **Anthropic** | ⭐ Easy | 💰💰 Pay-per-use | ⚡⚡ Medium | High accuracy |
| **Azure** | ⭐⭐⭐ Complex | 💰💰💰 Enterprise | ⚡⚡ Medium | Enterprise |
| **Grok** | ⭐ Easy | 💰💰 Pay-per-use | ⚡⚡ Medium | Alternative |

## Running Examples

```bash
# Run specific example
pytest examples/test_gemini_example.py -v

# Run all examples (requires all providers configured)
pytest examples/ -v

# Run with output
pytest examples/test_ollama_example.py -v -s
```

## Troubleshooting

### "API key not found"
- Check your `.env` file is in the project root
- Verify the key name matches the provider (e.g., `GEMINI_API_KEY`)

### "Provider not found"
- Install provider dependencies: `pip install ai-playwright[openai]`

### "Ollama connection failed"
- Ensure Ollama is running: `ollama serve`
- Check the URL: `OLLAMA_BASE_URL=http://localhost:11434`
- Verify model is pulled: `ollama list`

## More Information

- **Full Guide**: See `../AI_PROVIDER_GUIDE.md`
- **All Configurations**: See `provider_examples.py`
- **Documentation**: See `../README.md`
