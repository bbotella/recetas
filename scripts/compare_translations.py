#!/usr/bin/env python3
"""
Script para comparar traducciones locales con las del Docker.
Ayuda a diagnosticar diferencias entre entornos.
"""

import os
import sys
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection  # noqa: E402


def export_translations_to_json(filename="translations_snapshot.json"):
    """Exportar traducciones actuales a JSON para comparación."""
    print(f"📄 Exportando traducciones a {filename}...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener todas las traducciones
    cursor.execute(
        """
        SELECT r.title as original_title, rt.language, rt.title, rt.description, rt.ingredients, rt.instructions
        FROM recipes r
        JOIN recipe_translations rt ON r.id = rt.recipe_id
        ORDER BY r.title, rt.language
    """
    )

    translations = {}
    for row in cursor.fetchall():
        original_title, lang, title, description, ingredients, instructions = row

        if original_title not in translations:
            translations[original_title] = {}

        translations[original_title][lang] = {
            "title": title,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions,
        }

    conn.close()

    # Guardar en JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(translations)} recetas exportadas a {filename}")
    return translations


def compare_translations(local_file, docker_file):
    """Comparar traducciones entre archivos JSON."""
    print(f"🔍 Comparando {local_file} con {docker_file}...")

    try:
        with open(local_file, "r", encoding="utf-8") as f:
            local_translations = json.load(f)

        with open(docker_file, "r", encoding="utf-8") as f:
            docker_translations = json.load(f)

    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        return False

    differences = []

    # Comparar cada receta
    for recipe_title in local_translations:
        if recipe_title not in docker_translations:
            differences.append(f"❌ Receta faltante en Docker: {recipe_title}")
            continue

        local_recipe = local_translations[recipe_title]
        docker_recipe = docker_translations[recipe_title]

        # Comparar cada idioma
        for lang in local_recipe:
            if lang not in docker_recipe:
                differences.append(
                    f"❌ Idioma faltante en Docker: {recipe_title} ({lang})"
                )
                continue

            local_lang = local_recipe[lang]
            docker_lang = docker_recipe[lang]

            # Comparar cada campo
            for field in ["title", "description", "ingredients", "instructions"]:
                if local_lang.get(field) != docker_lang.get(field):
                    differences.append(
                        f"⚠️  Diferencia en {recipe_title} ({lang}) - {field}"
                    )
                    if len(local_lang.get(field, "")) < 100:
                        differences.append(f"   Local: {local_lang.get(field, '')}")
                        differences.append(f"   Docker: {docker_lang.get(field, '')}")

    # Mostrar diferencias
    if differences:
        print(f"\n❌ Se encontraron {len(differences)} diferencias:")
        for diff in differences[:20]:  # Mostrar solo las primeras 20
            print(diff)
        if len(differences) > 20:
            print(f"... y {len(differences) - 20} más")
    else:
        print("✅ No se encontraron diferencias. Las traducciones son idénticas!")

    return len(differences) == 0


def generate_sample_translations():
    """Generar muestras de traducciones para verificación rápida."""
    print("🔍 Generando muestras de traducciones...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Algunas recetas de muestra
    sample_recipes = ["Alcachofas Rellenas", "Batido de Coco", "Tarta de Queso"]

    for recipe_title in sample_recipes:
        print(f"\n📋 {recipe_title}:")
        cursor.execute(
            """
            SELECT rt.language, rt.title, rt.ingredients, rt.instructions
            FROM recipes r
            JOIN recipe_translations rt ON r.id = rt.recipe_id
            WHERE r.title = ?
            ORDER BY rt.language
        """,
            (recipe_title,),
        )

        for row in cursor.fetchall():
            lang, title, ingredients, instructions = row
            print(f"  {lang}: {title}")
            print(f"    Ingredientes: {ingredients[:50]}...")
            print(f"    Instrucciones: {instructions[:50]}...")

    conn.close()


def main():
    """Función principal."""
    print("Translation Comparison Tool")
    print("=" * 50)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "export":
            export_translations_to_json()
        elif command == "compare":
            if len(sys.argv) >= 4:
                compare_translations(sys.argv[2], sys.argv[3])
            else:
                print("Uso: python script.py compare <archivo_local> <archivo_docker>")
        elif command == "sample":
            generate_sample_translations()
        else:
            print("Comandos disponibles: export, compare, sample")
    else:
        print("Uso:")
        print("  python script.py export - Exportar traducciones actuales")
        print("  python script.py compare <local> <docker> - Comparar archivos")
        print("  python script.py sample - Mostrar muestras de traducciones")


if __name__ == "__main__":
    main()
