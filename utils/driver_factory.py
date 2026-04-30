"""
Driver Factory - Manages WebDriver creation and configuration
Supports Chrome and Firefox browsers with options for headless mode
"""

from selenium import webdriver

from utils.config import DEFAULT_WINDOW_SIZE


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
        options.add_argument(f"--window-size={DEFAULT_WINDOW_SIZE}")

        if headless:
            options.add_argument("--headless")

        # Selenium Manager resolves the driver binary automatically.
        driver = webdriver.Chrome(options=options)
        return driver

    @staticmethod
    def _create_firefox_driver(headless: bool = False):
        """Create Firefox WebDriver with options"""
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = "eager"  # Performance tuning: don't wait for all resources

        width, height = DEFAULT_WINDOW_SIZE.split(",")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

        if headless:
            options.add_argument("--headless")

        # Selenium Manager resolves the driver binary automatically.
        driver = webdriver.Firefox(options=options)
        return driver
