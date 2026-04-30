"""
Central configuration for the Selenium framework.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.saucedemo.com"
DEFAULT_WAIT_SECONDS = 10
DEFAULT_WINDOW_SIZE = "1920,1080"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"
