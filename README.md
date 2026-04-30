# QA Automation Framework - SauceDemo

A production-quality **Python Selenium Pytest Framework** for test automation, built with industry best practices and the **Page Object Model (POM)** architecture.

## 🎯 Project Overview

**Target Website:** https://www.saucedemo.com  
**Framework:** Python + Selenium + Pytest  
**Architecture:** Page Object Model (POM)  
**Goal:** Comprehensive automation testing framework suitable for job interviews and production use

---

## 📋 Features

- ✅ **Page Object Model** - Clean, maintainable, scalable test structure
- ✅ **Cross-Browser Support** - Chrome and Firefox
- ✅ **Screenshot on Failure** - Automatic captures for debugging
- ✅ **HTML Test Reports** - pytest-html integration
- ✅ **Data-Driven Testing** - Parameterized tests with CSV/JSON
- ✅ **Parallel Execution** - pytest-xdist support
- ✅ **Robust Logging** - Custom logger for test execution
- ✅ **Modular Architecture** - Separation of concerns (tests, pages, utils)

---

## 🚀 Quick Start

### Step 1: Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# List installed packages
pip list

# Run a single test to verify setup
pytest tests/test_login.py::TestLogin::test_valid_login -v
```

---

## 📁 Project Structure

```
qaframework/
├── venv/                      # Virtual environment (ignored in git)
├── tests/                     # Test files
│   ├── __init__.py
│   └── test_login.py         # Login test cases
├── pages/                     # Page Object Model classes
│   ├── __init__.py
│   └── login_page.py         # Login page POM
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── driver_factory.py      # WebDriver creation
│   └── logger.py              # Custom logging
├── screenshots/               # Failure screenshots (generated)
├── reports/                   # HTML reports (generated)
├── conftest.py               # Pytest fixtures and hooks
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_login.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_login.py::TestLogin -v
```

### Run Specific Test Case

```bash
pytest tests/test_login.py::TestLogin::test_valid_login -v
```

### Run Tests with Custom Browser

```bash
# Run on Firefox
pytest --browser=firefox

# Run on Chrome (default)
pytest --browser=chrome
```

### Run Tests with HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Run Tests in Parallel

```bash
pytest -n 4  # Run with 4 workers
```

### Run Only Smoke Tests

```bash
pytest -m smoke
```

---

## ✅ Step 1 - Completed (Current)

**What's Implemented:**

1. **Virtual Environment Setup**
   - Created isolated Python environment with venv
   - Installed all required dependencies
   - Created `requirements.txt` with pinned versions

2. **Project Structure**
   - Scaffolded `tests/`, `pages/`, `utils/`, `reports/`, `screenshots/` folders
   - Added `__init__.py` in all packages

3. **Core Utilities**
   - **`driver_factory.py`** - WebDriver factory for Chrome and Firefox creation
   - **`logger.py`** - Custom logger for test execution
   - **`conftest.py`** - Pytest fixtures for driver management and screenshot on failure

4. **Page Object Model**
   - **`login_page.py`** - Complete LoginPage POM with all methods:
     - `load()` - Navigate to login page
     - `enter_username()` / `enter_password()` - Input credentials
     - `login()` - Complete login flow
     - `get_error_message()` - Capture errors
     - `is_login_successful()` - Verify successful login

5. **Test Cases**
   - ✅ `test_valid_login` - Valid credentials login
   - ✅ `test_negative_login_scenarios` - JSON-driven invalid, locked, and empty credential cases

6. **Configuration**
   - `pytest.ini` - Pytest settings, markers, and addopts
   - `.gitignore` - Proper ignore rules

---

## 📚 Test Credentials (SauceDemo)

**Valid Users:**
- Username: `standard_user` | Password: `secret_sauce`
- Username: `problem_user` | Password: `secret_sauce`
- Username: `performance_glitch_user` | Password: `secret_sauce`

**Invalid Users:**
- Username: `locked_out_user` | Password: `secret_sauce` (Returns: locked account error)

---

## 🏗️ Architecture Details

### Page Object Model (POM)

Each page has:
- **Locators**: CSS/XPath selectors
- **Constructor**: Receives WebDriver instance
- **Methods**: User interactions (login, click, fill)
- **Assertions**: Page element verification

Example:
```python
login_page = LoginPage(driver)
login_page.load()
login_page.login("username", "password")
assert login_page.is_login_successful()
```

### Pytest Fixtures

- **`driver`** - Scope: `function` - Fresh driver per test, auto teardown
- **`browser`** - Browser type selection via CLI

### Custom Hooks

- **`pytest_runtest_makereport`** - Captures screenshot on failure
- **`pytest_addoption`** - Adds `--browser` command line option

---

## 🔍 Debugging

### View Test Logs

```bash
# Run with full output
pytest -v -s

# Run with short traceback
pytest --tb=short
```

### Check Screenshots

- Failed test screenshots saved in `screenshots/` folder
- Named as: `test_name_YYYY-MM-DD_HH-MM-SS_ms.png`

### View Latest HTML Report

```bash
# Generate and view report
pytest --html=reports/report.html --self-contained-html
# Open reports/report.html in browser
```

---

## 📝 Next Steps (Upcoming)

- **Step 2:** Cross-browser testing improvements and additional POM pages
- **Step 3:** Data-driven testing with CSV/JSON
- **Step 4:** Inventory and Product tests
- **Step 5:** Cart functionality tests
- **Step 6:** Complete checkout flow tests
- **Step 7:** CI/CD integration with GitHub Actions

---

## 📖 Best Practices Implemented

1. ✅ **DRY (Don't Repeat Yourself)** - Driver factory and fixtures
2. ✅ **Single Responsibility** - Separate classes for pages and utils
3. ✅ **Explicit Waits** - WebDriverWait with expected conditions
4. ✅ **Proper Logging** - Detailed logs for debugging
5. ✅ **Error Handling** - Try-catch for robustness
6. ✅ **Clean Code** - Type hints, docstrings, comments
7. ✅ **Test Independence** - No test dependencies, isolated fixtures

---

## 🛠️ Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'selenium'`
- Solution: Activate venv and run `pip install -r requirements.txt`

**Problem:** Tests not finding elements
- Solution: Check if `wait()` time needs increase in conftest.py

**Problem:** Chrome/Firefox driver not found
- Solution: webdriver-manager auto-downloads drivers (requires internet)

---

## 📞 Contact & Support

For questions or improvements, refer to the test documentation and comments in the code.

---

**Let's build a production-quality framework! 🚀**