"""
conftest.py - Pytest configuration and shared fixtures
Handles driver setup, teardown, and screenshot on failure
"""

import os
import pytest
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from utils.driver_factory import DriverFactory
from utils.logger import Logger


# Initialize logger
logger = Logger.setup_logger(__name__)


@pytest.fixture(scope="function")
def browser(request):
    """
    Fixture to provide browser type from command line or default to chrome
    Usage: pytest --browser=firefox or pytest (defaults to chrome)
    """
    browser_name = request.config.getoption("--browser", default="chrome")
    return browser_name


@pytest.fixture(scope="function")
def driver(browser, request):
    """
    Fixture to create and tear down WebDriver instance
    Provides a fresh driver for each test
    
    Run headless by default. Override with --headed flag.
    """
    headless = not request.config.getoption("--headed", default=False)
    logger.info(f"Starting WebDriver for browser: {browser} (headless={headless})")

    # Create driver using DriverFactory
    driver = DriverFactory.create_driver(browser_name=browser, headless=headless)
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    # Teardown - close driver
    logger.info(f"Closing WebDriver")
    driver.quit()


def pytest_addoption(parser):
    """Add custom command line options for pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed (visible) mode, default is headless",
    )


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "login: Login tests")
    config.addinivalue_line("markers", "cart: Cart tests")
    config.addinivalue_line("markers", "checkout: Checkout tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure
    Runs after each test to check if it failed
    """
    outcome = yield
    report = outcome.get_result()

    # On test failure, capture screenshot
    if report.when == "call" and report.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]
                screenshot_dir = "screenshots"

                # Create screenshots directory if it doesn't exist
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)

                screenshot_name = (
                    f"{screenshot_dir}/{item.name}_{timestamp}.png"
                )
                driver.save_screenshot(screenshot_name)
                logger.error(
                    f"Test failed: {item.name}. Screenshot saved: {screenshot_name}"
                )
