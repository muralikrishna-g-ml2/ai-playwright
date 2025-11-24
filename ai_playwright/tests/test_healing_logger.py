import pytest
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage


def test_healing_with_detailed_logging():
    """
    Test that intentionally fails to trigger the healing mechanism
    and verify that comprehensive details are logged to recommendations/healing_report.json
    """
    import os
    
    # Clean up previous report if exists
    report_path = "recommendations/healing_report.json"
    if os.path.exists(report_path):
        os.remove(report_path)
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        ai_page = AIPage(page)
        
        # Navigate to example.com
        ai_page.goto("https://example.com")
        
        # This will fail because the role name is incorrect
        # It should trigger healing and log comprehensive details
        try:
            ai_page.get_by_role("link", name="More information").click()
            print("✓ Test passed - element was found (possibly healed)")
        except Exception as e:
            print(f"✗ Test failed even after healing attempt: {e}")
            raise
        finally:
            browser.close()
            
    # Verify report was created
    assert os.path.exists(report_path), f"Healing report not found at {report_path}"
    print(f"✓ Verified healing report created at {report_path}")


if __name__ == "__main__":
    test_healing_with_detailed_logging()
