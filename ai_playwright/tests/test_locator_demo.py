import os
import pytest

def test_get_by_role_simple(ai_page):
    """Simple test showing get_by_role healing"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "demo.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Use get_by_role instead of locator - will heal if button text changes
    print("\nTesting get_by_role with healing...")
    ai_page.get_by_role("button", name="Continue").click()
    
    # Verify the action succeeded
    result_text = ai_page.locator("#result").inner_text()
    assert result_text == "Button Clicked!"
    print("get_by_role test passed!")
