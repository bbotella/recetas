#!/usr/bin/env python3
"""
Script to create Basque translation files (.po) for Flask-Babel using AI translations.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate_basque_translations import translate_to_basque_ai  # noqa: E402


def create_basque_po_file():
    """
    Create a complete Basque .po file with AI translations.
    """
    print("Creating Basque .po file with AI translations...")

    # Common interface strings to translate
    interface_strings = [
        "Aunt Carmen's Recipes",
        "Traditional family recipes",
        "Home",
        "Categories",
        "Language",
        "Search recipes...",
        "Search",
        "All categories",
        "Recipes found",
        "No recipes found",
        "Back to home",
        "Ingredients",
        "Instructions",
        "Preparation",
        "Preparation time",
        "Servings",
        "Difficulty",
        "Easy",
        "Medium",
        "Hard",
        "View recipe",
        "Share",
        "Print",
        "Favorites",
        "Add to favorites",
        "Remove from favorites",
        "Comments",
        "Write comment",
        "Send",
        "Cancel",
        "Save",
        "Edit",
        "Delete",
        "Confirm",
        "About us",
        "Contact",
        "Terms of use",
        "Privacy policy",
        "All rights reserved",
        "Developed with",
        "Filter by",
        "Sort by",
        "Relevance",
        "Date",
        "Alphabetical",
        "Popular",
        "Recent",
        "Most rated",
        "Loading...",
        "Error loading",
        "Page not found",
        "Go back",
        "Try again",
        "Successful operation",
        "Saved correctly",
        "Changes saved",
        "Preserving family culinary traditions",
        "Desserts",
        "Drinks",
        "Chicken",
        "Fish",
        "Meat",
        "Vegetables",
        "Appetizers",
        "Others",
    ]

    # Create .po file content
    po_content = """# Basque (Euskera) translations for Recipe App
# This file is distributed under the same license as the Recipe App project.
# Generated with AI translation system.
#
msgid ""
msgstr ""
"Project-Id-Version: Recipe App 1.0\\n"
"Report-Msgid-Bugs-To: admin@example.com\\n"
"POT-Creation-Date: 2024-01-01 12:00+0000\\n"
"PO-Revision-Date: 2024-01-01 12:00+0000\\n"
"Last-Translator: AI Translation System\\n"
"Language: eu\\n"
"Language-Team: Basque\\n"
"Plural-Forms: nplurals=2; plural=(n != 1)\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: AI Translation System\\n"

"""

    # Add translations for each string
    for english_string in interface_strings:
        basque_translation = translate_to_basque_ai(english_string, "interface")
        po_content += f'msgid "{english_string}"\n'
        po_content += f'msgstr "{basque_translation}"\n\n'

    # Write to .po file
    po_file_path = "translations/eu/LC_MESSAGES/messages.po"
    with open(po_file_path, "w", encoding="utf-8") as f:
        f.write(po_content)

    print(f"✅ Created Basque .po file: {po_file_path}")

    # Also create .pot template file for reference
    pot_file_path = "translations/eu/LC_MESSAGES/messages.pot"
    with open(pot_file_path, "w", encoding="utf-8") as f:
        f.write(po_content)

    print(f"✅ Created Basque .pot template file: {pot_file_path}")


def main():
    """
    Main function to create Basque translation files.
    """
    print("Basque Translation File Generator")
    print("=" * 40)

    create_basque_po_file()

    print("\n" + "=" * 40)
    print("🎉 Basque translation files created successfully!")
    print("Run 'python scripts/babel_manager.py compile' to compile translations.")


if __name__ == "__main__":
    main()
