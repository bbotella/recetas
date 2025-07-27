#!/usr/bin/env python3
"""
Script to fix specific linting issues more carefully.
"""

import os
import re


def fix_specific_unused_imports():
    """Fix only the specific unused imports that are clearly not needed"""
    
    # Fix test_app.py
    if os.path.exists("tests/test_app.py"):
        with open("tests/test_app.py", "r") as f:
            content = f.read()
        
        # Remove specific unused imports
        content = re.sub(r"from app import create_app_for_testing\n", "", content)
        content = re.sub(r"    sess = .*\n", "", content)
        
        with open("tests/test_app.py", "w") as f:
            f.write(content)
        print("Fixed tests/test_app.py")
    
    # Fix test_database.py
    if os.path.exists("tests/test_database.py"):
        with open("tests/test_database.py", "r") as f:
            content = f.read()
        
        # Remove specific unused imports
        content = re.sub(r"from database import init_database\n", "", content)
        
        with open("tests/test_database.py", "w") as f:
            f.write(content)
        print("Fixed tests/test_database.py")
    
    # Fix test_search.py
    if os.path.exists("tests/test_search.py"):
        with open("tests/test_search.py", "r") as f:
            content = f.read()
        
        # Remove specific unused imports
        content = re.sub(r"from database import get_all_recipes_with_translation\n", "", content)
        
        with open("tests/test_search.py", "w") as f:
            f.write(content)
        print("Fixed tests/test_search.py")
    
    # Fix test_translations.py
    if os.path.exists("tests/test_translations.py"):
        with open("tests/test_translations.py", "r") as f:
            content = f.read()
        
        # Remove specific unused imports
        content = re.sub(r"from unittest\.mock import MagicMock, call\n", "", content)
        content = re.sub(r"from database import init_database\n", "", content)
        
        with open("tests/test_translations.py", "w") as f:
            f.write(content)
        print("Fixed tests/test_translations.py")


def main():
    """Main function"""
    print("=== FIXING SPECIFIC UNUSED IMPORTS ===")
    fix_specific_unused_imports()
    print("=== SPECIFIC FIXES COMPLETE ===")


if __name__ == "__main__":
    main()