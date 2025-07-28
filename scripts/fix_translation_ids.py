#!/usr/bin/env python3
"""
Fix recipe ID mismatch in translations table.

This script fixes the issue where recipe_translations table had recipe_id values
with an offset of 146 (147-219 instead of 1-73). This caused translations to not
appear in the web application.
"""

import sqlite3
import os
import sys


def fix_translation_ids(db_path="recipes.db"):
    """Fix recipe ID mapping in translations table."""
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("🔧 Fixing recipe ID mapping in translations...")

        # Check if fix is needed
        cursor.execute("SELECT MIN(recipe_id), MAX(recipe_id) FROM recipe_translations")
        min_id, max_id = cursor.fetchone()

        if min_id == 1:
            print("✅ Translation IDs are already correct (starting from 1)")
            return True

        # Calculate offset
        cursor.execute("SELECT MIN(id) FROM recipes")
        min_recipe_id = cursor.fetchone()[0]
        offset = min_id - min_recipe_id

        print(f"📊 Current translation recipe_id range: {min_id} to {max_id}")
        print(f"📊 Detected offset: {offset}")

        # Create backup
        cursor.execute("DROP TABLE IF EXISTS recipe_translations_backup")
        cursor.execute(
            "CREATE TABLE recipe_translations_backup AS SELECT * FROM recipe_translations"
        )
        print("✅ Backup created")

        # Update recipe_id values
        cursor.execute(
            f"UPDATE recipe_translations SET recipe_id = recipe_id - {offset}"
        )
        affected_rows = cursor.rowcount
        print(f"✅ Updated {affected_rows} translation records")

        # Verify the fix
        cursor.execute("SELECT MIN(recipe_id), MAX(recipe_id) FROM recipe_translations")
        new_min_id, new_max_id = cursor.fetchone()
        print(f"✅ New recipe_id range: {new_min_id} to {new_max_id}")

        # Test a specific translation
        cursor.execute(
            'SELECT recipe_id, language, title FROM recipe_translations WHERE recipe_id = 1 AND language = "en"'
        )
        test_result = cursor.fetchone()
        if test_result:
            print(
                f"✅ Test query successful: Recipe {test_result[0]} ({test_result[1]}): {test_result[2]}"
            )
        else:
            print("❌ Test query failed")
            return False

        conn.commit()
        print("🎉 Fix completed and committed!")
        return True

    except Exception as e:
        print(f"❌ Error during fix: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "recipes.db"
    success = fix_translation_ids(db_path)
    sys.exit(0 if success else 1)
