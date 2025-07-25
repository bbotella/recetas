# Testing Documentation

## Overview

This project includes a comprehensive testing suite with automated CI/CD pipeline for the Tia Carmen recipes web application.

## Test Structure

### Test Files
- `tests/test_database.py` - Database operations (25 tests)
- `tests/test_app.py` - Flask routes and views (35 tests)
- `tests/test_i18n.py` - Internationalization (38 tests)
- `tests/test_search.py` - Search and filtering (43 tests)
- `tests/test_translations.py` - Translation functionality (23 tests)
- `tests/test_integration.py` - Integration tests (27 tests)

**Total: 191 tests**

### Test Categories (Pytest Markers)
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.database` - Database tests
- `@pytest.mark.flask` - Flask application tests
- `@pytest.mark.i18n` - Internationalization tests
- `@pytest.mark.slow` - Performance tests

## Running Tests

### Local Testing

#### Quick Test Run
```bash
# Run basic test suite
python run_tests.py
```

#### Full Pytest Suite
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/ -m "unit" -v
pytest tests/ -m "integration" -v
pytest tests/ -m "database" -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
```

#### Coverage Analysis
```bash
# Generate coverage report
python coverage_report.py
```

### Docker Testing
```bash
# Build test image
docker build -f Dockerfile.test -t tia-carmen-tests .

# Run tests in container
docker run --rm tia-carmen-tests
```

## CI/CD Pipeline

### GitHub Actions Workflows

#### Main CI/CD Pipeline (`.github/workflows/ci-cd.yml`)
- **Test Job**: Runs on Python 3.9, 3.10, 3.11
  - Installs dependencies
  - Runs comprehensive test suite
  - Generates coverage reports
  - Tests application startup

- **Lint Job**: Code quality checks
  - Black code formatter
  - Flake8 linter
  - Pylint analysis

- **Security Job**: Security scanning
  - Safety check for known vulnerabilities
  - Bandit security linter

- **Deploy Job**: Production deployment (main branch only)
  - Builds multi-platform Docker image (amd64, arm64)
  - Tests Docker container functionality
  - Pushes to Docker Hub registry
  - Updates Docker Hub description
  - Implements proper quality gates

#### Simple Test Workflow (`.github/workflows/test.yml`)
- Lightweight testing for quick feedback
- Runs on every push and pull request
- Uses custom test runner for fast validation

### Pre-commit Hooks
- Automatically runs tests before commits
- Prevents broken code from being committed
- Generates coverage reports

## Test Configuration

### Pytest Configuration (`pytest.ini`)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
addopts = --cov=. --cov-report=html --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
    database: Database tests
    flask: Flask application tests
    i18n: Internationalization tests
```

### Test Fixtures (`tests/conftest.py`)
- **app**: Flask application instance for testing
- **client**: Test client for making HTTP requests
- **temp_db**: Temporary SQLite database with test data
- **test_recipes**: Sample recipe data for testing

## Test Data

The test suite uses a temporary SQLite database with sample data:
- 3 test recipes with translations
- Multiple categories (Postres, Pollo, etc.)
- English and Chinese translations for Recipe 1
- Various test scenarios for edge cases

## Coverage Analysis

Current coverage: **28.6%** overall

### Coverage by File:
- `database.py`: 54.5% (6/11 functions)
- `app.py`: 0.0% (0/10 functions)

### Coverage Tools:
- **Pytest-cov**: Standard coverage reporting
- **Custom coverage_report.py**: Detailed function-level analysis
- **HTML reports**: Generated in `htmlcov/` directory

## Continuous Integration

### Triggers
- Push to main/master/develop branches
- Pull requests to main/master/develop branches

### Test Matrix
- Python versions: 3.9, 3.10, 3.11
- Operating system: Ubuntu Latest
- Database: SQLite (temporary for testing)

### Artifacts
- Coverage reports (XML, HTML)
- Security scan results
- Test results and logs

## Best Practices

### Writing Tests
1. Use descriptive test names
2. Follow AAA pattern (Arrange, Act, Assert)
3. Test edge cases and error conditions
4. Use appropriate pytest markers
5. Mock external dependencies
6. Test both positive and negative scenarios

### Test Organization
1. Group related tests in classes
2. Use fixtures for common setup
3. Keep tests independent
4. Use parametrized tests for multiple inputs
5. Separate unit and integration tests

### Maintenance
1. Keep tests updated with code changes
2. Remove obsolete tests
3. Maintain test data
4. Monitor test performance
5. Review coverage reports regularly

## Troubleshooting

### Common Issues

#### Import Errors
- Ensure virtual environment is activated
- Check PYTHONPATH includes project root
- Verify dependencies are installed

#### Database Issues
- Check DATABASE_PATH environment variable
- Ensure database is initialized
- Verify test fixtures are working

#### Coverage Issues
- Run tests with `--cov` flag
- Check coverage configuration
- Ensure all modules are included

### Running Specific Tests
```bash
# Run specific test file
pytest tests/test_database.py -v

# Run specific test function
pytest tests/test_database.py::TestDatabaseOperations::test_get_all_recipes -v

# Run tests matching pattern
pytest tests/ -k "test_search" -v
```

## Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure tests pass locally
3. Add appropriate markers
4. Update documentation
5. Check coverage impact

## Future Improvements

- [ ] Increase test coverage to 80%+
- [ ] Add performance benchmarks
- [ ] Implement end-to-end testing
- [ ] Add API testing
- [ ] Improve error handling tests
- [ ] Add load testing
- [ ] Implement mutation testing