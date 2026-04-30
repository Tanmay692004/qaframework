"""
Cart Page - Page Object Model for the shopping cart
Handles validation of cart contents and item removal
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import DEFAULT_WAIT_SECONDS


class CartPage:
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTON = (By.XPATH, ".//button[contains(@class,'cart_button') or contains(@class,'btn_inventory')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_SECONDS)

    def get_cart_items(self):
        """Return list of product names present in the cart"""
        items = []
        elems = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEM))
        for el in elems:
            name = el.find_element(*self.ITEM_NAME).text.strip()
            items.append(name)
        return items

    def remove_item_by_name(self, product_name: str) -> bool:
        """Remove item by name from cart. Returns True if removed."""
        elems = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEM))
        for el in elems:
            name = el.find_element(*self.ITEM_NAME).text.strip()
            if name.lower() == product_name.lower():
                btn = el.find_element(By.XPATH, ".//button")
                btn.click()
                return True
        return False
