"""
Checkout Page - POM for checkout flow (information and finish)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object Model for SauceDemo checkout pages"""

    # From cart page to checkout start
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # Checkout: Your Information
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    # Checkout: Overview
    FINISH_BUTTON = (By.ID, "finish")

    # Completion
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)

    def start_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def enter_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)

    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        return self.get_text(self.COMPLETE_TEXT)

    def get_error_message(self) -> str:
        """Return checkout validation error text."""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            return ""
