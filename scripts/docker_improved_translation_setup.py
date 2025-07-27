#!/usr/bin/env python3
"""
Script mejorado para Docker que usa los sistemas de traducción que funcionan localmente.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def run_translation_systems():
    """Ejecutar los sistemas de traducción que funcionan localmente."""
    print("🔄 Ejecutando sistemas de traducción...")

    try:
        # 1. Actualizar ingredientes con traducciones completas
        print("🥕 Actualizando ingredientes...")
        from complete_ingredients_translation import (
            generate_complete_ingredients_translations,
        )

        generate_complete_ingredients_translations()

        # 2. Actualizar instrucciones con traducciones completas
        print("📋 Actualizando instrucciones...")
        from complete_instructions_translation import (
            generate_complete_instructions_translations,
        )

        generate_complete_instructions_translations()

        # 3. Expandir instrucciones en español
        print("🇪🇸 Expandiendo instrucciones en español...")
        from expand_spanish_instructions import expand_spanish_instructions

        expand_spanish_instructions()

        print("✅ Sistemas de traducción ejecutados exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error ejecutando sistemas de traducción: {e}")
        print("⚠️ Continuando sin sistemas de traducción...")
        return False


def verify_database_translations():
    """Verificar que las traducciones existan en la base de datos."""
    print("🔍 Verificando traducciones en la base de datos...")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que existan traducciones
        cursor.execute(
            """
            SELECT language, COUNT(*)
            FROM recipe_translations
            WHERE language IN ('eu', 'ca', 'en', 'zh')
            GROUP BY language
            ORDER BY language
        """
        )

        results = cursor.fetchall()
        total_translations = 0

        for lang, count in results:
            print(f"📊 {lang}: {count} traducciones")
            total_translations += count

        print(f"📊 Total: {total_translations} traducciones")

        # Verificar algunas traducciones específicas
        cursor.execute(
            """
            SELECT r.title, rt.language, rt.title, rt.ingredients, rt.instructions
            FROM recipes r
            JOIN recipe_translations rt ON r.id = rt.recipe_id
            WHERE r.title IN ('Alcachofas Rellenas', 'Batido de Coco')
            AND rt.language IN ('eu', 'en')
            ORDER BY r.title, rt.language
        """
        )

        test_results = cursor.fetchall()
        for row in test_results:
            original_title, lang, title, ingredients, instructions = row
            print(f"✅ {original_title} ({lang}): {title}")
            print(f"   Ingredientes: {ingredients[:50]}...")
            print(f"   Instrucciones: {instructions[:50]}...")

        conn.close()
        return total_translations > 0

    except Exception as e:
        print(f"❌ Error verificando traducciones: {e}")
        return False


def generate_interface_translations():
    """Generar traducciones de interfaz."""
    print("🔄 Generando traducciones de interfaz...")

    try:
        from fix_interface_translations import fix_interface_translations

        fix_interface_translations()
        print("✅ Traducciones de interfaz generadas")
        return True
    except Exception as e:
        print(f"❌ Error generando traducciones de interfaz: {e}")
        return False


def compile_mo_files():
    """Compilar archivos .mo usando msgfmt."""
    print("🔄 Compilando archivos .mo...")

    import subprocess

    languages = ["es", "eu", "ca", "en", "zh"]
    success_count = 0

    for lang in languages:
        po_file = f"translations/{lang}/LC_MESSAGES/messages.po"
        mo_file = f"translations/{lang}/LC_MESSAGES/messages.mo"

        if os.path.exists(po_file):
            try:
                # Usar msgfmt para compilar
                subprocess.run(
                    ["msgfmt", po_file, "-o", mo_file],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                print(f"✅ {lang}: {mo_file}")
                success_count += 1
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"❌ {lang}: Error compilando - {e}")
        else:
            print(f"⚠️ {lang}: No se encontró {po_file}")

    print(f"📊 Compilados {success_count}/{len(languages)} archivos .mo")
    return success_count > 0


def verify_mo_files():
    """Verificar que los archivos .mo existan y no estén vacíos."""
    print("🔍 Verificando archivos .mo...")

    languages = ["es", "eu", "ca", "en", "zh"]
    valid_files = 0

    for lang in languages:
        mo_file = f"translations/{lang}/LC_MESSAGES/messages.mo"
        if os.path.exists(mo_file):
            size = os.path.getsize(mo_file)
            if size > 0:
                print(f"✅ {mo_file} ({size} bytes)")
                valid_files += 1
            else:
                print(f"❌ {mo_file} - VACÍO")
        else:
            print(f"❌ {mo_file} - FALTANTE")

    print(f"📊 Archivos válidos: {valid_files}/{len(languages)}")
    return valid_files == len(languages)


def test_flask_babel():
    """Probar Flask-Babel con las traducciones."""
    print("🧪 Probando Flask-Babel...")

    try:
        from flask import Flask
        from flask_babel import Babel, gettext as _

        app = Flask(__name__)
        app.config["LANGUAGES"] = {
            "es": "Español",
            "ca": "Valencià",
            "en": "English",
            "zh": "中文",
            "eu": "Euskera",
        }
        app.config["BABEL_DEFAULT_LOCALE"] = "es"
        app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"

        babel = Babel()
        babel.init_app(app)

        # Probar traducción en diferentes idiomas
        test_languages = ["es", "eu", "ca", "en", "zh"]

        with app.app_context():
            for lang in test_languages:
                try:
                    # Simular cambio de idioma
                    with app.test_request_context():
                        app.config["BABEL_DEFAULT_LOCALE"] = lang
                        translated = _("View Recipe")
                        print(f"✅ {lang}: 'View Recipe' → '{translated}'")
                except Exception as e:
                    print(f"❌ {lang}: Error - {e}")
                    return False

        print("✅ Flask-Babel funcionando correctamente")
        return True

    except Exception as e:
        print(f"❌ Error probando Flask-Babel: {e}")
        return False


def main():
    """Función principal mejorada."""
    print("Docker Translation Setup (Improved)")
    print("=" * 50)

    # Inicializar base de datos
    try:
        init_database()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        sys.exit(1)

    # Ejecutar sistemas de traducción
    run_translation_systems()

    # Verificar traducciones en base de datos
    if not verify_database_translations():
        print("❌ No hay traducciones en la base de datos")
        sys.exit(1)

    # Generar traducciones de interfaz
    if not generate_interface_translations():
        print("❌ Falló la generación de traducciones de interfaz")
        sys.exit(1)

    # Compilar archivos .mo
    if not compile_mo_files():
        print("❌ Falló la compilación de archivos .mo")
        sys.exit(1)

    # Verificar archivos .mo
    if not verify_mo_files():
        print("❌ Faltan archivos .mo válidos")
        sys.exit(1)

    # Probar Flask-Babel
    if not test_flask_babel():
        print("❌ Flask-Babel no está funcionando correctamente")
        sys.exit(1)

    print("\n🎉 Configuración de traducciones completada exitosamente!")
    print("Docker está listo con traducciones funcionando correctamente.")


if __name__ == "__main__":
    main()
