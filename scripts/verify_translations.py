#!/usr/bin/env python3
"""
Script to verify that all translations are properly compiled.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def verify_translations():
    """Verify that all translation files are properly compiled."""
    print("Verifying translation compilation...")

    # Check for translation directories
    translations_dir = "translations"
    if not os.path.exists(translations_dir):
        print(f"❌ Translations directory not found: {translations_dir}")
        return False

    # Expected languages
    expected_languages = ["es", "ca", "en", "zh"]

    all_good = True

    for lang in expected_languages:
        lang_dir = os.path.join(translations_dir, lang, "LC_MESSAGES")
        po_file = os.path.join(lang_dir, "messages.po")
        mo_file = os.path.join(lang_dir, "messages.mo")

        if not os.path.exists(lang_dir):
            print(f"❌ Language directory not found: {lang_dir}")
            all_good = False
            continue

        if not os.path.exists(po_file):
            print(f"❌ Translation source file not found: {po_file}")
            all_good = False
            continue

        if not os.path.exists(mo_file):
            print(f"❌ Compiled translation file not found: {mo_file}")
            all_good = False
            continue

        # Check if .mo file is newer than .po file
        po_mtime = os.path.getmtime(po_file)
        mo_mtime = os.path.getmtime(mo_file)

        if mo_mtime < po_mtime:
            print("⚠️  Translation file outdated for {}: {}".format(lang, mo_file))
            print("   Please run: python scripts/babel_manager.py compile")
            all_good = False
            continue

        print(f"✅ Language {lang}: translations compiled successfully")

    if all_good:
        print("✅ All translations verified successfully!")
        return True
    else:
        print("❌ Some translations are missing or not properly compiled.")
        return False


if __name__ == "__main__":
    success = verify_translations()
    sys.exit(0 if success else 1)
