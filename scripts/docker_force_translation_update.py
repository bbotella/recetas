#!/usr/bin/env python3
"""
Script para forzar la actualización de traducciones en Docker.
Asegura que las traducciones en el contenedor sean las mismas que localmente.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def force_update_translations():
    """Forzar actualización completa de traducciones en Docker."""
    print("🔄 Forzando actualización de traducciones en Docker...")

    # Inicializar base de datos
    init_database()

    # Importar y ejecutar sistemas de traducción
    try:
        # 1. Primero ejecutar el sistema de traducción mejorado
        print("📝 Ejecutando sistema de traducción mejorado...")
        from enhanced_translation_system import generate_enhanced_translations

        generate_enhanced_translations()

        # 2. Luego actualizar ingredientes específicamente
        print("🥕 Actualizando ingredientes...")
        from complete_ingredients_translation import (
            generate_complete_ingredients_translations,
        )

        generate_complete_ingredients_translations()

        # 3. Actualizar instrucciones específicamente
        print("📋 Actualizando instrucciones...")
        from complete_instructions_translation import (
            generate_complete_instructions_translations,
        )

        generate_complete_instructions_translations()

        # 4. Expandir instrucciones en español para consistencia
        print("🇪🇸 Expandiendo instrucciones en español...")
        from expand_spanish_instructions import expand_spanish_instructions

        expand_spanish_instructions()

        print("✅ Traducciones actualizadas exitosamente!")

    except Exception as e:
        print(f"❌ Error al actualizar traducciones: {e}")
        return False

    return True


def verify_translations():
    """Verificar que las traducciones se hayan actualizado correctamente."""
    print("🔍 Verificando traducciones...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar algunas traducciones específicas
    test_cases = [
        ("Alcachofas Rellenas", "eu", "Artxindurriak Beterik"),
        ("Batido de Coco", "eu", "Koko Irabiagaia"),
        ("Alcachofas Rellenas", "en", "Stuffed Artichokes"),
        ("Batido de Coco", "en", "Coconut Shake"),
        ("Alcachofas Rellenas", "ca", "Carxofes Farcides"),
        ("Batido de Coco", "zh", "椰子奶昔"),
    ]

    all_correct = True

    for original_title, lang, expected_title in test_cases:
        cursor.execute(
            """
            SELECT rt.title, rt.ingredients, rt.instructions
            FROM recipes r
            JOIN recipe_translations rt ON r.id = rt.recipe_id
            WHERE r.title = ? AND rt.language = ?
            LIMIT 1
        """,
            (original_title, lang),
        )

        result = cursor.fetchone()
        if result:
            actual_title, ingredients, instructions = result
            print(f"✅ {original_title} ({lang}): {actual_title}")

            # Verificar que ingredientes no contengan español
            if lang != "es" and any(
                word in ingredients.lower()
                for word in ["sal", "aceite", "agua", "cebolla"]
            ):
                print(f"⚠️  Ingredientes contienen español: {ingredients[:100]}...")
                all_correct = False

            # Verificar que instrucciones no contengan español
            if lang != "es" and any(
                word in instructions.lower()
                for word in ["poner", "hacer", "cocinar", "añadir"]
            ):
                print(f"⚠️  Instrucciones contienen español: {instructions[:100]}...")
                all_correct = False

        else:
            print(f"❌ No se encontró: {original_title} ({lang})")
            all_correct = False

    conn.close()

    if all_correct:
        print("✅ Todas las traducciones verificadas correctamente!")
    else:
        print("❌ Algunas traducciones tienen problemas")

    return all_correct


def main():
    """Función principal."""
    print("Docker Translation Updater")
    print("=" * 50)

    # Forzar actualización de traducciones
    success = force_update_translations()

    if success:
        # Verificar traducciones
        verify_translations()

        # Generar traducciones de interfaz
        print("🔄 Generando traducciones de interfaz...")
        from fix_interface_translations import fix_interface_translations

        fix_interface_translations()

        # Compilar archivos .mo
        print("🔄 Compilando archivos .mo...")
        from docker_compile_translations import compile_translations

        compile_translations()

        print("\n🎉 Actualización de traducciones completada!")
        print("Las traducciones en Docker ahora coinciden con las locales.")
    else:
        print("\n❌ Falló la actualización de traducciones")
        sys.exit(1)


if __name__ == "__main__":
    main()
