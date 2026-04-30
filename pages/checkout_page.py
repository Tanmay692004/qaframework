"""
Checkout Page - POM for checkout flow (information and finish)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
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

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def start_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        btn.click()

    def enter_customer_info(self, first_name: str, last_name: str, postal_code: str):
        fn = self.wait.until(EC.presence_of_element_located(self.FIRST_NAME))
        ln = self.driver.find_element(*self.LAST_NAME)
        pc = self.driver.find_element(*self.POSTAL_CODE)

        fn.clear(); fn.send_keys(first_name)
        ln.clear(); ln.send_keys(last_name)
        pc.clear(); pc.send_keys(postal_code)

    def continue_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        btn.click()

    def finish_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        btn.click()

    def get_complete_header(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.COMPLETE_HEADER))
        return el.text.strip()

    def get_complete_text(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.COMPLETE_TEXT))
        return el.text.strip()
