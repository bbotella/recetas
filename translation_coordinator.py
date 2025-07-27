#!/usr/bin/env python3
"""
Script para procesar todas las traducciones usando IA directa de Claude.
Este script coordina el proceso de traducción pero las traducciones reales
las proporciona Claude usando su inteligencia artificial.
"""

import json
import os

def load_spanish_texts():
    """Cargar textos originales en español."""
    with open('texts_to_translate.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_existing_translations(language):
    """Cargar traducciones existentes."""
    filename = f'translations_{language}.json'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_translations(language, translations):
    """Guardar traducciones."""
    filename = f'translations_{language}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

def get_translation_progress():
    """Obtener progreso de traducción."""
    spanish_texts = load_spanish_texts()
    languages = ['euskera', 'english', 'chinese', 'catalan']
    
    total_recipes = len(spanish_texts)
    progress = {}
    
    for lang in languages:
        translations = load_existing_translations(lang)
        translated_count = len(translations)
        progress[lang] = {
            'translated': translated_count,
            'total': total_recipes,
            'percentage': (translated_count / total_recipes) * 100
        }
    
    return progress

def get_next_recipes_to_translate(batch_size=5):
    """Obtener las próximas recetas que necesitan traducción."""
    spanish_texts = load_spanish_texts()
    languages = ['euskera', 'english', 'chinese', 'catalan']
    
    # Encontrar recetas que faltan por traducir
    missing_recipes = {}
    
    for lang in languages:
        translations = load_existing_translations(lang)
        missing = []
        
        for recipe_id, recipe_data in spanish_texts.items():
            if recipe_id not in translations:
                missing.append({
                    'id': recipe_id,
                    'title': recipe_data['title'],
                    'description': recipe_data['description'],
                    'ingredients': recipe_data['ingredients'],
                    'instructions': recipe_data['instructions'],
                    'category': recipe_data['category']
                })
        
        missing_recipes[lang] = missing[:batch_size]
    
    return missing_recipes

def main():
    """Función principal."""
    print("=== PROGRESO DE TRADUCCIÓN ===")
    progress = get_translation_progress()
    
    for lang, data in progress.items():
        print(f"{lang}: {data['translated']}/{data['total']} ({data['percentage']:.1f}%)")
    
    print("\n=== PRÓXIMAS RECETAS A TRADUCIR ===")
    next_recipes = get_next_recipes_to_translate(5)
    
    for lang, recipes in next_recipes.items():
        print(f"\n{lang.upper()}:")
        for recipe in recipes:
            print(f"  - {recipe['id']}: {recipe['title']}")
    
    print("\n=== INSTRUCCIONES ===")
    print("Claude debe traducir las recetas mostradas arriba usando su IA.")
    print("Para cada receta, traducir: título, descripción, ingredientes, instrucciones, categoría")
    print("Las traducciones deben ser contextuales y apropiadas para cada idioma.")

if __name__ == "__main__":
    main()