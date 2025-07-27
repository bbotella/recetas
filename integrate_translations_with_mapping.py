#!/usr/bin/env python3
"""
Script to map and integrate recipe translations from JSON files to database.
Maps recipe IDs by matching titles between JSON and database.
"""

import json
import sqlite3
import os
from fuzzywuzzy import fuzz


def load_json_translations(filename):
    """Load translations from JSON file"""
    if not os.path.exists(filename):
        print(f"Warning: {filename} does not exist")
        return {}

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def get_recipe_mapping():
    """Create mapping between JSON IDs and database IDs by matching titles"""
    # Load English translations as reference
    english_translations = load_json_translations("translations_english.json")

    # Get all recipes from database
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM recipes")
    db_recipes = cursor.fetchall()
    conn.close()

    # Create mapping
    mapping = {}

    for json_id, json_recipe in english_translations.items():
        json_title = json_recipe["title"]
        best_match = None
        best_score = 0

        # Find best matching title in database
        for db_id, db_title in db_recipes:
            score = fuzz.ratio(json_title.lower(), db_title.lower())
            if score > best_score:
                best_score = score
                best_match = db_id

        # Only map if we have a good match (>70% similarity)
        if best_score > 70:
            mapping[json_id] = best_match
            print(
                f"Mapped: {json_id} -> {best_match} "
                f"('{json_title}' -> '{db_title}', score: {best_score})"
            )
        else:
            print(
                f"No good match for: {json_id} '{json_title}' (best score: {best_score})"
            )

    return mapping


def integrate_translations_with_mapping():
    """Integrate translations using ID mapping"""

    # Get ID mapping
    print("Creating ID mapping...")
    mapping = get_recipe_mapping()
    print(f"Successfully mapped {len(mapping)} recipes")

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
        print(f"\\nProcessing {lang_name}...")

        # Load translations
        translations = load_json_translations(filename)
        if not translations:
            continue

        lang_translations = 0

        for json_id, translation in translations.items():
            # Skip if we don't have a mapping for this ID
            if json_id not in mapping:
                continue

            db_id = mapping[json_id]

            try:
                # Insert or replace translation
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO recipe_translations
                    (
                        recipe_id,
                        language,
                        title,
                        description,
                        ingredients,
                        instructions,
                        category)
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

        print(f"Saved {lang_translations} translations for {lang_name}")
        total_translations += lang_translations

    # Commit changes
    conn.commit()
    conn.close()

    print("\\n=== TRANSLATION INTEGRATION COMPLETE ===")
    print(f"Total translations saved to database: {total_translations}")
    print("Recipe translations are now available in the application!")


if __name__ == "__main__":
    integrate_translations_with_mapping()
