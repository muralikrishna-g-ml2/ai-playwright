# AI Provider Benchmark Results

**Test Date:** November 23, 2025  
**Framework Version:** 0.1.0  
**Test Scenario:** Self-healing locator on example.com

## Executive Summary

Comprehensive benchmark testing of AI providers for test healing capabilities. Tests measure the time taken to detect a broken locator, analyze the page, and suggest a working alternative.

## Test Results

| Provider | Model | Status | Total Time | Healing Time | Success |
|----------|-------|--------|------------|--------------|---------|
| **Google Gemini** | gemini-2.0-flash-lite | ✅ PASS | 36.22s | 32.64s | ✅ |
| **OpenAI ChatGPT** | gpt-4o-mini | ✅ PASS | 34.21s | 32.62s | ✅ |
| **Anthropic Claude** | claude-3-5-sonnet | ⏭️ SKIP | - | - | Not tested |
| **Azure OpenAI** | - | ⏭️ SKIP | - | - | Not configured |
| **Ollama (Local)** | llama3 | ⏭️ SKIP | - | - | Not running |

## Performance Metrics

### Speed Comparison

```
🥇 Fastest: OpenAI (gpt-4o-mini) - 34.21s
🥈 Second: Google Gemini - 36.22s

Average Total Time: 35.22s
Average Healing Time: 32.63s
```

### Success Rate

- **Total Tests:** 2 (configured providers)
- **Passed:** 2
- **Failed:** 0
- **Success Rate:** 100%

## Detailed Analysis

### Google Gemini
- **Model:** `gemini-2.0-flash-lite-preview-02-05`
- **Total Time:** 36.22s
- **Healing Time:** 32.64s
- **Overhead:** 3.58s (page load + retry)
- **Healed Locator:** `a[href="https://iana.org/domains/example"]`
- **Quality:** ✅ Excellent - Precise CSS selector

**Pros:**
- Free tier available
- Fast response
- Accurate healing
- Easy setup

**Cons:**
- Slightly slower than OpenAI
- Requires internet connection

### OpenAI ChatGPT
- **Model:** `gpt-4o-mini`
- **Total Time:** 34.21s
- **Healing Time:** 32.62s
- **Overhead:** 1.59s (page load + retry)
- **Healed Locator:** `a[href="https://iana.org/domains/example"]`
- **Quality:** ✅ Excellent - Precise CSS selector

**Pros:**
- Fastest provider tested
- Highly accurate
- Reliable API
- Multiple model options

**Cons:**
- Pay-per-use pricing
- Requires API key

## Cost Analysis

### Per-Healing Cost Estimates

| Provider | Model | Est. Cost/Healing | Notes |
|----------|-------|-------------------|-------|
| **Gemini** | flash-lite | ~$0.0001 | Free tier: 15 RPM |
| **OpenAI** | gpt-4o-mini | ~$0.0015 | Input: ~500 tokens, Output: ~50 tokens |
| **Anthropic** | claude-3-5-sonnet | ~$0.0030 | Input: ~500 tokens, Output: ~50 tokens |
| **Azure** | gpt-4 | ~$0.0060 | Varies by deployment |
| **Ollama** | llama3 | $0.0000 | Free (local) |

*Estimates based on current pricing and average token usage*

## Recommendations

### For Development/Testing
**Recommended:** Google Gemini
- Free tier sufficient for most dev work
- Fast enough for quick iterations
- Easy setup

### For CI/CD
**Recommended:** OpenAI (gpt-4o-mini)
- Fastest response time
- Highly reliable
- Predictable costs

### For Enterprise
**Recommended:** Azure OpenAI
- Enterprise SLA
- Data residency options
- Integration with Azure ecosystem

### For Privacy/Offline
**Recommended:** Ollama
- Completely offline
- No data leaves your network
- Free to use
- Slower but acceptable for security-critical scenarios

## Test Methodology

### Test Scenario
1. Navigate to https://example.com
2. Attempt to click link with text "More information" using `get_by_role()`
3. Locator fails (intentionally broken)
4. AI analyzes page HTML
5. AI suggests alternative locator
6. Framework retries with new locator
7. Verify navigation success

### Metrics Collected
- **Total Time:** End-to-end test execution
- **Healing Time:** Time spent in AI analysis
- **Overhead:** Page load + retry time
- **Success:** Whether healing worked
- **Locator Quality:** Accuracy of suggested locator

## Healing Quality

Both providers suggested identical, high-quality locators:

**Original (Broken):** `get_by_role("link", name="More information")`  
**Healed (Working):** `a[href="https://iana.org/domains/example"]`

### Quality Assessment: ✅ Excellent

- **Specificity:** High - Uses exact href match
- **Reliability:** High - Unlikely to break
- **Maintainability:** Good - Clear intent
- **Performance:** Excellent - Direct CSS selector

## Conclusion

Both tested providers (Gemini and OpenAI) demonstrate excellent healing capabilities with:
- 100% success rate
- Sub-40 second healing time
- High-quality locator suggestions
- Reliable performance

**Winner:** OpenAI (gpt-4o-mini) by a narrow margin (2 seconds faster)

However, for most use cases, **Google Gemini** offers the best value with its free tier and comparable performance.

## Running Your Own Benchmarks

```bash
# Set up your API keys in .env
echo "GEMINI_API_KEY=your-key" >> .env
echo "OPENAI_API_KEY=your-key" >> .env

# Run benchmark
python benchmark_providers.py

# View results
cat benchmark_results.json
```

## Next Steps

1. Test with Anthropic Claude (requires API key)
2. Test with Azure OpenAI (requires deployment)
3. Test with Ollama (requires local setup)
4. Run benchmarks on more complex pages
5. Test with different locator types

---

*Benchmark conducted on: macOS, Python 3.13.2, Playwright 1.40+*  
*Results may vary based on network conditions and API response times*
