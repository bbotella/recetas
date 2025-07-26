#!/usr/bin/env python3
"""
Script to migrate recipe translations from 'va' to 'ca' in the database.
This is needed because we changed the language code from 'va' to 'ca' for Babel compatibility.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection


def migrate_language_code(old_code, new_code):
    """Migrate recipe translations from old language code to new language code."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if old language code exists
    cursor.execute(
        "SELECT COUNT(*) FROM recipe_translations WHERE language = ?", (old_code,)
    )
    old_count = cursor.fetchone()[0]

    if old_count == 0:
        print(f"No translations found for language '{old_code}'")
        return False

    # Check if new language code already exists
    cursor.execute(
        "SELECT COUNT(*) FROM recipe_translations WHERE language = ?", (new_code,)
    )
    new_count = cursor.fetchone()[0]

    print(f"Found {old_count} translations for '{old_code}'")
    if new_count > 0:
        print(f"Warning: {new_count} translations already exist for '{new_code}'")
        print("These will be replaced by the migration.")

    # Migrate translations
    cursor.execute(
        "UPDATE recipe_translations SET language = ? WHERE language = ?",
        (new_code, old_code),
    )

    migrated_count = cursor.rowcount
    print(f"Migrated {migrated_count} translations from '{old_code}' to '{new_code}'")

    conn.commit()
    conn.close()

    return True


def main():
    """Main function to migrate Valencian translations."""
    print("Migrating Valencian translations from 'va' to 'ca'...")
    print("=" * 50)

    success = migrate_language_code("va", "ca")

    if success:
        print("\n✅ Migration completed successfully!")
        print("Valencian recipes should now display correctly in the web interface.")
    else:
        print("\n❌ Migration failed or no translations to migrate.")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
