#!/usr/bin/env python3
"""
Script to verify that Flask-Babel translations are working correctly in Docker.
"""

import os
import sys
from pathlib import Path


def verify_translations():
    """Verify that all translation files are present and properly compiled."""
    print("🔍 Verifying Flask-Babel translations...")

    # Change to the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Check translations directory
    translations_dir = project_root / "translations"
    if not translations_dir.exists():
        print("❌ No translations directory found")
        return False

    # Expected languages
    expected_languages = ["es", "eu", "ca", "en", "zh"]

    # Check each language
    missing_files = []
    for lang in expected_languages:
        lang_dir = translations_dir / lang / "LC_MESSAGES"
        po_file = lang_dir / "messages.po"
        mo_file = lang_dir / "messages.mo"

        if not po_file.exists():
            missing_files.append(f"{lang}/messages.po")
        if not mo_file.exists():
            missing_files.append(f"{lang}/messages.mo")

    if missing_files:
        print(f"❌ Missing translation files: {missing_files}")
        return False

    # Test Flask-Babel loading
    try:
        from flask import Flask
        from flask_babel import Babel, gettext as _

        app = Flask(__name__)
        app.config["LANGUAGES"] = {
            "es": "Español",
            "ca": "Valencià",
            "en": "English",
            "zh": "中文",
            "eu": "Euskera",
        }
        app.config["BABEL_DEFAULT_LOCALE"] = "es"
        app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"

        babel = Babel()
        babel.init_app(app)

        # Test translation loading for each language
        with app.app_context():
            for lang in expected_languages:
                app.config["BABEL_DEFAULT_LOCALE"] = lang
                try:
                    # Try to get a translation
                    translated = _("View Recipe")
                    print(f"✅ {lang}: '{translated}'")
                except Exception as e:
                    print(f"❌ {lang}: Failed to load translation - {e}")
                    return False

        print("✅ All translations loaded successfully")
        return True

    except Exception as e:
        print(f"❌ Flask-Babel test failed: {e}")
        return False


if __name__ == "__main__":
    success = verify_translations()
    if not success:
        sys.exit(1)
    print("\n🎉 All translations verified successfully!")
