#!/usr/bin/env python3
"""
Script simplificado para Docker que preserva las traducciones existentes
y solo asegura que los archivos .mo se generen correctamente.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def import_translations_from_backup():
    """Importar traducciones desde archivo de backup."""
    print("📥 Importando traducciones desde backup...")

    backup_file = "translations_backup.json"
    if not os.path.exists(backup_file):
        print("⚠️ No se encontró archivo de backup, continuando sin importar")
        return True

    try:
        import json

        with open(backup_file, "r", encoding="utf-8") as f:
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


def verify_database_translations():
    """Verificar que las traducciones existan en la base de datos."""
    print("🔍 Verificando traducciones en la base de datos...")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que existan traducciones
        cursor.execute(
            """
            SELECT COUNT(*) FROM recipe_translations
            WHERE language IN ('eu', 'ca', 'en', 'zh')
        """
        )

        count = cursor.fetchone()[0]
        print(f"📊 Encontradas {count} traducciones en la base de datos")

        if count == 0:
            print("⚠️ No hay traducciones en la base de datos")
            return False

        # Verificar algunas traducciones específicas
        cursor.execute(
            """
            SELECT r.title, rt.language, rt.title
            FROM recipes r
            JOIN recipe_translations rt ON r.id = rt.recipe_id
            WHERE r.title IN ('Alcachofas Rellenas', 'Batido de Coco')
            AND rt.language IN ('eu', 'en')
            ORDER BY r.title, rt.language
        """
        )

        results = cursor.fetchall()
        for row in results:
            print(f"✅ {row[0]} ({row[1]}): {row[2]}")

        conn.close()
        return True

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
    """Compilar archivos .mo."""
    print("🔄 Compilando archivos .mo...")

    try:
        from docker_compile_translations import compile_translations

        success = compile_translations()

        if success:
            print("✅ Archivos .mo compilados exitosamente")
        else:
            print("⚠️ Problemas compilando archivos .mo")

        return success
    except Exception as e:
        print(f"❌ Error compilando archivos .mo: {e}")
        return False


def verify_mo_files():
    """Verificar que los archivos .mo existan."""
    print("🔍 Verificando archivos .mo...")

    languages = ["es", "eu", "ca", "en", "zh"]
    missing_files = []

    for lang in languages:
        mo_file = f"translations/{lang}/LC_MESSAGES/messages.mo"
        if os.path.exists(mo_file):
            print(f"✅ {mo_file}")
        else:
            print(f"❌ {mo_file} - FALTANTE")
            missing_files.append(mo_file)

    return len(missing_files) == 0


def main():
    """Función principal simplificada."""
    print("Docker Translation Setup (Simplified)")
    print("=" * 50)

    # Inicializar base de datos
    try:
        init_database()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        sys.exit(1)

    # Importar traducciones desde backup
    if not import_translations_from_backup():
        print("❌ Falló la importación de traducciones desde backup")
        sys.exit(1)

    # Verificar traducciones existentes
    if not verify_database_translations():
        print("⚠️ No hay traducciones en la base de datos, pero continuando...")

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
        print("❌ Faltan archivos .mo")
        sys.exit(1)

    print("\n🎉 Configuración de traducciones completada exitosamente!")
    print("Las traducciones están listas para usar en Docker.")


if __name__ == "__main__":
    main()
