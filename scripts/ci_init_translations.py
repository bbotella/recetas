#!/usr/bin/env python3
"""
CI initialization script for setting up translations in GitHub Actions.
This script creates basic translations for CI testing without requiring full AI system.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database


def create_basic_translations():
    """Create basic translations for CI testing."""
    print("🔄 Creating basic translations for CI testing...")

    # Initialize database
    init_database()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if we have any recipes
    cursor.execute("SELECT COUNT(*) FROM recipes")
    recipe_count = cursor.fetchone()[0]

    if recipe_count == 0:
        print("⚠️ No recipes found - skipping translation creation")
        conn.close()
        return True

    # Create basic translations for testing
    languages = ["en", "zh", "ca", "eu"]

    for lang in languages:
        # Delete existing translations
        cursor.execute("DELETE FROM recipe_translations WHERE language = ?", (lang,))

        # Get all recipes
        cursor.execute(
            "SELECT id, title, description, ingredients, instructions, category FROM recipes"
        )
        recipes = cursor.fetchall()

        for recipe in recipes:
            recipe_id, title, description, ingredients, instructions, category = recipe

            # Create basic test translations
            cursor.execute(
                """
                INSERT INTO recipe_translations
                (recipe_id, language, title, description, ingredients, instructions, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    recipe_id,
                    lang,
                    f"{title} ({lang})",
                    f"{description} ({lang})",
                    f"{ingredients} ({lang})",
                    f"{instructions} ({lang})",
                    f"{category} ({lang})",
                ),
            )

    conn.commit()
    conn.close()

    print(f"✅ Created basic translations for {len(languages)} languages")
    return True


def create_basic_po_files():
    """Create basic .po files for CI testing."""
    print("🔄 Creating basic .po files for CI testing...")

    languages = ["es", "en", "zh", "ca", "eu"]

    for lang in languages:
        po_dir = Path(f"translations/{lang}/LC_MESSAGES")
        po_dir.mkdir(parents=True, exist_ok=True)

        po_file = po_dir / "messages.po"

        # Create basic .po file content
        po_content = f"""# {lang} translations for Recipe App (CI Testing)
msgid ""
msgstr ""
"Project-Id-Version: Recipe App 1.0\\n"
"Language: {lang}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Home"
msgstr "Home ({lang})"

msgid "Categories"
msgstr "Categories ({lang})"

msgid "Search"
msgstr "Search ({lang})"

msgid "Ingredients"
msgstr "Ingredients ({lang})"

msgid "Instructions"
msgstr "Instructions ({lang})"
"""

        with open(po_file, "w", encoding="utf-8") as f:
            f.write(po_content)

    print(f"✅ Created basic .po files for {len(languages)} languages")
    return True


def main():
    """Main function for CI initialization."""
    print("🚀 CI Translation Initialization")
    print("=" * 50)

    try:
        # Create basic translations
        if not create_basic_translations():
            print("❌ Failed to create basic translations")
            sys.exit(1)

        # Create basic .po files
        if not create_basic_po_files():
            print("❌ Failed to create basic .po files")
            sys.exit(1)

        print("\n✅ CI translation initialization completed successfully!")

    except Exception as e:
        print(f"❌ CI initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
