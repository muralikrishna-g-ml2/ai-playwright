import os
import pytest

def test_get_by_role_healing(ai_page):
    """Test healing for get_by_role locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try to find button with wrong role/name - should heal to find the actual button
    # The page has button with id="old-submit", we'll try wrong text
    print("\nTesting get_by_role healing...")
    ai_page.get_by_role("button", name="Submit Form").click()
    print("get_by_role test passed!")

def test_get_by_label_healing(ai_page):
    """Test healing for get_by_label locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try wrong label text - should heal to correct one
    print("\nTesting get_by_label healing...")
    ai_page.get_by_label("Email").fill("test@example.com")
    print("get_by_label test passed!")

def test_get_by_placeholder_healing(ai_page):
    """Test healing for get_by_placeholder locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try wrong placeholder - should heal
    print("\nTesting get_by_placeholder healing...")
    ai_page.get_by_placeholder("Search...").fill("laptop")
    print("get_by_placeholder test passed!")

def test_get_by_text_healing(ai_page):
    """Test healing for get_by_text locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try wrong text - should heal
    print("\nTesting get_by_text healing...")
    text = ai_page.get_by_text("Welcome").inner_text()
    assert "Welcome" in text
    print("get_by_text test passed!")

def test_get_by_alt_text_healing(ai_page):
    """Test healing for get_by_alt_text locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try wrong alt text - should heal
    print("\nTesting get_by_alt_text healing...")
    ai_page.get_by_alt_text("Logo").click()
    print("get_by_alt_text test passed!")

def test_get_by_title_healing(ai_page):
    """Test healing for get_by_title locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try wrong title - should heal
    print("\nTesting get_by_title healing...")
    text = ai_page.get_by_title("Items").inner_text()
    assert "items" in text
    print("get_by_title test passed!")

def test_get_by_test_id_healing(ai_page):
    """Test healing for get_by_test_id locator"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Try wrong test id - should heal
    print("\nTesting get_by_test_id healing...")
    ai_page.get_by_test_id("checkout").click()
    print("get_by_test_id test passed!")

def test_chained_locator_healing(ai_page):
    """Test healing for chained locators"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Test chaining with filter
    print("\nTesting chained locator healing...")
    # Try to find product with wrong class, then filter - should heal
    ai_page.locator(".product").filter(has_text="Product C").locator("button").click()
    print("Chained locator test passed!")

def test_locator_list_operations(ai_page):
    """Test healing for list operations (first, last, nth)"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "comprehensive_test.html"))
    ai_page.goto(f"file://{file_path}")
    ai_page.original_page.set_default_timeout(2000)
    
    # Test first, last, nth
    print("\nTesting list operations...")
    ai_page.locator(".add-to-cart").first.click()
    print("List operations test passed!")
