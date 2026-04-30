"""
Inventory Page - Page Object Model for product listing and actions
Handles product listing, sorting, add/remove actions, and navigation to cart
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from utils.config import DEFAULT_WAIT_SECONDS


class InventoryPage:
    """Page Object Model for SauceDemo Inventory Page"""

    PRODUCT_CONTAINER = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_REMOVE_BUTTON = (By.XPATH, ".//button[contains(@class,'btn_inventory')]")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_SECONDS)

    def get_all_products(self):
        """Return list of product dicts: {name, price, element}"""
        products = []
        elems = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CONTAINER))
        for el in elems:
            name = el.find_element(*self.PRODUCT_NAME).text.strip()
            price_text = el.find_element(*self.PRODUCT_PRICE).text.strip().replace("$", "")
            try:
                price = float(price_text)
            except Exception:
                price = None
            products.append({"name": name, "price": price, "element": el})
        return products

    def sort_products(self, option_value: str):
        """Sort products by option value (e.g., 'lohi', 'hilo', 'az', 'za')"""
        select_elem = self.wait.until(EC.element_to_be_clickable(self.SORT_SELECT))
        select = Select(select_elem)
        select.select_by_value(option_value)

    def add_product_to_cart(self, product_name: str) -> bool:
        """Click Add to cart button for product with given name. Returns True if clicked."""
        products = self.get_all_products()
        for p in products:
            if p["name"].lower() == product_name.lower():
                btn = p["element"].find_element(By.XPATH, ".//button")
                if btn.text.lower() in ("add to cart", "add to cart "):
                    btn.click()
                    return True
                # if already added, the button might say Remove
                return False
        return False

    def remove_product_from_cart(self, product_name: str) -> bool:
        """Click Remove button for product with given name. Returns True if removed."""
        products = self.get_all_products()
        for p in products:
            if p["name"].lower() == product_name.lower():
                btn = p["element"].find_element(By.XPATH, ".//button")
                if btn.text.lower() in ("remove", "remove "):
                    btn.click()
                    return True
                return False
        return False

    def open_cart(self):
        """Navigate to cart page"""
        cart_link = self.wait.until(EC.element_to_be_clickable(self.SHOPPING_CART_LINK))
        cart_link.click()

    def get_cart_badge_count(self) -> int:
        """Return the integer count shown on the cart badge, or 0 if absent"""
        try:
            badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            return int(badge.text.strip())
        except Exception:
            return 0
