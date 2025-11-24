import os
import pytest

def test_healing_button_click(ai_page):
    # Load the local HTML file
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "demo.html"))
    ai_page.goto(f"file://{file_path}")

    # Try to click a non-existent button (simulating a broken test)
    # The actual button is #continue-btn
    # We will try #submit-btn
    # Set a short timeout to trigger the error quickly
    ai_page.original_page.set_default_timeout(2000)
    
    print("\nAttempting to click #submit-btn (which doesn't exist)...")
    ai_page.locator("#submit-btn").click()

    # Verify the action succeeded (meaning it was healed)
    result_text = ai_page.locator("#result").inner_text()
    assert result_text == "Button Clicked!"
