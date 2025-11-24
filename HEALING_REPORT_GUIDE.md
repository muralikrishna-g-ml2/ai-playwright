# Enhanced Healing Report Documentation

## Overview

The AI-Playwright framework now includes **comprehensive healing reports** that capture detailed information when tests fail and are automatically healed. These reports provide all the necessary context for an automated agent to fix the code without human intervention.

## What Gets Logged

When a test fails and the healing mechanism kicks in, the system automatically captures:

### 1. **Identification & Tracking**
- Unique healing ID (e.g., `HEAL-893D611E`)
- Timestamp of the healing event
- Severity level (`low`, `medium`, `high`, `critical`)
- Status (`healed`, `pending_fix`, `failed`)

### 2. **Test Information**
```json
"test_info": {
    "test_name": "test_healing_with_detailed_logging",
    "test_file": "test_healing_logger.py",
    "test_class": null,
    "test_method": "test_healing_with_detailed_logging",
    "line_number": null
}
```

### 3. **Error Details**
```json
"error_details": {
    "error_type": "TimeoutError",
    "error_message": "Locator.click: Timeout 30000ms exceeded...",
    "stack_trace": "Full stack trace...",
    "failure_count": 1,
    "last_success": null,
    "action_attempted": "click"
}
```

### 4. **Locator Analysis**
```json
"locator_issue": {
    "original_locator": "get_by_role('link', ...)",
    "original_locator_type": "role_based",
    "failed_reason": "Element not found or not visible within timeout period",
    "suggested_locator": "a[href=\"https://iana.org/domains/example\"]",
    "suggested_locator_type": "attribute_selector",
    "confidence_score": 0.85,
    "alternative_locators": []
}
```

### 5. **Code Context**
```json
"code_context": {
    "file_path": "test_healing_logger.py",
    "function_name": "test_healing_with_detailed_logging",
    "problematic_line": "page.get_by_role('link', ...)",
    "code_snippet_before": "",
    "code_snippet_after": "",
    "line_start": null,
    "line_end": null
}
```

### 6. **Root Cause Analysis**
```json
"root_cause_analysis": {
    "primary_cause": "Dynamic content loading - element text or role may be rendered differently or delayed",
    "contributing_factors": [
        "Role Based locator may be too specific for dynamic content",
        "Possible timing issue with page rendering",
        "Element might load conditionally or asynchronously"
    ],
    "environmental_factors": {
        "browser": "chromium",
        "viewport": "{'width': 1280, 'height': 720}",
        "network_conditions": "normal"
    }
}
```

### 7. **Suggested Fixes**
```json
"suggested_fix": {
    "fix_type": "locator_replacement",
    "priority": "high",
    "code_changes": [
        {
            "file": "test_healing_logger.py",
            "line_number": null,
            "original_code": "page.get_by_role('link', ...)",
            "fixed_code": "page.locator('a[href=\"https://iana.org/domains/example\"]')",
            "change_type": "replace"
        }
    ],
    "alternative_fixes": [
        {
            "description": "Add explicit wait before interacting with element",
            "code": "page.wait_for_selector('a[href=\"...\"]', state='visible')\npage.locator('a[href=\"...\"]').click()"
        }
    ],
    "validation_steps": [
        "Run the test 5 times to ensure stability",
        "Verify the locator works across different browsers",
        "Check if the fix handles edge cases (slow network, delayed rendering)"
    ]
}
```

### 8. **AI Recommendations**
```json
"ai_recommendations": {
    "best_practice": "Attribute selectors are stable when targeting unchanging attributes like href or data-*",
    "preventive_measures": [
        "Add explicit waits for dynamic content",
        "Use multiple fallback locators",
        "Implement retry logic for flaky elements"
    ],
    "test_improvement": "Consider adding a custom fixture that waits for critical page elements before proceeding"
}
```

### 9. **Metadata**
```json
"metadata": {
    "healer_agent": "HealerAgent-v1.0",
    "healing_strategy": "locator_analysis_and_replacement",
    "auto_fix_eligible": true,
    "requires_human_review": false,
    "estimated_fix_time_seconds": 15,
    "related_issues": [],
    "tags": ["timeout_error", "role_based", "action_click", "timing_issue", "dynamic_content"]
}
```

## How It Works

### Automatic Logging
When a test fails:

1. **Failure Detection**: The `AIElementHandle` detects a `TimeoutError`
2. **Healing Attempt**: The `HealerAgent` analyzes the page and suggests a new locator
3. **Context Capture**: The system captures:
   - Browser and viewport information
   - Page content (truncated to 5000 chars)
   - Action being performed
   - Full error message and stack trace
4. **Comprehensive Logging**: All details are written to `healing_report.json`
5. **Retry**: The healed locator is used to retry the action

### Code Location
- **Logger**: `ai_playwright/utils/logger.py` - `ChangeLogger` class
- **Wrapper**: `ai_playwright/core/wrapper.py` - `AIElementHandle._perform_action()` method
- **Healer**: `ai_playwright/core/healer.py` - `HealerAgent.heal()` method

## Using the Healing Report

### For Automated Agents
An automated healing agent can:

1. **Parse the JSON**: Read `healing_report.json`
2. **Identify Issues**: Filter by `status: "healed"` or `auto_fix_eligible: true`
3. **Apply Fixes**: Use the `suggested_fix.code_changes` to update test files
4. **Validate**: Run the validation steps to ensure the fix works
5. **Learn**: Use the root cause analysis to prevent similar issues

### Example Agent Workflow
```python
import json

# Read healing report
with open('healing_report.json', 'r') as f:
    healing_data = json.load(f)

# Process each healing event
for entry in healing_data:
    if entry.get('auto_fix_eligible') and entry.get('status') == 'healed':
        # Extract fix information
        file_path = entry['code_context']['file_path']
        original_code = entry['suggested_fix']['code_changes'][0]['original_code']
        fixed_code = entry['suggested_fix']['code_changes'][0]['fixed_code']
        
        # Apply fix to file
        # ... (implement file modification logic)
        
        # Validate fix
        # ... (run validation steps)
```

## Locator Type Detection

The system automatically detects and categorizes locator types:

| Locator Type | Example | Detection Pattern |
|-------------|---------|-------------------|
| `role_based` | `get_by_role('button', ...)` | Starts with `get_by_role` |
| `text_based` | `get_by_text('Submit')` | Starts with `get_by_text` |
| `id_selector` | `#submit-btn` | Starts with `#` |
| `class_selector` | `.btn-primary` | Starts with `.` |
| `attribute_selector` | `a[href="..."]` | Contains `[` and `]` |
| `xpath` | `//button[@id='submit']` | Starts with `//` |
| `css_selector` | `button.submit` | Default for other CSS |

## Severity Levels

Severity is automatically determined:

- **Critical**: Multiple failures (failure_count > 2)
- **High**: Timeout errors
- **Medium**: Other errors
- **Low**: Minor issues

## Best Practices

### For Test Writers
1. **Review Reports Regularly**: Check `healing_report.json` for patterns
2. **Update Tests**: Apply suggested fixes to make tests more stable
3. **Use Stable Locators**: Follow the AI recommendations for better locators

### For Automation Engineers
1. **Monitor Healing Events**: Track which tests are being healed frequently
2. **Implement Fixes**: Use the comprehensive data to permanently fix flaky tests
3. **Analyze Root Causes**: Use the root cause analysis to improve test design

### For AI Agents
1. **Parse Structured Data**: The JSON format is designed for easy parsing
2. **Confidence Scores**: Use confidence scores to prioritize fixes
3. **Validation Steps**: Always run validation steps after applying fixes
4. **Learn from Patterns**: Use tags and root cause analysis to prevent similar issues

## Configuration

### Custom Log File Location
```python
from ai_playwright import AIPage
from ai_playwright.utils.logger import ChangeLogger

# Use custom log file
page.logger = ChangeLogger("custom_healing_report.json")
```

### Extending the Logger
You can extend the `ChangeLogger` class to add custom analysis:

```python
from ai_playwright.utils.logger import ChangeLogger

class CustomLogger(ChangeLogger):
    def _analyze_root_cause(self, original_locator, new_locator, error_message):
        # Add custom root cause analysis
        cause = super()._analyze_root_cause(original_locator, new_locator, error_message)
        # Add your custom logic
        return cause
```

## Example Output

See `healing_report.json` for a complete example of the enhanced logging output.

## Future Enhancements

Planned improvements:
- [ ] Capture actual line numbers from source code
- [ ] Track failure count across multiple test runs
- [ ] Add screenshot/video capture on failure
- [ ] Implement confidence score from AI model
- [ ] Add support for multiple alternative locators from AI
- [ ] Integrate with CI/CD for automatic fix suggestions
- [ ] Add machine learning to predict likely failures

## Troubleshooting

### Empty healing_report.json
- Ensure tests are actually failing and being healed
- Check that the `AIPage` wrapper is being used
- Verify file permissions for writing

### Missing Details
- Some fields (like line_number) require additional instrumentation
- Stack traces may be limited based on error type
- Alternative locators require AI provider configuration

## Contributing

To enhance the healing report:
1. Modify `ai_playwright/utils/logger.py` for new fields
2. Update `ai_playwright/core/wrapper.py` to capture additional context
3. Add helper methods for new analysis types
4. Update this documentation

---

**Version**: 1.0  
**Last Updated**: 2025-11-23  
**Maintainer**: AI-Playwright Team
