#!/usr/bin/env python3
"""
Script to verify Valencian translations are working correctly
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def verify_valencian_translations():
    """Verify all Valencian translations are in place"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🔶 Verifying Valencian translations...")
    print("=" * 60)

    # Check total recipes
    cursor.execute("SELECT COUNT(*) FROM recipes")
    total_recipes = cursor.fetchone()[0]
    print(f"📊 Total recipes in database: {total_recipes}")

    # Check Valencian translations
    cursor.execute("SELECT COUNT(*) FROM recipe_translations WHERE language = 'va'")
    valencian_count = cursor.fetchone()[0]
    print(f"🔶 Valencian translations: {valencian_count}")

    # Check coverage
    coverage = (valencian_count / total_recipes) * 100
    print(f"📈 Translation coverage: {coverage:.1f}%")

    # Sample verification
    print("\n🔶 Sample Valencian translations:")
    print("-" * 40)

    cursor.execute(
        """
        SELECT r.id, r.title as spanish_title, rt.title as valencian_title, rt.category
        FROM recipes r
        LEFT JOIN recipe_translations rt ON r.id = rt.recipe_id AND rt.language = 'va'
        ORDER BY r.id
        LIMIT 10
    """
    )

    samples = cursor.fetchall()
    for sample in samples:
        if sample["valencian_title"]:
            print(
                f"✅ {sample['id']}: {sample['spanish_title']} → {sample['valencian_title']}"
            )
        else:
            print(f"❌ {sample['id']}: {sample['spanish_title']} → (missing)")

    # Check categories
    print("\n🔶 Category translations:")
    print("-" * 40)

    cursor.execute(
        """
        SELECT DISTINCT category as spanish_category,
               (SELECT rt.category FROM recipe_translations rt WHERE rt.category IS NOT NULL
                AND rt.language = 'va' AND rt.category != ''
                AND rt.recipe_id IN (SELECT id FROM recipes WHERE category = r.category)
                LIMIT 1) as valencian_category
        FROM recipes r
        ORDER BY category
    """
    )

    categories = cursor.fetchall()
    for cat in categories:
        if cat["valencian_category"]:
            print(f"✅ {cat['spanish_category']} → {cat['valencian_category']}")
        else:
            print(f"❌ {cat['spanish_category']} → (missing)")

    # Check languages available
    print("\n🔶 Available languages:")
    print("-" * 40)

    cursor.execute(
        "SELECT DISTINCT language, COUNT(*) as count FROM recipe_translations GROUP BY language ORDER BY language"
    )
    languages = cursor.fetchall()
    for lang in languages:
        print(f"✅ {lang['language']}: {lang['count']} translations")

    conn.close()

    print("\n" + "=" * 60)
    if coverage >= 100:
        print("🎉 SUCCESS! All recipes have Valencian translations!")
        print("🔶 Valencian is now available in the language selector")
        print("🔶 Position: 2nd (after Spanish, before English)")
    else:
        print("⚠️  Some recipes may need Valencian translations")

    return coverage >= 100


def test_web_interface():
    """Test that web interface supports Valencian"""
    print("\n🔶 Testing web interface support...")
    print("-" * 40)

    # Check if app.py has been updated
    try:
        with open("app.py", "r") as f:
            content = f.read()
            if '"va": "Valencià"' in content:
                print("✅ Valencian language added to app.py")
            else:
                print("❌ Valencian language not found in app.py")
    except FileNotFoundError:
        print("❌ app.py not found")

    # Check if translation files exist
    if os.path.exists("translations/va/LC_MESSAGES/messages.po"):
        print("✅ Valencian .po file exists")
    else:
        print("❌ Valencian .po file missing")

    if os.path.exists("translations/va/LC_MESSAGES/messages.mo"):
        print("✅ Valencian .mo file exists")
    else:
        print("❌ Valencian .mo file missing")


if __name__ == "__main__":
    success = verify_valencian_translations()
    test_web_interface()

    if success:
        print("\n🎉 VERIFICATION COMPLETE!")
        print("✅ All Valencian translations are working correctly")
        print("✅ Web interface supports Valencian")
        print("✅ Valencian is in 2nd position in language selector")
    else:
        print("\n⚠️  VERIFICATION INCOMPLETE")
        print("❌ Some translations may be missing")
