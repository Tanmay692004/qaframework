"""
Driver Factory - Manages WebDriver creation and configuration
Supports Chrome and Firefox browsers with options for headless mode
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverFactory:
    """Factory class to create WebDriver instances"""

    @staticmethod
    def create_driver(browser_name: str = "chrome", headless: bool = False):
        """
        Create and return a WebDriver instance

        Args:
            browser_name (str): Browser type - "chrome" or "firefox"
            headless (bool): Run browser in headless mode

        Returns:
            WebDriver: Selenium WebDriver instance

        Raises:
            ValueError: If unsupported browser is specified
        """
        browser_name = browser_name.lower().strip()

        if browser_name == "chrome":
            return DriverFactory._create_chrome_driver(headless)
        elif browser_name == "firefox":
            return DriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(
                f"Unsupported browser: {browser_name}. Use 'chrome' or 'firefox'"
            )

    @staticmethod
    def _create_chrome_driver(headless: bool = False):
        """Create Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()
        options.page_load_strategy = "eager"  # Performance tuning: don't wait for all resources

        # Add desired options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        if headless:
            options.add_argument("--headless")

        # Create driver with auto-download via webdriver-manager
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
        return driver

    @staticmethod
    def _create_firefox_driver(headless: bool = False):
        """Create Firefox WebDriver with options"""
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = "eager"  # Performance tuning: don't wait for all resources

        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        if headless:
            options.add_argument("--headless")

        # Create driver with auto-download via webdriver-manager
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
        return driver
