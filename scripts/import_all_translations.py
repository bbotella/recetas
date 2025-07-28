#!/usr/bin/env python3
"""
Script para importar todas las traducciones desde archivos JSON individuales
para uso en Docker.
"""

import os
import sys
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def import_translations_from_individual_files():
    """Importar traducciones desde archivos individuales por idioma."""
    print("📥 Importando traducciones desde archivos individuales...")

    # Mapeo de archivos a códigos de idioma
    language_files = {
        "english": "en",
        "chinese": "zh",
        "catalan": "ca",
        "euskera": "eu",
    }

    conn = get_db_connection()
    cursor = conn.cursor()

    total_imported = 0

    for file_suffix, lang_code in language_files.items():
        filename = f"translations_{file_suffix}.json"

        if not os.path.exists(filename):
            print(f"⚠️  Archivo {filename} no encontrado, saltando...")
            continue

        try:
            with open(filename, "r", encoding="utf-8") as f:
                translations = json.load(f)

            # Importar traducciones para este idioma
            for recipe_id, translation_data in translations.items():
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO recipe_translations
                    (recipe_id, language, title, description, ingredients, instructions, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        int(recipe_id),
                        lang_code,
                        translation_data.get("title", ""),
                        translation_data.get("description", ""),
                        translation_data.get("ingredients", ""),
                        translation_data.get("instructions", ""),
                        translation_data.get("category", ""),
                    ),
                )

            conn.commit()
            imported_count = len(translations)
            total_imported += imported_count
            print(
                f"✅ Importadas {imported_count} traducciones desde {filename} ({lang_code})"
            )

        except Exception as e:
            print(f"❌ Error importando desde {filename}: {e}")
            continue

    conn.close()
    print(f"✅ Total importadas: {total_imported} traducciones")

    return total_imported


def verify_translations_imported():
    """Verificar que las traducciones fueron importadas correctamente."""
    print("\n🔍 Verificando traducciones importadas...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Contar traducciones por idioma
    cursor.execute(
        """
        SELECT language, COUNT(*) as count
        FROM recipe_translations
        GROUP BY language
        ORDER BY language
    """
    )

    results = cursor.fetchall()

    if not results:
        print("❌ No se encontraron traducciones en la base de datos")
        conn.close()
        return False

    print("📊 Traducciones por idioma:")
    for lang, count in results:
        print(f"  {lang}: {count} traducciones")

    # Verificar algunas traducciones específicas
    cursor.execute(
        """
        SELECT r.id, r.title, rt.language, rt.title as translated_title
        FROM recipes r
        JOIN recipe_translations rt ON r.id = rt.recipe_id
        WHERE rt.language = 'en'
        LIMIT 3
    """
    )

    sample_translations = cursor.fetchall()

    if sample_translations:
        print("\n📝 Ejemplo de traducciones (EN):")
        for recipe_id, original, lang, translated in sample_translations:
            print(f"  {recipe_id}: '{original}' -> '{translated}'")

    conn.close()
    return True


def main():
    """Función principal."""
    print("=== IMPORTACIÓN DE TRADUCCIONES PARA DOCKER ===")

    # Inicializar base de datos
    init_database()

    # Importar traducciones
    total_imported = import_translations_from_individual_files()

    if total_imported > 0:
        # Verificar importación
        verify_translations_imported()
        print(f"\n✅ Proceso completado: {total_imported} traducciones importadas")
    else:
        print("\n❌ No se importaron traducciones")
        sys.exit(1)


if __name__ == "__main__":
    main()
