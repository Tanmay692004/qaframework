"""
Central configuration for the Selenium framework.
Supports environment-specific settings and .env file loading.
"""

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load .env file if it exists
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)


def get_env(key: str, default: str = None) -> str:
    """Get environment variable with optional default."""
    return os.getenv(key, default)


# Environment (dev, staging, production)
APP_ENV = get_env("APP_ENV", "dev")

# Base URL configuration (environment-aware)
_ENV_URLS = {
    "dev": "https://www.saucedemo.com",
    "staging": os.getenv("STAGING_URL", "https://www.saucedemo.com"),
    "production": os.getenv("PRODUCTION_URL", "https://www.saucedemo.com"),
}
BASE_URL = _ENV_URLS.get(APP_ENV, "https://www.saucedemo.com")

# Wait and window configuration
DEFAULT_WAIT_SECONDS = int(get_env("DEFAULT_WAIT_SECONDS", "10"))
DEFAULT_WINDOW_SIZE = get_env("DEFAULT_WINDOW_SIZE", "1920,1080")

# Directory configuration
SCREENSHOTS_DIR = PROJECT_ROOT / get_env("SCREENSHOTS_DIR", "screenshots")
REPORTS_DIR = PROJECT_ROOT / get_env("REPORTS_DIR", "reports")

# Feature flags
HEADLESS = get_env("HEADLESS", "true").lower() == "true"
SCREENSHOT_ON_FAILURE = get_env("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

# Logging
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
