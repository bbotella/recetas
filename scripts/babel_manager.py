#!/usr/bin/env python3
"""
Babel management script for Flask-Babel internationalization
"""
import sys
import subprocess


def run_command(cmd, description):
    """Run a command and print the result"""
    print(f"Running: {description}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True


def extract_messages():
    """Extract translatable strings from code"""
    cmd = "pybabel extract -F babel.cfg -k _ -o messages.pot ."
    return run_command(cmd, "Extracting translatable strings")


def init_language(lang):
    """Initialize a new language"""
    cmd = f"pybabel init -i messages.pot -d translations -l {lang}"
    return run_command(cmd, f"Initializing language: {lang}")


def update_translations():
    """Update existing translations"""
    cmd = "pybabel update -i messages.pot -d translations"
    return run_command(cmd, "Updating translations")


def compile_translations():
    """Compile translations to .mo files"""
    cmd = "pybabel compile -d translations"
    return run_command(cmd, "Compiling translations")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python babel_manager.py extract    - Extract strings")
        print("  python babel_manager.py init <lang> - Initialize new language")
        print("  python babel_manager.py update     - Update existing translations")
        print("  python babel_manager.py compile    - Compile translations")
        print("  python babel_manager.py all        - Do extract, update, and compile")
        return

    action = sys.argv[1]

    if action == "extract":
        extract_messages()
    elif action == "init":
        if len(sys.argv) < 3:
            print("Please specify language code (e.g. 'fr' for French)")
            return
        lang = sys.argv[2]
        if extract_messages():
            init_language(lang)
    elif action == "update":
        if extract_messages():
            update_translations()
    elif action == "compile":
        compile_translations()
    elif action == "all":
        if extract_messages():
            if update_translations():
                compile_translations()
    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    main()
