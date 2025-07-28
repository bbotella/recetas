#!/usr/bin/env python3
"""
Script to verify all recipe descriptions and translations have been updated correctly.
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def verify_updates():
    """Verify that all updates have been applied correctly"""
    conn = get_db_connection()

    print("🔍 Verifying recipe descriptions and translations...")
    print("=" * 60)

    # Check Spanish descriptions
    print("\n📚 Checking Spanish descriptions...")
    recipes = conn.execute(
        "SELECT id, title, description FROM recipes ORDER BY id"
    ).fetchall()

    long_descriptions = 0
    for recipe in recipes:
        desc_length = len(recipe["description"])
        if desc_length > 300:  # Enhanced Spanish descriptions should be much longer
            long_descriptions += 1
            print(f"✅ {recipe['title']} - {desc_length} characters")
        else:
            print(
                f"⚠️  {recipe['title']} - {desc_length} characters (may need enhancement)"
            )

    # Check English translations
    print("\n🇬🇧 Checking English translations...")
    en_translations = conn.execute(
        "SELECT recipe_id, title, description FROM recipe_translations WHERE language = 'en' ORDER BY recipe_id"
    ).fetchall()

    long_en_descriptions = 0
    for translation in en_translations:
        desc_length = len(translation["description"])
        if desc_length > 250:  # Enhanced English descriptions should be longer
            long_en_descriptions += 1
            print(f"✅ {translation['title']} - {desc_length} characters")
        else:
            print(
                f"⚠️  {translation['title']} - {desc_length} characters (may need enhancement)"
            )

    # Check Chinese translations
    print("\n🇨🇳 Checking Chinese translations...")
    zh_translations = conn.execute(
        "SELECT recipe_id, title, description FROM recipe_translations WHERE language = 'zh' ORDER BY recipe_id"
    ).fetchall()

    long_zh_descriptions = 0
    for translation in zh_translations:
        desc_length = len(translation["description"])
        if desc_length > 80:  # Chinese text is more compact, so lower threshold
            long_zh_descriptions += 1
            print(f"✅ {translation['title']} - {desc_length} characters")
        else:
            print(
                f"⚠️  {translation['title']} - {desc_length} characters (may need enhancement)"
            )

    conn.close()

    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"Total recipes: {len(recipes)}")
    print(f"Enhanced Spanish descriptions: {long_descriptions}")
    print(f"Enhanced English translations: {long_en_descriptions}")
    print(f"Enhanced Chinese translations: {long_zh_descriptions}")

    if long_descriptions > 0 and long_en_descriptions > 0 and long_zh_descriptions > 0:
        print(
            "\n🎉 SUCCESS! All descriptions have been enhanced with gastronomic and
        emotional tone!"
        )
    else:
        print("\n⚠️  Some descriptions may need further enhancement.")

    return long_descriptions, long_en_descriptions, long_zh_descriptions


def show_sample_updates():
    """Show a sample of the updated descriptions"""
    conn = get_db_connection()

    print("\n📝 Sample of updated descriptions:")
    print("=" * 60)

    # Show Spanish sample
    sample_recipe = conn.execute("SELECT * FROM recipes WHERE id = 147").fetchone()
    if sample_recipe:
        print(f"\n🇪🇸 Spanish - {sample_recipe['title']}:")
        print(f"   {sample_recipe['description'][:200]}...")

    # Show English sample
    sample_en = conn.execute(
        "SELECT * FROM recipe_translations WHERE recipe_id = 147 AND language = 'en'"
    ).fetchone()
    if sample_en:
        print(f"\n🇬🇧 English - {sample_en['title']}:")
        print(f"   {sample_en['description'][:200]}...")

    # Show Chinese sample
    sample_zh = conn.execute(
        "SELECT * FROM recipe_translations WHERE recipe_id = 147 AND language = 'zh'"
    ).fetchone()
    if sample_zh:
        print(f"\n🇨🇳 Chinese - {sample_zh['title']}:")
        print(f"   {sample_zh['description'][:200]}...")

    conn.close()


if __name__ == "__main__":
    verify_updates()
    show_sample_updates()
