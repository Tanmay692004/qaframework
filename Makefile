.PHONY: help test test-login test-products test-checkout test-all test-parallel test-chrome test-firefox test-smoke test-regression report clean install

# Default shell
SHELL := /bin/bash

# Pytest executable (uses venv)
PYTEST := python -m pytest

# Default target
.DEFAULT_GOAL := help

## help: Show this help message
help:
	@echo "QA Automation Framework - Available Commands"
	@echo "============================================"
	@sed -n 's/^## //p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'
	@echo ""
	@echo "Examples:"
	@echo "  make test              # Run all tests"
	@echo "  make test-parallel     # Run in parallel (4 workers)"
	@echo "  make test-firefox      # Run all tests on Firefox"
	@echo "  make report            # Generate HTML report"

## test-login: Run login tests only
test-login:
	$(PYTEST) tests/test_login.py -v

## test-products: Run product/cart tests only
test-products:
	$(PYTEST) tests/test_products.py -v

## test-checkout: Run checkout tests only
test-checkout:
	$(PYTEST) tests/test_checkout.py -v

## test: Run all tests (full suite)
test:
	$(PYTEST) tests/ -v

## test-parallel: Run all tests in parallel (4 workers)
test-parallel:
	$(PYTEST) tests/ -n 4 -v

## test-chrome: Run all tests on Chrome
test-chrome:
	$(PYTEST) tests/ --browser=chrome -v

## test-firefox: Run all tests on Firefox
test-firefox:
	$(PYTEST) tests/ --browser=firefox -v

## test-smoke: Run smoke tests only
test-smoke:
	$(PYTEST) -m smoke -v

## test-regression: Run regression tests only
test-regression:
	$(PYTEST) -m regression -v

## test-headed: Run all tests in headed (visible) mode
test-headed:
	$(PYTEST) tests/ --headed -v

## test-retry: Run tests with automatic retry on failure (2 retries)
test-retry:
	$(PYTEST) tests/ --reruns 2 --reruns-delay 1 -v

## report: Generate HTML report for full suite
report:
	$(PYTEST) tests/ \
		--html=reports/report.html \
		--self-contained-html \
		--junitxml=reports/junit.xml \
		-v

## report-parallel: Generate HTML report with parallel execution
report-parallel:
	$(PYTEST) tests/ \
		-n 4 \
		--html=reports/report-parallel.html \
		--self-contained-html \
		--junitxml=reports/junit-parallel.xml \
		-v

## report-firefox: Generate HTML report on Firefox
report-firefox:
	$(PYTEST) tests/ \
		--browser=firefox \
		--html=reports/report-firefox.html \
		--self-contained-html \
		--junitxml=reports/junit-firefox.xml \
		-v

## debug: Run a single test in headed mode with verbose output
debug:
	$(PYTEST) tests/test_login.py::test_login_cases -vv --headed -s

## clean: Remove generated reports and screenshots
clean:
	@rm -rf reports/*.html reports/*.xml screenshots/*.png
	@echo "Cleaned reports and screenshots"

## install: Install dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt

## lint: Check code style (optional)
lint:
	@echo "Linting hooks can be added here"

## version: Show Python and pytest versions
version:
	@python --version
	@$(PYTEST) --version

.PHONY: help test test-login test-products test-checkout test-all test-parallel \
	test-chrome test-firefox test-smoke test-regression test-headed test-retry \
	report report-parallel report-firefox debug clean install lint version
