"""
AI-Enhanced Playwright Framework

A self-healing test automation framework that uses Google Gemini AI to automatically
fix broken locators in Playwright tests.
"""

from .core.wrapper import AIPage, AIElementHandle
from .core.healer import HealerAgent
from .utils.logger import ChangeLogger

__version__ = "0.1.0"
__all__ = ["AIPage", "AIElementHandle", "HealerAgent", "ChangeLogger"]
