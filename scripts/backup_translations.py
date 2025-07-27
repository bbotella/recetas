#!/usr/bin/env python3
"""
Script para exportar las traducciones actuales de la base de datos local
y poder importarlas en Docker.
"""

import os
import sys
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def export_current_translations():
    """Exportar todas las traducciones actuales."""
    print("📤 Exportando traducciones actuales...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Exportar traducciones de recetas
    cursor.execute(
        """
        SELECT r.id, r.title, rt.language, rt.title, rt.description, rt.ingredients, rt.instructions
        FROM recipes r
        JOIN recipe_translations rt ON r.id = rt.recipe_id
        ORDER BY r.id, rt.language
    """
    )

    translations = []
    for row in cursor.fetchall():
        (
            recipe_id,
            original_title,
            language,
            title,
            description,
            ingredients,
            instructions,
        ) = row
        translations.append(
            {
                "recipe_id": recipe_id,
                "original_title": original_title,
                "language": language,
                "title": title,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
            }
        )

    conn.close()

    # Guardar en archivo JSON
    with open("translations_backup.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"✅ Exportadas {len(translations)} traducciones a translations_backup.json")
    return translations


def import_translations_from_backup():
    """Importar traducciones desde archivo de backup."""
    print("📥 Importando traducciones desde backup...")

    if not os.path.exists("translations_backup.json"):
        print("❌ No se encontró archivo translations_backup.json")
        return False

    try:
        with open("translations_backup.json", "r", encoding="utf-8") as f:
            translations = json.load(f)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Importar cada traducción
        for trans in translations:
            cursor.execute(
                """
                INSERT OR REPLACE INTO recipe_translations
                (recipe_id, language, title, description, ingredients, instructions)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    trans["recipe_id"],
                    trans["language"],
                    trans["title"],
                    trans["description"],
                    trans["ingredients"],
                    trans["instructions"],
                ),
            )

        conn.commit()
        conn.close()

        print(f"✅ Importadas {len(translations)} traducciones desde backup")
        return True

    except Exception as e:
        print(f"❌ Error importando traducciones: {e}")
        return False


def main():
    """Función principal."""
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        # Importar traducciones
        init_database()
        import_translations_from_backup()
    else:
        # Exportar traducciones
        export_current_translations()


if __name__ == "__main__":
    main()
