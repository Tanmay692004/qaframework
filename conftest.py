"""Pytest configuration, shared fixtures, and failure diagnostics."""

import base64
import re
from datetime import datetime

import pytest
from utils.driver_factory import DriverFactory
from utils.logger import Logger
from utils.config import REPORTS_DIR, SCREENSHOTS_DIR, DEFAULT_WAIT_SECONDS

try:
    import pytest_html
except Exception:  # pragma: no cover - available in normal test runs
    pytest_html = None


# Initialize logger
logger = Logger.setup_logger(__name__)


def _sanitize_nodeid(nodeid: str) -> str:
    """Convert a pytest nodeid into a filename-safe slug."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", nodeid)
    return cleaned.strip("_")


def _build_screenshot_path(item, browser: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"{_sanitize_nodeid(item.nodeid)}__{browser}__{timestamp}.png"
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    return str(SCREENSHOTS_DIR / filename)


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
    driver.implicitly_wait(DEFAULT_WAIT_SECONDS)

    yield driver

    # Teardown - close driver
    logger.info(f"Closing WebDriver")
    driver.quit()


@pytest.fixture(autouse=True)
def log_test_lifecycle(request):
    """Log test start/end for easier report triage."""
    logger.info("TEST START: %s", request.node.nodeid)
    yield
    logger.info("TEST END: %s", request.node.nodeid)


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

    metadata = getattr(config, "_metadata", None)
    if metadata is not None:
        metadata["Project"] = "QA Framework"
        metadata["Reports"] = str(REPORTS_DIR)
        metadata["Screenshots"] = str(SCREENSHOTS_DIR)


def pytest_html_report_title(report):
    report.title = "SauceDemo QA Automation Report"


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
                browser = item.funcargs.get("browser", "chrome")
                screenshot_name = _build_screenshot_path(item, browser)
                driver.save_screenshot(screenshot_name)
                logger.error(
                    "Test failed: %s. Screenshot saved: %s",
                    item.nodeid,
                    screenshot_name,
                )

                if pytest_html is not None:
                    extra = getattr(report, "extra", [])
                    try:
                        with open(screenshot_name, "rb") as image_file:
                            encoded = base64.b64encode(image_file.read()).decode("utf-8")

                        extra.append(
                            pytest_html.extras.html(
                                f'<div><p><strong>Failure screenshot:</strong></p>'
                                f'<img src="data:image/png;base64,{encoded}" '
                                f'alt="failure screenshot" '
                                f'style="max-width: 100%; border: 1px solid #d0d7de;" />'
                                f"</div>"
                            )
                        )
                        report.extra = extra
                    except Exception:
                        logger.warning(
                            "Could not attach screenshot to HTML report for %s",
                            item.nodeid,
                        )
