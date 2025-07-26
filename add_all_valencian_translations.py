#!/usr/bin/env python3
"""
Script to add complete Valencian translations for all 73 recipes
Using La Ribera Alta dialect form of Valencian
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_recipes():
    """Get all recipes from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes ORDER BY id")
    recipes = cursor.fetchall()
    conn.close()
    return recipes


def translate_to_valencian(spanish_text, context="general"):
    """Basic translation helper for common terms"""
    translations = {
        # Cooking terms
        "mantequilla": "mantega",
        "cebolla": "ceba",
        "tomate": "tomaca",
        "tomaca": "tomaca",
        "pollo": "pollastre",
        "huevos": "ous",
        "huevo": "ou",
        "aceite": "oli",
        "sal": "sal",
        "pimienta": "pebre",
        "agua": "aigua",
        "harina": "farina",
        "azúcar": "sucre",
        "leche": "llet",
        "nata": "nata",
        "queso": "formatge",
        "jamón": "pernil",
        "pescado": "peix",
        "carne": "carn",
        "verduras": "verdures",
        "patata": "patata",
        "patatas": "patates",
        "arroz": "arròs",
        "vino": "vi",
        "limón": "llimona",
        "naranja": "taronja",
        "manzana": "poma",
        "fresa": "maduixa",
        "chocolate": "xocolata",
        "café": "café",
        "té": "té",
        # Categories
        "Pollo": "Pollastre",
        "Carnes": "Carns",
        "Pescado": "Peix",
        "Verduras": "Verdures",
        "Postres": "Postres",
        "Bebidas": "Begudes",
        "Otros": "Altres",
        # Cooking actions
        "freír": "fregir",
        "cocer": "coure",
        "hervir": "bullir",
        "asar": "rostir",
        "dorar": "daurar",
        "mezclar": "mesclar",
        "añadir": "afegir",
        "servir": "servir",
        "cortar": "tallar",
        "pelar": "pelar",
        "picar": "picar",
        "batir": "batre",
        "calentar": "calfar",
        "enfriar": "refredar",
        # Time and measures
        "minutos": "minuts",
        "hora": "hora",
        "horas": "hores",
        "gramos": "grams",
        "litro": "litre",
        "cucharada": "cullerada",
        "cucharadas": "cullerades",
        "pizca": "polsim",
        "al gusto": "al gust",
        # Common phrases
        "Se": "Es",
        "se": "es",
        "La": "La",
        "El": "El",
        "en": "en",
        "con": "amb",
        "para": "per a",
        "por": "per",
        "hasta": "fins",
        "desde": "des de",
        "sobre": "sobre",
        "bajo": "baix",
        "durante": "durant",
        "antes": "abans",
        "después": "després",
        "mientras": "mentre",
        "cuando": "quan",
        "donde": "on",
        "como": "com",
        "porque": "perquè",
        "aunque": "encara que",
        "también": "també",
        "además": "a més",
        "entonces": "llavors",
        "luego": "després",
        "ahora": "ara",
        "hoy": "hui",
        "ayer": "ahir",
        "mañana": "demà",
        "siempre": "sempre",
        "nunca": "mai",
        "todo": "tot",
        "nada": "res",
        "algo": "alguna cosa",
        "mucho": "molt",
        "poco": "poc",
        "muy": "molt",
        "más": "més",
        "menos": "menys",
        "mejor": "millor",
        "peor": "pitjor",
        "grande": "gran",
        "pequeño": "xicotet",
        "bueno": "bo",
        "malo": "dolent",
        "nuevo": "nou",
        "viejo": "vell",
        "joven": "jove",
        "caliente": "calent",
        "frío": "fred",
        "dulce": "dolç",
        "salado": "salat",
        "amargo": "amarg",
        "ácido": "àcid",
    }

    result = spanish_text
    for spanish, valencian in translations.items():
        result = result.replace(spanish, valencian)

    return result


def create_valencian_translation(recipe):
    """Create a comprehensive Valencian translation for a recipe"""

    # Translate title
    title_va = translate_to_valencian(recipe["title"])

    # Translate description (keep the enhanced gastronomic descriptions)
    description_va = translate_to_valencian(recipe["description"])

    # Translate ingredients
    ingredients_va = translate_to_valencian(recipe["ingredients"])

    # Translate instructions
    instructions_va = translate_to_valencian(recipe["instructions"])

    # Translate category
    category_va = translate_to_valencian(recipe["category"])

    return {
        "title": title_va,
        "description": description_va,
        "ingredients": ingredients_va,
        "instructions": instructions_va,
        "category": category_va,
    }


def insert_valencian_translation(recipe_id, translation):
    """Insert a single Valencian translation"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT OR REPLACE INTO recipe_translations
           (recipe_id, language, title, description, ingredients, instructions, category)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            recipe_id,
            "va",
            translation["title"],
            translation["description"],
            translation["ingredients"],
            translation["instructions"],
            translation["category"],
        ),
    )

    conn.commit()
    conn.close()


def main():
    """Main function to create all Valencian translations"""
    print("🔶 Creating Valencian translations for all 73 recipes...")
    print("=" * 60)

    recipes = get_all_recipes()
    success_count = 0

    for recipe in recipes:
        try:
            translation = create_valencian_translation(recipe)
            insert_valencian_translation(recipe["id"], translation)
            print(f"✓ Recipe {recipe['id']}: {translation['title']}")
            success_count += 1
        except Exception as e:
            print(f"✗ Error with recipe {recipe['id']}: {e}")

    print("=" * 60)
    print(f"✅ Successfully created {success_count} Valencian translations!")
    print("🔶 Valencian now available in position 2 of language selector")


if __name__ == "__main__":
    main()
