#!/usr/bin/env python3
"""
Database migration script to add calories columns to existing recipes table.
"""

import sqlite3
import os
import sys

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DATABASE_PATH  # noqa: E402


def migrate_database():
    """Add calories columns to existing recipes table."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Add estimated_calories column
        cursor.execute("ALTER TABLE recipes ADD COLUMN estimated_calories INTEGER")
        print("✅ Added estimated_calories column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("⚠️  estimated_calories column already exists")
        else:
            print(f"❌ Error adding estimated_calories column: {e}")

    try:
        # Add servings column
        cursor.execute("ALTER TABLE recipes ADD COLUMN servings INTEGER DEFAULT 4")
        print("✅ Added servings column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("⚠️  servings column already exists")
        else:
            print(f"❌ Error adding servings column: {e}")

    conn.commit()
    conn.close()
    print("✅ Database migration completed")


if __name__ == "__main__":
    migrate_database()
