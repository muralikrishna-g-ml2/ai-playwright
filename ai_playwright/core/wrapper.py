from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from .healer import HealerAgent
from ..utils.logger import ChangeLogger
import os

class AIElementHandle:
    """
    Self-healing wrapper for Playwright Locator objects.
    
    This class wraps Playwright's Locator to provide automatic healing capabilities.
    When a locator action fails with a TimeoutError, it uses AI to find an alternative
    locator and retries the action.
    
    Attributes:
        page (AIPage): Reference to the parent AIPage instance
        locator_description (str): Human-readable description of the locator
        element (Locator): The underlying Playwright Locator object
    
    Example:
        >>> ai_page = AIPage(page)
        >>> element = AIElementHandle(ai_page, "#submit-btn")
        >>> element.click()  # Will auto-heal if #submit-btn doesn't exist
    """
    
    def __init__(self, page: 'AIPage', locator_description: str, locator_obj: Locator = None):
        """
        Initialize an AIElementHandle.
        
        Args:
            page (AIPage): The parent AIPage instance
            locator_description (str): Description of the locator (e.g., "#button" or "get_by_role('button')")
            locator_obj (Locator, optional): Pre-created Playwright Locator object.
                If None, treats locator_description as a CSS/XPath selector.
        """
        self.page = page
        self.locator_description = locator_description
        
        # If locator_obj is provided, use it; otherwise treat description as CSS selector
        if locator_obj is not None:
            self.element = locator_obj
        else:
            # Backward compatibility: treat description as CSS/XPath selector
            self.element = page.original_page.locator(locator_description)

    def __getattr__(self, name):
        """
        Dynamically wrap all Locator methods with healing capability.
        
        Args:
            name (str): Name of the attribute/method being accessed
        
        Returns:
            The wrapped method if callable, or the property value directly
        
        Raises:
            AttributeError: If the attribute doesn't exist on the underlying Locator
        """
        if name.startswith("__"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Get the attribute from the underlying Locator
        attr = getattr(self.element, name)

        # If it's a method, wrap it to handle timeouts and healing
        if callable(attr):
            def wrapped_method(*args, **kwargs):
                return self._perform_action(name, *args, **kwargs)
            return wrapped_method
        
        # If it's a property, return it directly
        return attr

    def _perform_action(self, action_name, *args, **kwargs):
        """
        Execute a Locator action with automatic healing on failure.
        
        This method intercepts all Locator method calls. If a TimeoutError occurs,
        it triggers the AI healing process to find an alternative locator and retries.
        
        Args:
            action_name (str): Name of the Locator method to call
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method
        
        Returns:
            The result of the method call, or an AIElementHandle if the method
            returns a Locator (for chaining)
        
        Raises:
            PlaywrightTimeoutError: If healing fails or the healed locator also fails
        """
        try:
            method = getattr(self.element, action_name)
            result = method(*args, **kwargs)
            
            # Handle methods that return new Locators - wrap them in AIElementHandle
            if action_name in ['locator', 'filter', 'and_', 'or_', 'first', 'last', 'nth',
                              'get_by_role', 'get_by_label', 'get_by_placeholder', 
                              'get_by_text', 'get_by_alt_text', 'get_by_title', 'get_by_test_id']:
                # Build descriptive chain
                if action_name == 'locator' and len(args) > 0:
                    new_description = f"{self.locator_description} >> {args[0]}"
                elif action_name in ['first', 'last']:
                    new_description = f"{self.locator_description}.{action_name}()"
                elif action_name == 'nth' and len(args) > 0:
                    new_description = f"{self.locator_description}.nth({args[0]})"
                elif action_name == 'filter':
                    new_description = f"{self.locator_description}.filter(...)"
                elif action_name in ['and_', 'or_']:
                    new_description = f"{self.locator_description}.{action_name}(...)"
                else:
                    # get_by_* methods
                    new_description = f"{self.locator_description}.{action_name}(...)"
                
                return AIElementHandle(self.page, new_description, result)
            
            return result
            
        except PlaywrightTimeoutError as e:
            print(f"Action '{action_name}' failed on '{self.locator_description}'. Attempting to heal...")
            
            # Capture state
            page_content = self.page.original_page.content()
            
            # Heal
            new_locator = self.page.healer.heal(page_content, self.locator_description, str(e))
            
            if new_locator and new_locator != "ELEMENT_MISSING":
                print(f"Healed! New locator: {new_locator}")
                
                # Prepare test context
                test_context = {
                    "browser": self.page.original_page.context.browser.browser_type.name if hasattr(self.page.original_page.context, 'browser') else "unknown",
                    "viewport": str(self.page.original_page.viewport_size) if self.page.original_page.viewport_size else "unknown",
                    "failure_count": 1,  # Could be enhanced to track actual failure count
                    "stack_trace": str(e)
                }
                
                # Log the change with comprehensive details
                self.page.logger.log_change(
                    test_name=os.getenv("PYTEST_CURRENT_TEST", "unknown_test"),
                    original_locator=self.locator_description,
                    new_locator=new_locator,
                    error_message=str(e),
                    action_name=action_name,
                    page_content=page_content[:5000],  # Truncate to avoid huge logs
                    confidence_score=0.85,  # Could be enhanced with actual AI confidence
                    test_context=test_context
                )
                
                # Update self.element and self.locator_description
                # This is crucial: we update the CURRENT handle to point to the new locator
                self.element = self.page.original_page.locator(new_locator)
                self.locator_description = new_locator 
                
                # Retry the action
                method = getattr(self.element, action_name)
                result = method(*args, **kwargs)
                
                # Handle chaining for retried action too
                if action_name in ['locator', 'filter', 'and_', 'or_', 'first', 'last', 'nth',
                                  'get_by_role', 'get_by_label', 'get_by_placeholder', 
                                  'get_by_text', 'get_by_alt_text', 'get_by_title', 'get_by_test_id']:
                    if action_name == 'locator' and len(args) > 0:
                        new_description = f"{self.locator_description} >> {args[0]}"
                    else:
                        new_description = f"{self.locator_description}.{action_name}(...)"
                    return AIElementHandle(self.page, new_description, result)
                
                return result
            else:
                print("Healing failed.")
                raise e

class AIPage:
    """
    Self-healing wrapper for Playwright Page objects.
    
    This class wraps Playwright's Page to provide automatic healing for all locator
    methods. It's a drop-in replacement for Playwright's Page that adds AI-powered
    self-healing capabilities.
    
    Attributes:
        original_page (Page): The underlying Playwright Page object
        healer (HealerAgent): AI agent for healing broken locators
        logger (ChangeLogger): Logger for recording healing actions
    
    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> from ai_playwright import AIPage
        >>> 
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     ai_page = AIPage(page)
        ...     ai_page.goto("https://example.com")
        ...     ai_page.get_by_role("button", name="Submit").click()
    """
    
    def __init__(self, page: Page):
        """
        Initialize an AIPage wrapper.
        
        Args:
            page (Page): The Playwright Page object to wrap
        """
        self.original_page = page
        self.healer = HealerAgent()
        self.logger = ChangeLogger()

    def goto(self, url, **kwargs):
        """
        Navigate to a URL.
        
        Args:
            url (str): URL to navigate to
            **kwargs: Additional arguments passed to Playwright's goto method
        
        Returns:
            Response: The server's response
        """
        return self.original_page.goto(url, **kwargs)

    def locator(self, selector, **kwargs):
        """
        Create a locator with self-healing capability.
        
        Args:
            selector (str): CSS or XPath selector
            **kwargs: Additional arguments for the locator
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.locator("#submit-btn").click()
        """
        return AIElementHandle(self, selector)
    
    # Playwright semantic locator methods
    def get_by_role(self, role, **kwargs):
        """
        Locate element by ARIA role with self-healing.
        
        Args:
            role (str): ARIA role (e.g., "button", "checkbox", "link")
            **kwargs: Additional arguments like name, exact, etc.
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_role("button", name="Submit").click()
        """
        locator_obj = self.original_page.get_by_role(role, **kwargs)
        description = f"get_by_role({role!r}, ...)"
        return AIElementHandle(self, description, locator_obj)
    
    def get_by_label(self, text, **kwargs):
        """
        Locate form control by associated label with self-healing.
        
        Args:
            text (str): Label text
            **kwargs: Additional arguments like exact
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_label("Email").fill("user@example.com")
        """
        locator_obj = self.original_page.get_by_label(text, **kwargs)
        description = f"get_by_label({text!r})"
        return AIElementHandle(self, description, locator_obj)
    
    def get_by_placeholder(self, text, **kwargs):
        """
        Locate input by placeholder with self-healing.
        
        Args:
            text (str): Placeholder text
            **kwargs: Additional arguments like exact
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_placeholder("Search...").fill("query")
        """
        locator_obj = self.original_page.get_by_placeholder(text, **kwargs)
        description = f"get_by_placeholder({text!r})"
        return AIElementHandle(self, description, locator_obj)
    
    def get_by_text(self, text, **kwargs):
        """
        Locate element by text content with self-healing.
        
        Args:
            text (str): Text content to search for
            **kwargs: Additional arguments like exact
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_text("Welcome").is_visible()
        """
        locator_obj = self.original_page.get_by_text(text, **kwargs)
        description = f"get_by_text({text!r})"
        return AIElementHandle(self, description, locator_obj)
    
    def get_by_alt_text(self, text, **kwargs):
        """
        Locate image by alt text with self-healing.
        
        Args:
            text (str): Alt text
            **kwargs: Additional arguments like exact
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_alt_text("Company Logo").click()
        """
        locator_obj = self.original_page.get_by_alt_text(text, **kwargs)
        description = f"get_by_alt_text({text!r})"
        return AIElementHandle(self, description, locator_obj)
    
    def get_by_title(self, text, **kwargs):
        """
        Locate element by title attribute with self-healing.
        
        Args:
            text (str): Title attribute value
            **kwargs: Additional arguments like exact
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_title("Close").click()
        """
        locator_obj = self.original_page.get_by_title(text, **kwargs)
        description = f"get_by_title({text!r})"
        return AIElementHandle(self, description, locator_obj)
    
    def get_by_test_id(self, test_id):
        """
        Locate element by test id (data-testid) with self-healing.
        
        Args:
            test_id (str): Test ID value
        
        Returns:
            AIElementHandle: Self-healing element handle
        
        Example:
            >>> ai_page.get_by_test_id("checkout-button").click()
        """
        locator_obj = self.original_page.get_by_test_id(test_id)
        description = f"get_by_test_id({test_id!r})"
        return AIElementHandle(self, description, locator_obj)
    
    def frame_locator(self, selector):
        """
        Locate frame - returns FrameLocator (not wrapped for now).
        
        Args:
            selector (str): Frame selector
        
        Returns:
            FrameLocator: Playwright's FrameLocator (not wrapped)
        
        Note:
            FrameLocator is not currently wrapped with healing capabilities.
        """
        # Note: FrameLocator is a different class, would need separate wrapper
        return self.original_page.frame_locator(selector)
    
    def __getattr__(self, name):
        """
        Delegate all other attributes to the underlying Page object.
        
        Args:
            name (str): Attribute name
        
        Returns:
            The attribute from the underlying Playwright Page
        """
        return getattr(self.original_page, name)
