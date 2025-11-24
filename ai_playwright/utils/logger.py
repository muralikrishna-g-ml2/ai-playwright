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

    def log_change(self, test_name, original_locator, new_locator, error_message):
        """
        Log a healing action to the JSON file.
        
        Records details about a successful locator healing, including timestamp,
        test name, original and new locators, and the error that triggered healing.
        
        If an entry with the same test_name and original_locator already exists,
        it will be updated instead of creating a duplicate.
        
        Args:
            test_name (str): Name of the test that failed (e.g., "tests/test_login.py::test_user_login")
            original_locator (str): The locator that failed
            new_locator (str): The healed locator that succeeded
            error_message (str): The error message from the original failure
        
        Example:
            >>> logger = ChangeLogger()
            >>> logger.log_change(
            ...     "tests/test_login.py::test_submit",
            ...     "#submit-btn",
            ...     "#continue-btn",
            ...     "Locator.click: Timeout 2000ms exceeded"
            ... )
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "original_locator": original_locator,
            "new_locator": new_locator,
            "error_message": error_message
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
