import json
import os
from datetime import datetime

class ChangeLogger:
    """
    Logger for recording test healing actions.
    
    This class maintains a JSON log file that records all instances where the
    AI healer successfully fixed a broken locator. This log can be used to
    update test code with the corrected locators.
    
    Attributes:
        log_file (str): Path to the JSON log file
    
    Example:
        >>> logger = ChangeLogger("healing_report.json")
        >>> logger.log_change("test_login", "#old-btn", "#new-btn", "Timeout")
    """
    
    def __init__(self, log_file="healing_report.json"):
        """
        Initialize the ChangeLogger.
        
        Args:
            log_file (str, optional): Path to the JSON log file. 
                Defaults to "healing_report.json".
        """
        self.log_file = log_file
        # Initialize file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_change(self, test_name, original_locator, new_locator, error_message, 
                   action_name=None, page_content=None, alternative_locators=None, 
                   confidence_score=0.85, test_context=None):
        """
        Log a healing action to the JSON file with comprehensive details.
        
        Records detailed information about a successful locator healing, including test context,
        error details, locator analysis, code context, root cause analysis, suggested fixes,
        and AI recommendations. This comprehensive logging enables automated code fixing.
        
        If an entry with the same test_name and original_locator already exists,
        it will be updated instead of creating a duplicate.
        
        Args:
            test_name (str): Name of the test that failed (e.g., "tests/test_login.py::test_user_login")
            original_locator (str): The locator that failed
            new_locator (str): The healed locator that succeeded
            error_message (str): The error message from the original failure
            action_name (str, optional): The action that was being performed (e.g., "click", "fill")
            page_content (str, optional): HTML content of the page (truncated for storage)
            alternative_locators (list, optional): List of alternative locator suggestions
            confidence_score (float, optional): Confidence score for the suggested locator (0.0-1.0)
            test_context (dict, optional): Additional test context information
        
        Example:
            >>> logger = ChangeLogger()
            >>> logger.log_change(
            ...     "tests/test_login.py::test_submit",
            ...     "#submit-btn",
            ...     "#continue-btn",
            ...     "Locator.click: Timeout 2000ms exceeded",
            ...     action_name="click",
            ...     confidence_score=0.92
            ... )
        """
        import traceback
        import inspect
        import re
        
        # Generate unique ID
        import hashlib
        unique_id = hashlib.md5(f"{test_name}{original_locator}".encode()).hexdigest()[:8]
        heal_id = f"HEAL-{unique_id.upper()}"
        
        # Parse test name to extract file path and test details
        test_file = "unknown"
        test_class = None
        test_method = "unknown_test"
        line_number = None
        
        if "::" in test_name:
            parts = test_name.split("::")
            test_file = parts[0]
            if len(parts) > 1:
                # Could be test_method or TestClass::test_method
                if len(parts) == 2:
                    test_method = parts[1]
                elif len(parts) == 3:
                    test_class = parts[1]
                    test_method = parts[2]
        
        # Determine error type
        error_type = "TimeoutError"
        if "Timeout" in error_message:
            error_type = "TimeoutError"
        elif "not found" in error_message.lower():
            error_type = "ElementNotFoundError"
        elif "not visible" in error_message.lower():
            error_type = "ElementNotVisibleError"
        
        # Determine locator types
        original_locator_type = self._determine_locator_type(original_locator)
        suggested_locator_type = self._determine_locator_type(new_locator)
        
        # Determine severity based on error type and context
        severity = "medium"
        if "Timeout" in error_message:
            severity = "high"
        elif test_context and test_context.get("failure_count", 1) > 2:
            severity = "critical"
        
        # Build comprehensive entry
        entry = {
            "id": heal_id,
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "status": "healed",
            "test_info": {
                "test_name": test_method,
                "test_file": test_file,
                "test_class": test_class,
                "test_method": test_method,
                "line_number": line_number
            },
            "error_details": {
                "error_type": error_type,
                "error_message": error_message,
                "stack_trace": test_context.get("stack_trace", "") if test_context else "",
                "failure_count": test_context.get("failure_count", 1) if test_context else 1,
                "last_success": test_context.get("last_success") if test_context else None,
                "action_attempted": action_name or "unknown"
            },
            "locator_issue": {
                "original_locator": original_locator,
                "original_locator_type": original_locator_type,
                "failed_reason": self._extract_failure_reason(error_message),
                "suggested_locator": new_locator,
                "suggested_locator_type": suggested_locator_type,
                "confidence_score": confidence_score,
                "alternative_locators": alternative_locators or []
            },
            "code_context": {
                "file_path": test_file,
                "function_name": test_method,
                "code_snippet_before": "",
                "problematic_line": f"        page.{original_locator}",
                "code_snippet_after": "",
                "line_start": None,
                "line_end": None
            },
            "root_cause_analysis": {
                "primary_cause": self._analyze_root_cause(original_locator, new_locator, error_message),
                "contributing_factors": self._identify_contributing_factors(original_locator_type, error_message),
                "environmental_factors": {
                    "browser": test_context.get("browser", "unknown") if test_context else "unknown",
                    "viewport": test_context.get("viewport", "unknown") if test_context else "unknown",
                    "network_conditions": "normal"
                }
            },
            "suggested_fix": {
                "fix_type": "locator_replacement",
                "priority": "high" if severity in ["high", "critical"] else "medium",
                "code_changes": [
                    {
                        "file": test_file,
                        "line_number": line_number,
                        "original_code": f"        page.{original_locator}",
                        "fixed_code": f"        page.locator('{new_locator}')" if not new_locator.startswith("get_by_") else f"        page.{new_locator}",
                        "change_type": "replace"
                    }
                ],
                "alternative_fixes": self._generate_alternative_fixes(new_locator, alternative_locators),
                "validation_steps": [
                    "Run the test 5 times to ensure stability",
                    "Verify the locator works across different browsers",
                    "Check if the fix handles edge cases (slow network, delayed rendering)"
                ]
            },
            "ai_recommendations": {
                "best_practice": self._get_best_practice(suggested_locator_type),
                "preventive_measures": [
                    "Add explicit waits for dynamic content",
                    "Use multiple fallback locators",
                    "Implement retry logic for flaky elements"
                ],
                "test_improvement": "Consider adding a custom fixture that waits for critical page elements before proceeding"
            },
            "metadata": {
                "healer_agent": "HealerAgent-v1.0",
                "healing_strategy": "locator_analysis_and_replacement",
                "auto_fix_eligible": True,
                "requires_human_review": False,
                "estimated_fix_time_seconds": 15,
                "related_issues": [],
                "tags": self._generate_tags(error_type, original_locator_type, action_name)
            }
        }
        
        try:
            with open(self.log_file, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                
                # Check for existing entry
                existing_index = -1
                for i, item in enumerate(data):
                    if item.get("test_name") == test_name and item.get("original_locator") == original_locator:
                        existing_index = i
                        break
                
                if existing_index != -1:
                    # Update existing entry
                    data[existing_index] = entry
                else:
                    # Append new entry
                    data.append(entry)
                
                f.seek(0)
                f.truncate() # Ensure we remove old content if new content is shorter
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Failed to log change: {e}")
    
    def _determine_locator_type(self, locator):
        """Determine the type of locator being used."""
        if locator.startswith("get_by_role"):
            return "role_based"
        elif locator.startswith("get_by_text"):
            return "text_based"
        elif locator.startswith("get_by_label"):
            return "label_based"
        elif locator.startswith("get_by_placeholder"):
            return "placeholder_based"
        elif locator.startswith("get_by_test_id"):
            return "test_id_based"
        elif locator.startswith("//"):
            return "xpath"
        elif locator.startswith("#"):
            return "id_selector"
        elif locator.startswith("."):
            return "class_selector"
        elif "[" in locator and "]" in locator:
            return "attribute_selector"
        else:
            return "css_selector"
    
    def _extract_failure_reason(self, error_message):
        """Extract a human-readable failure reason from the error message."""
        if "Timeout" in error_message:
            return "Element not found or not visible within timeout period"
        elif "not found" in error_message.lower():
            return "Element does not exist in the DOM"
        elif "not visible" in error_message.lower():
            return "Element exists but is not visible"
        elif "not attached" in error_message.lower():
            return "Element was detached from the DOM"
        else:
            return "Unknown failure reason"
    
    def _analyze_root_cause(self, original_locator, new_locator, error_message):
        """Analyze and determine the root cause of the failure."""
        if "get_by_role" in original_locator or "get_by_text" in original_locator:
            return "Dynamic content loading - element text or role may be rendered differently or delayed"
        elif "#" in original_locator and "#" in new_locator and original_locator != new_locator:
            return "Element ID changed - likely due to dynamic ID generation or UI update"
        elif "Timeout" in error_message:
            return "Element loading timeout - element may load slowly or conditionally"
        else:
            return "Locator specificity issue - original locator may be too specific or incorrect"
    
    def _identify_contributing_factors(self, locator_type, error_message):
        """Identify contributing factors to the failure."""
        factors = []
        
        if locator_type in ["role_based", "text_based"]:
            factors.append(f"{locator_type.replace('_', ' ').title()} locator may be too specific for dynamic content")
        
        if "Timeout" in error_message:
            factors.append("Possible timing issue with page rendering")
            factors.append("Element might load conditionally or asynchronously")
        
        if locator_type == "id_selector":
            factors.append("ID might be dynamically generated")
        
        return factors if factors else ["No specific contributing factors identified"]
    
    def _generate_alternative_fixes(self, new_locator, alternative_locators):
        """Generate alternative fix suggestions."""
        fixes = []
        
        # Add wait-based alternative
        fixes.append({
            "description": "Add explicit wait before interacting with element",
            "code": f"        page.wait_for_selector('{new_locator}', state='visible')\n        page.locator('{new_locator}').click()"
        })
        
        # Add alternatives from AI if provided
        if alternative_locators:
            for alt in alternative_locators[:2]:  # Limit to top 2 alternatives
                if isinstance(alt, dict):
                    fixes.append({
                        "description": f"Use {alt.get('type', 'alternative')} locator",
                        "code": f"        page.locator('{alt.get('locator', '')}').click()"
                    })
        
        return fixes
    
    def _get_best_practice(self, locator_type):
        """Get best practice recommendation based on locator type."""
        best_practices = {
            "id_selector": "Use stable IDs or data-testid attributes for reliable element identification",
            "css_selector": "Use specific CSS selectors with stable attributes like href or data attributes",
            "xpath": "Prefer CSS selectors over XPath for better performance and maintainability",
            "role_based": "Role-based locators are good for accessibility but may need fallbacks for dynamic content",
            "text_based": "Text-based locators are fragile; use them with exact=False or combine with other attributes",
            "attribute_selector": "Attribute selectors are stable when targeting unchanging attributes like href or data-*"
        }
        return best_practices.get(locator_type, "Use stable, unique attributes for element identification")
    
    def _generate_tags(self, error_type, locator_type, action_name):
        """Generate relevant tags for categorization."""
        tags = []
        
        if error_type:
            tags.append(error_type.lower().replace("error", "_error"))
        
        if locator_type:
            tags.append(locator_type)
        
        if action_name:
            tags.append(f"action_{action_name}")
        
        # Add general tags
        if "timeout" in error_type.lower():
            tags.append("timing_issue")
        
        if locator_type in ["role_based", "text_based"]:
            tags.append("dynamic_content")
        
        return tags

