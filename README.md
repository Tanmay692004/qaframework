# QA Automation Framework - SauceDemo

Interview-ready Python UI automation framework for SauceDemo, built with Selenium, Pytest, Page Object Model, data-driven tests, failure evidence, and parallel/browser-flexible execution.

## Project Snapshot

- Target app: SauceDemo
- Stack: Python 3.12, Selenium 4, Pytest, pytest-html, pytest-xdist
- Architecture: Page Object Model with a shared base page abstraction
- Driver strategy: Selenium Manager, no manual driver downloads
- Quality goals: maintainable tests, readable reports, and clean execution evidence for interviews

## Why this stands out

- Login coverage is data-driven from external JSON with valid, invalid, and edge cases.
- Failure screenshots are captured only on failures and attached to HTML reports.
- Chrome and Firefox are selectable from a single CLI option.
- Parallel execution is enabled without shared-state collisions by using function-scoped drivers.
- The suite is organized like real client work, not a demo script.

## Features

- Page Object Model for maintainable UI automation
- Base page abstraction to remove duplicate Selenium helpers
- Data-driven login coverage with JSON test data
- Screenshot-on-failure hook via `pytest_runtest_makereport`
- pytest-html integration with report title and metadata
- Cross-browser execution with `--browser=chrome|firefox`
- Parallel execution with pytest-xdist
- Centralized config and driver factory for cleaner abstractions
- Structured logging for test lifecycle visibility
- CI-ready layout for GitHub Actions

## Evidence Included

- Failure screenshots are stored in `screenshots/`
- HTML reports are generated in `reports/`
- README supports embedding execution and report screenshots for recruiter review

Recommended screenshot files for the README:

- `docs/images/test-execution.png`
- `docs/images/html-report.png`

Example Markdown to paste once those images exist:

```markdown
## Execution Evidence

![Test Execution](docs/images/test-execution.png)

![HTML Report](docs/images/html-report.png)
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate it

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execution Commands

### Login suite

```bash
pytest tests/test_login.py -q
```

### Full suite

```bash
pytest
```

### Cross-browser execution

```bash
pytest --browser=chrome
pytest --browser=firefox
```

### Parallel execution

```bash
pytest -n auto
```

### HTML report generation

```bash
pytest tests/test_login.py tests/test_products.py tests/test_checkout.py --html=reports/report.html --self-contained-html
```

### Parallel plus HTML report

```bash
pytest tests/test_login.py tests/test_products.py tests/test_checkout.py -n auto --browser=firefox --html=reports/report.html --self-contained-html
```

## Reporting Behavior

- Reports use pytest-html with a custom title: SauceDemo QA Automation Report
- Metadata includes project, reports path, and screenshots path
- Failure screenshots are embedded inside the report as inline images
- Raw PNG evidence is also preserved in `screenshots/`

## Test Design

### Data-driven login coverage

Login tests are parameterized from `test_data/login_users.json`.

Included scenarios:

- valid users
- invalid users
- edge cases such as empty inputs, long inputs, and injection-like input strings

This matters in interviews because it shows the suite is built for scale, not hardcoded around one happy path.

### Pytest fixtures and hooks

- `driver` creates a fresh browser per test and avoids cross-test contamination
- `browser` reads the CLI browser choice
- `pytest_runtest_makereport` captures screenshots only on failure
- `pytest_addoption` adds browser/headed control without changing code

### Driver strategy

`utils/driver_factory.py` centralizes browser creation.

- Chrome and Firefox are both supported
- Selenium Manager resolves drivers automatically
- Headless runs are enabled by default for CI friendliness
- Browser switching is clean and isolated to the fixture layer

## Repository Layout

```text
qaframework/
├── conftest.py
├── pages/
├── reports/
├── screenshots/
├── test_data/
├── tests/
├── utils/
├── pytest.ini
├── requirements.txt
└── README.md
```

## Current Coverage

- Login flows: data-driven success and failure cases
- Product/cart flows: add, remove, sort, and cart assertions
- Checkout flows: happy path plus validation coverage

## Interview Talking Points

- The framework is structured for maintainability, not just execution.
- Report evidence is attached automatically, which makes defects easier to triage.
- Parallel execution works because each test has its own driver instance.
- The browser is configurable without code changes, which is useful in CI and local debugging.
- JSON-driven test data shows separation of concerns between scenario design and test logic.

## Notes

- If you want the README to look even stronger, add real screenshots from the latest report run using the paths above.
- If a failure occurs, check `screenshots/` first, then open the HTML report in `reports/`.
