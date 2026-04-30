"""
Product & Cart Tests
Covers add/remove, sorting, and cart validation
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.logger import Logger

logger = Logger.setup_logger(__name__)


@pytest.mark.cart
@pytest.mark.product
class TestProducts:
    """Tests for product listing and cart functionality"""

    def login_standard(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("standard_user", "secret_sauce")
        assert login_page.is_login_successful(), "Login should succeed"
        return InventoryPage(driver)

    @pytest.mark.parametrize(
        "product_name",
        [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ],
    )
    def test_add_to_cart(self, driver, product_name):
        inventory = self.login_standard(driver)
        added = inventory.add_product_to_cart(product_name)
        assert added, f"Should be able to add {product_name} to cart"
        assert inventory.get_cart_badge_count() == 1, "Cart badge should show 1"

    @pytest.mark.parametrize(
        "product_name",
        [
            "Sauce Labs Backpack",
            "Sauce Labs Fleece Jacket",
        ],
    )
    def test_remove_from_cart(self, driver, product_name):
        inventory = self.login_standard(driver)
        inventory.add_product_to_cart(product_name)
        assert inventory.get_cart_badge_count() == 1

        removed = inventory.remove_product_from_cart(product_name)
        assert removed, f"Should be able to remove {product_name} from cart"
        assert inventory.get_cart_badge_count() == 0, "Cart badge should be gone after removal"

    def test_sort_low_to_high(self, driver):
        inventory = self.login_standard(driver)

        inventory.sort_products("lohi")
        products = inventory.get_all_products()
        prices = [p["price"] for p in products if p["price"] is not None]
        assert prices == sorted(prices), "Prices should be sorted ascending"

    def test_sort_high_to_low(self, driver):
        inventory = self.login_standard(driver)

        inventory.sort_products("hilo")
        products = inventory.get_all_products()
        prices = [p["price"] for p in products if p["price"] is not None]
        assert prices == sorted(prices, reverse=True), "Prices should be sorted descending"

    @pytest.mark.parametrize("sort_value", ["az", "za"])
    def test_sort_by_name(self, driver, sort_value):
        inventory = self.login_standard(driver)

        inventory.sort_products(sort_value)
        product_names = [product["name"] for product in inventory.get_all_products()]

        if sort_value == "az":
            assert product_names == sorted(product_names)
        else:
            assert product_names == sorted(product_names, reverse=True)

    def test_validate_cart_contents(self, driver):
        inventory = self.login_standard(driver)

        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"]
        for name in items_to_add:
            added = inventory.add_product_to_cart(name)
            assert added, f"Should add {name}"

        assert inventory.get_cart_badge_count() == len(items_to_add)

        inventory.open_cart()
        cart = CartPage(driver)
        cart_items = cart.get_cart_items()

        for name in items_to_add:
            assert name in cart_items, f"{name} should be present in cart"

    def test_cart_removal_keeps_other_item(self, driver):
        inventory = self.login_standard(driver)

        first_item = "Sauce Labs Backpack"
        second_item = "Sauce Labs Bolt T-Shirt"
        assert inventory.add_product_to_cart(first_item)
        assert inventory.add_product_to_cart(second_item)
        assert inventory.get_cart_badge_count() == 2

        inventory.open_cart()
        cart = CartPage(driver)

        assert cart.remove_item_by_name(first_item)
        remaining_items = cart.get_cart_items()

        assert second_item in remaining_items
        assert first_item not in remaining_items
