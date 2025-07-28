#!/usr/bin/env python3
"""
Test script to verify title translations work correctly.
"""

import sys

from flask_babel import _
from app import app

sys.path.insert(0, ".")


def test_title_translations():
    """Test that title translations work for all languages."""

    print("🔍 Testing Title Translations")
    print("=" * 50)

    # Test languages
    languages = {
        "es": "Recetas de la Tía Carmen",
        "en": "Aunt Carmen's Recipes",
        "zh": "卡门阿姨的食谱",
        "ca": "Receptes de la Tia Carmen",
        "eu": "Carmen Izebaren Errezetek",
    }

    with app.app_context():
        for lang_code, expected_title in languages.items():
            # Simulate request context with language
            with app.test_request_context(f"/?language={lang_code}"):
                actual_title = _("Aunt Carmen's Recipes")
                status = "✅" if actual_title == expected_title else "❌"
                print(f"{status} {lang_code.upper()}: '{actual_title}'")
                if actual_title != expected_title:
                    print(f"    Expected: '{expected_title}'")
                    print(f"    Got:      '{actual_title}'")

    print("\n🎯 Title Translation Test Complete")


def test_template_rendering():
    """Test that templates render titles correctly."""

    print("\n🌐 Testing Template Rendering")
    print("=" * 50)

    languages = ["es", "en", "zh", "ca", "eu"]

    with app.test_client() as client:
        for lang in languages:
            # Test home page
            response = client.get(f"/?language={lang}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {lang.upper()}: Home page loads")

            # Check if title is in response
            if b"<title>" in response.data:
                # Extract title from response
                title_start = response.data.find(b"<title>") + 7
                title_end = response.data.find(b"</title>")
                title = response.data[title_start:title_end].decode("utf-8")
                print(f"    Title: {title}")

    print("\n🎯 Template Rendering Test Complete")


def main():
    """Main test function."""

    print("🔄 TITLE TRANSLATION TESTS")
    print("=" * 60)

    test_title_translations()
    test_template_rendering()

    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETE")
    print("=" * 60)

    print("\nTo test manually:")
    print("1. Run: python3 app.py")
    print("2. Open: http://localhost:5000")
    print("3. Switch languages and check page title")


if __name__ == "__main__":
    main()
