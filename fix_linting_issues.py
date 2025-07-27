#!/usr/bin/env python3
"""
Script to fix remaining linting issues in the translation files.
This addresses unused imports, missing newlines, and other formatting issues.
"""

import os
import re


def fix_unused_imports():
    """Fix unused imports in translation files"""
    files_to_fix = [
        "fix_babel_translations.py",
        "update_babel_translations.py",
        "integrate_recipe_translations.py",
    ]

    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue

        print(f"Fixing imports in {file_path}...")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove unused json import
        content = re.sub(r"import json\n", "", content)

        # Remove unused datetime import
        content = re.sub(r"from datetime import datetime\n", "", content)

        # Add newline at end of file if missing
        if not content.endswith("\n"):
            content += "\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Fixed {file_path}")


def fix_line_breaks():
    """Fix line break issues in babel manager"""
    file_path = "babel_manager.py"

    if not os.path.exists(file_path):
        return

    print(f"Fixing line breaks in {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Add newline at end of file if missing
    if not content.endswith("\n"):
        content += "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed {file_path}")


def fix_translation_coordinator():
    """Fix translation coordinator spacing issues"""
    file_path = "translation_coordinator.py"

    if not os.path.exists(file_path):
        return

    print(f"Fixing spacing in {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Add newline at end of file if missing
    if not content.endswith("\n"):
        content += "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed {file_path}")


def main():
    """Main function to fix linting issues"""
    print("=== FIXING LINTING ISSUES ===")

    fix_unused_imports()
    fix_line_breaks()
    fix_translation_coordinator()

    print("\n=== LINTING FIXES COMPLETE ===")
    print("Run 'black .' to format the files and fix remaining issues.")


if __name__ == "__main__":
    main()
