"""
Test Login - Login page test cases
Tests valid login, invalid login, locked user, and empty credentials scenarios
"""

import pytest
from pages.login_page import LoginPage
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

        # Arrange
        login_page = LoginPage(driver)
        username = "standard_user"
        password = "secret_sauce"

        # Act
        login_page.load()
        login_page.login(username, password)

        # Assert
        assert login_page.is_login_successful(), "Login should be successful"
        assert "inventory" in driver.current_url, "Should redirect to inventory page"
        logger.info("test_valid_login: PASSED")

    def test_invalid_login(self, driver):
        """
        Test Case: Invalid login with wrong password
        Expected: Error message is displayed
        """
        logger.info("Starting test_invalid_login")

        # Arrange
        login_page = LoginPage(driver)
        username = "standard_user"
        password = "wrong_password"

        # Act
        login_page.load()
        login_page.login(username, password)

        # Assert
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed"
        assert "do not match" in error_message.lower(), "Should show password mismatch error"
        logger.info(f"test_invalid_login: PASSED - Error: {error_message}")

    def test_locked_user_login(self, driver):
        """
        Test Case: Login with locked user account
        Expected: Locked user error message is displayed
        """
        logger.info("Starting test_locked_user_login")

        # Arrange
        login_page = LoginPage(driver)
        username = "locked_out_user"
        password = "secret_sauce"

        # Act
        login_page.load()
        login_page.login(username, password)

        # Assert
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed"
        assert "locked" in error_message.lower(), "Should show locked user error"
        logger.info(f"test_locked_user_login: PASSED - Error: {error_message}")

    def test_empty_username(self, driver):
        """
        Test Case: Login with empty username
        Expected: Error message for empty username
        """
        logger.info("Starting test_empty_username")

        # Arrange
        login_page = LoginPage(driver)
        username = ""
        password = "secret_sauce"

        # Act
        login_page.load()
        login_page.login(username, password)

        # Assert
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed for empty username"
        assert "required" in error_message.lower() or "username" in error_message.lower(), \
            "Should show username required error"
        logger.info(f"test_empty_username: PASSED - Error: {error_message}")

    def test_empty_password(self, driver):
        """
        Test Case: Login with empty password
        Expected: Error message for empty password
        """
        logger.info("Starting test_empty_password")

        # Arrange
        login_page = LoginPage(driver)
        username = "standard_user"
        password = ""

        # Act
        login_page.load()
        login_page.login(username, password)

        # Assert
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed for empty password"
        assert "required" in error_message.lower() or "password" in error_message.lower(), \
            "Should show password required error"
        logger.info(f"test_empty_password: PASSED - Error: {error_message}")

    def test_empty_credentials(self, driver):
        """
        Test Case: Login with both empty username and password
        Expected: Error message for missing credentials
        """
        logger.info("Starting test_empty_credentials")

        # Arrange
        login_page = LoginPage(driver)
        username = ""
        password = ""

        # Act
        login_page.load()
        login_page.login(username, password)

        # Assert
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed for empty credentials"
        logger.info(f"test_empty_credentials: PASSED - Error: {error_message}")
