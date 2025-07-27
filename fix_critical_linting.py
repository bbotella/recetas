#!/usr/bin/env python3
"""
Script to fix critical linting issues systematically.
Focuses on unused imports and line length issues.
"""

import os
import re
import subprocess


def remove_unused_imports_from_file(file_path):
    """Remove unused imports from a specific file"""
    if not os.path.exists(file_path):
        return

    print(f"Fixing unused imports in {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define unused imports to remove
    unused_imports = [
        r"from unittest\.mock import patch, MagicMock\n",
        r"from unittest\.mock import patch\n",
        r"from unittest\.mock import MagicMock\n",
        r"from flask import url_for, session\n",
        r"from flask import url_for\n",
        r"from flask import session\n",
        r"from flask import request\n",
        r"from flask_babel import get_locale\n",
        r"import sqlite3\n",
        r"import tempfile\n",
        r"import os\n",
        r"from database import init_database\n",
        r"from database import get_all_recipes_with_translation\n",
        r"from unittest\.mock import call\n",
        r"from app import create_app_for_testing\n",
    ]

    # Remove unused imports
    for import_pattern in unused_imports:
        content = re.sub(import_pattern, "", content)

    # Remove unused variable assignments
    content = re.sub(r"    sess = .*\n", "", content)

    # Clean up multiple empty lines
    content = re.sub(r"\n\n\n+", "\n\n", content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed {file_path}")


def fix_line_length_in_database():
    """Fix line length issues in database.py"""
    file_path = "database.py"
    if not os.path.exists(file_path):
        return

    print(f"Fixing line length issues in {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix specific long lines
    replacements = [
        (
            'def get_recipe_with_translation(recipe_id, language="es"):',
            'def get_recipe_with_translation(recipe_id, language="es"):',
        ),
        (
            'def search_recipes_with_translation(query, category=None, language="es"):',
            "def search_recipes_with_translation(query, category=None, "
            'language="es"):',
        ),
        (
            'def get_all_recipes_with_translation(language="es"):',
            'def get_all_recipes_with_translation(language="es"):',
        ),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed {file_path}")


def main():
    """Main function to fix critical linting issues"""
    print("=== FIXING CRITICAL LINTING ISSUES ===")

    # Fix unused imports in test files
    test_files = [
        "tests/conftest.py",
        "tests/test_app.py",
        "tests/test_database.py",
        "tests/test_i18n.py",
        "tests/test_integration.py",
        "tests/test_search.py",
        "tests/test_translations.py",
    ]

    for test_file in test_files:
        remove_unused_imports_from_file(test_file)

    # Fix database.py line length issues
    fix_line_length_in_database()

    # Run black to fix formatting
    print("\nRunning black formatter...")
    subprocess.run(["black", "."], capture_output=True)

    print("\n=== CRITICAL LINTING FIXES COMPLETE ===")


if __name__ == "__main__":
    main()
