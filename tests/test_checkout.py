"""
Checkout Flow Tests
Covers successful purchase and negative scenarios for missing information
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import Logger

logger = Logger.setup_logger(__name__)


@pytest.mark.checkout
class TestCheckout:
    """Tests for checkout happy and negative flows"""

    def login_and_add_item(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("standard_user", "secret_sauce")
        assert login_page.is_login_successful()

        inventory = InventoryPage(driver)
        inventory.add_product_to_cart("Sauce Labs Backpack")
        inventory.open_cart()
        return inventory

    def test_complete_purchase(self, driver):
        self.login_and_add_item(driver)
        cart = CartPage(driver)

        items = cart.get_cart_items()
        assert "Sauce Labs Backpack" in items

        checkout = CheckoutPage(driver)
        checkout.start_checkout()
        checkout.enter_customer_info("John", "Doe", "12345")
        checkout.continue_checkout()
        checkout.finish_checkout()

        header = checkout.get_complete_header()
        text = checkout.get_complete_text()

        # Allow minor punctuation differences (e.g. trailing '!') in the header
        assert header.upper().startswith("THANK YOU FOR YOUR ORDER"), f"Unexpected header: {header}"
        assert "your order has been dispatched" in text.lower() or "order" in text.lower()

    def test_missing_information_shows_error(self, driver):
        self.login_and_add_item(driver)
        checkout = CheckoutPage(driver)
        checkout.start_checkout()

        # Leave first name empty
        checkout.enter_customer_info("", "Doe", "12345")
        checkout.continue_checkout()

        assert checkout.get_error_message(), "Should display error when required fields are missing"

    @pytest.mark.parametrize(
        "first_name,last_name,postal_code,expected_error",
        [
            ("", "Doe", "12345", "first name"),
            ("John", "", "12345", "last name"),
            ("John", "Doe", "", "postal code"),
        ],
    )
    def test_checkout_validation_messages(self, driver, first_name, last_name, postal_code, expected_error):
        self.login_and_add_item(driver)
        checkout = CheckoutPage(driver)
        checkout.start_checkout()
        checkout.enter_customer_info(first_name, last_name, postal_code)
        checkout.continue_checkout()

        error_message = checkout.get_error_message()
        assert error_message, "Checkout validation error should be shown"
        assert expected_error in error_message.lower()
