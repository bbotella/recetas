# Makefile for Tia Carmen Recipe App Testing

.PHONY: help test test-fast test-full coverage lint security clean setup docker-test

# Default target
help:
	@echo "Available commands:"
	@echo "  setup       - Set up development environment"
	@echo "  test        - Run basic test suite"
	@echo "  test-fast   - Run quick tests only"
	@echo "  test-full   - Run full pytest suite with coverage"
	@echo "  coverage    - Generate coverage report"
	@echo "  lint        - Run code linting"
	@echo "  security    - Run security checks"
	@echo "  docker-test - Run tests in Docker container"
	@echo "  clean       - Clean temporary files"

# Set up development environment
setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Setup complete. Activate with: source venv/bin/activate"

# Run basic test suite
test:
	@echo "Running basic test suite..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate && python scripts/run_tests.py; \
	else \
		python3 scripts/run_tests.py; \
	fi

# Run quick tests only
test-fast:
	@echo "Running quick tests..."
	pytest tests/ -m "not slow" -v

# Run full pytest suite with coverage
test-full:
	@echo "Running full test suite with coverage..."
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

# Generate coverage report
coverage:
	@echo "Generating coverage report..."
	python scripts/coverage_report.py

# Run code linting
lint:
	@echo "Running code linting..."
	-flake8 --max-line-length=88 --extend-ignore=E203,W503 .
	-black --check --diff .
	-pylint --disable=all --enable=unused-import,undefined-variable,syntax-error *.py scripts/*.py

# Run security checks
security:
	@echo "Running security checks..."
	-safety check
	-bandit -r . -f json -o bandit-report.json

# Run tests in Docker container
docker-test:
	@echo "Building test Docker image..."
	docker build -f Dockerfile.test -t tia-carmen-tests .
	@echo "Running tests in container..."
	docker run --rm tia-carmen-tests

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf bandit-report.json
	rm -rf test_recipes.db
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*~" -delete

# Install pre-commit hooks
install-hooks:
	@echo "Installing pre-commit hooks..."
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hooks installed!"

# Run all quality checks
check-all: lint security test-full coverage
	@echo "All quality checks completed!"

# CI simulation
ci: setup test-full lint security
	@echo "CI simulation completed!"