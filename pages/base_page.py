"""
Base Page - shared helpers for Selenium page objects.
"""

import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import DEFAULT_WAIT_SECONDS


class BasePage:
    """Common Selenium interactions shared across all page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_SECONDS)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open(self, url: str):
        self.logger.info("Opening URL: %s", url)
        self.driver.get(url)

    def click(self, locator):
        self.logger.info("Clicking element: %s", locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str, clear: bool = True):
        self.logger.info("Typing text into: %s", locator)
        element = self.wait.until(EC.presence_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        self.logger.info("Reading text from: %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator)).text.strip()

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False