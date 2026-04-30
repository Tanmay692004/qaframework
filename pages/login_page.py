"""
Login Page - Page Object Model for the login page
Handles all interactions with the SauceDemo login page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object Model for SauceDemo Login Page"""

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_PAGE_TITLE = (By.CLASS_NAME, "app_logo")

    # Base URL
    BASE_URL = "https://www.saucedemo.com"

    def __init__(self, driver):
        """
        Initialize LoginPage with WebDriver instance

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        """Navigate to the login page"""
        self.driver.get(self.BASE_URL)
        return self

    def enter_username(self, username: str):
        """
        Enter username in the username field

        Args:
            username (str): Username to enter
        """
        username_field = self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str):
        """
        Enter password in the password field

        Args:
            password (str): Password to enter
        """
        password_field = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self):
        """Click the Login button"""
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()

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
            error_element = self.wait.until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except:
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
        except:
            return False
