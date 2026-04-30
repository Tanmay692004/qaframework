"""
Login Page - Page Object Model for the login page
Handles all interactions with the SauceDemo login page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    """Page Object Model for SauceDemo Login Page"""

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_PAGE_TITLE = (By.CLASS_NAME, "app_logo")

    # Base URL
    BASE_URL = BASE_URL

    def __init__(self, driver):
        """
        Initialize LoginPage with WebDriver instance

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)

    def load(self):
        """Navigate to the login page"""
        self.open(self.BASE_URL)
        return self

    def enter_username(self, username: str):
        """
        Enter username in the username field

        Args:
            username (str): Username to enter
        """
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        """
        Enter password in the password field

        Args:
            password (str): Password to enter
        """
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click the Login button"""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """
        Perform login with provided credentials

        Args:
            username (str): Username
            password (str): Password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self) -> str:
        """
        Get error message if login failed

        Returns:
            str: Error message text, or empty string if no error
        """
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            return ""

    def is_login_successful(self) -> bool:
        """
        Check if login was successful by verifying inventory page is loaded

        Returns:
            bool: True if inventory page element is present, False otherwise
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.INVENTORY_PAGE_TITLE))
            return True
        except Exception:
            return False
