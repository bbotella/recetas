#!/usr/bin/env python3
"""
Docker-compatible script to compile Flask-Babel translations.
This script handles the compilation process without relying on shell commands.
"""

import os
import sys
import subprocess
from pathlib import Path


def compile_translations():
    """Compile all translation files to .mo format."""
    print("🔄 Compiling Flask-Babel translations...")

    # Change to the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Check if translations directory exists
    translations_dir = project_root / "translations"
    if not translations_dir.exists():
        print("❌ No translations directory found")
        return False

    # Try to compile using pybabel
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pybabel", "compile", "-d", "translations"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("✅ Successfully compiled translations using pybabel")
        print(f"Output: {result.stdout}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠️ pybabel compilation failed: {e}")

        # Fallback: try to use the manual compilation script
        try:
            # Add current directory to path for imports
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            from compile_mo_files import compile_all_translations

            # Compile all translations manually
            count = compile_all_translations()
            if count > 0:
                print(f"✅ {count} language files compiled manually")
                return True
            else:
                print("❌ No translations files found to compile")
                return False
        except Exception as fallback_error:
            print(f"❌ Fallback compilation failed: {fallback_error}")
            return False


def main():
    """Main function."""
    print("Docker Translation Compiler")
    print("=" * 40)

    success = compile_translations()

    if success:
        print("\n🎉 Translation compilation completed successfully!")

        # Verify compiled files
        mo_files = list(Path("translations").glob("**/LC_MESSAGES/messages.mo"))
        print(f"Compiled .mo files: {len(mo_files)}")
        for mo_file in mo_files:
            print(f"  - {mo_file}")
    else:
        print("\n❌ Translation compilation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
