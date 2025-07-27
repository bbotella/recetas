#!/usr/bin/env python3
"""
Script para actualizar traducciones desde dentro del contenedor Docker en tiempo de ejecución.
"""

import os
import sys
import signal
import subprocess

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def update_translations_runtime():
    """Actualizar traducciones en tiempo de ejecución."""
    print("🔄 Actualizando traducciones en tiempo de ejecución...")

    try:
        # Ejecutar el script de actualización forzada
        result = subprocess.run(
            [sys.executable, "scripts/docker_force_translation_update.py"],
            capture_output=True,
            text=True,
            cwd="/app",
        )

        if result.returncode == 0:
            print("✅ Traducciones actualizadas exitosamente!")
            print(result.stdout)
        else:
            print("❌ Error al actualizar traducciones:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error ejecutando actualización: {e}")
        return False

    return True


def restart_flask_app():
    """Reiniciar la aplicación Flask para aplicar cambios."""
    print("🔄 Reiniciando aplicación Flask...")

    try:
        # Enviar señal SIGHUP al proceso principal de Flask
        os.kill(1, signal.SIGHUP)
        print("✅ Aplicación reiniciada!")
    except Exception as e:
        print(f"⚠️ No se pudo reiniciar automáticamente: {e}")
        print("Por favor, reinicia el contenedor manualmente")


def main():
    """Función principal."""
    print("Docker Runtime Translation Updater")
    print("=" * 50)

    # Verificar que estamos en un contenedor
    if not os.path.exists("/.dockerenv"):
        print(
            "⚠️ Este script está diseñado para ejecutarse dentro de un contenedor Docker"
        )

    # Actualizar traducciones
    if update_translations_runtime():
        print("\n🎉 Traducciones actualizadas!")
        print("Recomendación: Reinicia el contenedor para aplicar todos los cambios")
    else:
        print("\n❌ Falló la actualización de traducciones")
        sys.exit(1)


if __name__ == "__main__":
    main()
