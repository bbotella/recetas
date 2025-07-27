#!/usr/bin/env python3
"""
Flask-Babel compilation script for Recetas de la Tía Carmen
This script compiles .po files to .mo files for all supported languages
"""

import subprocess
import sys
from pathlib import Path


def compile_translations():
    """Compile all .po files to .mo files"""

    # Languages to compile
    languages = ["en", "zh", "ca", "eu"]

    # Base directory for translations
    base_dir = Path("/Users/bernardobotellacorbi/Documents/dev/tiaCarmen/translations")

    print("=== COMPILING BABEL TRANSLATIONS ===")

    # Check if we have the required tools
    try:
        subprocess.run(["msgfmt", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: msgfmt not found. Please install gettext tools.")
        print("On macOS: brew install gettext")
        print("On Ubuntu/Debian: sudo apt-get install gettext")
        sys.exit(1)

    success_count = 0

    for lang in languages:
        lang_dir = base_dir / lang / "LC_MESSAGES"
        po_file = lang_dir / "messages.po"
        mo_file = lang_dir / "messages.mo"

        if not po_file.exists():
            print(f"Warning: {po_file} does not exist, skipping {lang}")
            continue

        try:
            # Compile .po to .mo
            result = subprocess.run(
                ["msgfmt", "-o", str(mo_file), str(po_file)],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"✓ Compiled {lang}: {po_file} -> {mo_file}")
                success_count += 1
            else:
                print(f"✗ Error compiling {lang}: {result.stderr}")

        except Exception as e:
            print(f"✗ Error compiling {lang}: {e}")

    print("\n=== COMPILATION COMPLETE ===")
    print(f"Successfully compiled {success_count}/{len(languages)} languages")

    if success_count == len(languages):
        print("All translations compiled successfully!")
        print("You can now restart the Flask application to use the new translations.")
    else:
        print("Some translations failed to compile. Please check the errors above.")


if __name__ == "__main__":
    compile_translations()
