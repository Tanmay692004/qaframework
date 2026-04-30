"""
Test Login - Login page test cases
Uses data-driven testing for negative login scenarios.
"""

import pytest

from pages.login_page import LoginPage
from utils.data_loader import DataLoader
from utils.logger import Logger

logger = Logger.setup_logger(__name__)


@pytest.mark.login
class TestLogin:
    """Test cases for login functionality"""

    @pytest.mark.smoke
    def test_valid_login(self, driver):
        """
        Test Case: Valid login attempt
        Expected: User successfully logs in and inventory page is displayed
        """
        logger.info("Starting test_valid_login")

        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("standard_user", "secret_sauce")

        assert login_page.is_login_successful(), "Login should be successful"
        assert "inventory" in driver.current_url, "Should redirect to inventory page"
        logger.info("test_valid_login: PASSED")

    @pytest.mark.parametrize(
        "case_data",
        DataLoader.load_json("test_data/login_negative_cases.json"),
        ids=lambda case: case["case_id"],
    )
    def test_negative_login_scenarios(self, driver, case_data):
        """
        Data-driven login validation for invalid, locked, and empty credential scenarios.
        """
        logger.info("Starting test_negative_login_scenarios: %s", case_data["case_id"])

        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(case_data["username"], case_data["password"])

        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed"
        assert case_data["expected_error_contains"] in error_message.lower(), (
            f"Expected '{case_data['expected_error_contains']}' in '{error_message}'"
        )
        logger.info(
            "test_negative_login_scenarios: PASSED - %s | Error: %s",
            case_data["case_id"],
            error_message,
        )
