#!/usr/bin/env python3
"""
Script to integrate recipe translations from JSON files into the database.
This script loads the translations from the JSON files and saves them to the database.
"""

import sqlite3
import os
import json


def load_json_translations(language_code):
    """Load translations from JSON file"""
    file_path = (
        f"/Users/bernardobotellacorbi/Documents/dev/tiaCarmen/"
        f"translations_{language_code}.json"
    )

    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist")
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def save_recipe_translations_to_db():
    """Save all recipe translations to the database"""

    # Database path
    db_path = "/Users/bernardobotellacorbi/Documents/dev/tiaCarmen/recipes.db"

    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} does not exist")
        return

    # Language mappings
    language_mappings = {
        "english": "en",
        "chinese": "zh",
        "catalan": "ca",
        "euskera": "eu",
    }

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure the recipe_translations table exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipe_translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            language TEXT NOT NULL,
            title TEXT,
            description TEXT,
            ingredients TEXT,
            instructions TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id),
            UNIQUE(recipe_id, language)
        )
    """
    )

    total_translations = 0

    for lang_name, lang_code in language_mappings.items():
        print(f"\nProcessing {lang_name} ({lang_code})...")

        # Load translations from JSON
        translations = load_json_translations(lang_name)

        if not translations:
            print(f"No translations found for {lang_name}")
            continue

        lang_translations = 0

        for recipe_id_str, translation in translations.items():
            recipe_id = int(recipe_id_str)

            # Check if this recipe exists in the main recipes table
            cursor.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,))
            if not cursor.fetchone():
                print(f"Warning: Recipe {recipe_id} not found in main recipes table")
                continue

            try:
                # Insert or replace translation
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO recipe_translations
                    (recipe_id, language, title, description,
                     ingredients, instructions, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        recipe_id,
                        lang_code,
                        translation.get("title", ""),
                        translation.get("description", ""),
                        translation.get("ingredients", ""),
                        translation.get("instructions", ""),
                        translation.get("category", ""),
                    ),
                )

                lang_translations += 1

            except Exception as e:
                print(
                    f"Error inserting translation for recipe {recipe_id} "
                    f"in {lang_name}: {e}"
                )

        print(f"Saved {lang_translations} translations for {lang_name}")
        total_translations += lang_translations

    # Commit changes
    conn.commit()
    conn.close()

    print("\n=== TRANSLATION INTEGRATION COMPLETE ===")
    print(f"Total translations saved to database: {total_translations}")
    print("Recipe translations are now available in the application!")


def main():
    """Main function"""
    print("=== INTEGRATING RECIPE TRANSLATIONS TO DATABASE ===")
    save_recipe_translations_to_db()


if __name__ == "__main__":
    main()
