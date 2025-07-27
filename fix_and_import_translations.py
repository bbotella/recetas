#!/usr/bin/env python3
"""
Script to fix JSON translation IDs and import them to database.
The JSON files have IDs 147-219, but database has IDs 220-292.
We need to add 73 to each JSON ID to match database IDs.
"""

import json
import sqlite3
import os

# ID offset to convert JSON IDs to database IDs
ID_OFFSET = 73  # JSON starts at 147, DB starts at 220


def fix_and_import_translations():
    """Fix JSON translation IDs and import to database"""

    # Language mappings
    language_files = {
        "english": ("translations_english.json", "en"),
        "chinese": ("translations_chinese.json", "zh"),
        "catalan": ("translations_catalan.json", "ca"),
        "euskera": ("translations_euskera.json", "eu"),
    }

    conn = sqlite3.connect("recipes.db")
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

    for lang_name, (filename, lang_code) in language_files.items():
        print(f"Processing {lang_name}...")

        if not os.path.exists(filename):
            print(f"Warning: {filename} does not exist")
            continue

        # Load JSON translations
        with open(filename, "r", encoding="utf-8") as f:
            translations = json.load(f)

        lang_translations = 0

        for json_id_str, translation in translations.items():
            # Convert JSON ID to database ID
            json_id = int(json_id_str)
            db_id = json_id + ID_OFFSET

            # Verify this recipe exists in database
            cursor.execute("SELECT id FROM recipes WHERE id = ?", (db_id,))
            if not cursor.fetchone():
                print(
                    f"Warning: Recipe {db_id} not found in database (JSON ID: {json_id})"
                )
                continue

            try:
                # Insert or replace translation
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO recipe_translations
                    (recipe_id, language, title, description, ingredients, instructions, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        db_id,
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
                print(f"Error inserting translation for recipe {db_id}: {e}")

        print(f"✅ Saved {lang_translations} translations for {lang_name}")
        total_translations += lang_translations

    # Commit changes
    conn.commit()
    conn.close()

    print("\\n=== TRANSLATION IMPORT COMPLETE ===")
    print(f"Total translations saved to database: {total_translations}")
    print("Recipe translations are now available in the application!")


if __name__ == "__main__":
    fix_and_import_translations()
