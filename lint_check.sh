#!/bin/bash
set -e

echo "🔍 Running Complete Lint Check..."
echo "================================="

echo "1. Black formatter check..."
black --check --diff .

echo "2. Flake8 linter..."
flake8 .

echo "3. Pylint analysis..."
pylint --disable=all --enable=unused-import,undefined-variable,syntax-error *.py

echo "================================="
echo "✅ All linting checks passed!"
echo "Ready for CI/CD pipeline!"