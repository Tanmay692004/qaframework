"""Parametrized login tests driven by JSON data (valid, invalid, edge cases)."""

import pytest

from pages.login_page import LoginPage
from utils.data_loader import DataLoader
from utils.logger import Logger

logger = Logger.setup_logger(__name__)


CASES = DataLoader.load_json("test_data/login_users.json")


@pytest.mark.login
@pytest.mark.parametrize("case", CASES, ids=[c["case_id"] for c in CASES])
def test_login_cases(driver, case):
    """Single parametrized test that covers success and failure login scenarios.

    Data format (test_data/login_users.json):
      - case_id: unique identifier used as pytest id
      - username, password
      - expected: "success" or "failure"
      - expected_error_contains: (for failures) substring to assert in error message
    """
    logger.info("Running login case: %s", case["case_id"])

    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(case.get("username", ""), case.get("password", ""))

    if case.get("expected") == "success":
        assert login_page.is_login_successful(), f"{case['case_id']} should login successfully"
        assert "inventory" in driver.current_url, "Should redirect to inventory page"
        logger.info("%s: PASSED (success)", case["case_id"])
    else:
        error_message = login_page.get_error_message() or ""
        assert error_message, f"{case['case_id']}: expected an error message"
        expected_sub = case.get("expected_error_contains", "").lower()
        assert expected_sub in error_message.lower(), (
            f"{case['case_id']}: expected '{expected_sub}' in '{error_message}'"
        )
        logger.info("%s: PASSED (expected failure) | Error: %s", case["case_id"], error_message)

