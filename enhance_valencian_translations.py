#!/usr/bin/env python3
"""
Script to enhance Valencian translations with better La Ribera Alta dialect
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Enhanced Valencian translations with La Ribera Alta dialect improvements
ENHANCED_VALENCIAN_TITLES = {
    # Recipes with specific improvements
    148: "Pollarda o Pollastre amb Pomes",
    149: "Corona de Xai",
    150: "Arengades Rostides en Vi",
    152: "Ous al Curri",
    153: "Rosada amb Tomàtigues",
    154: "Llenguado Farcit de Gambes i Bolets",
    155: "Filet Estrogonoff",
    156: "Canelons en Salsa de Formatge",
    158: "Pizza Napolitana",
    159: "Budín de Peix",
    160: "Peix al Forn amb Vi",
    161: "Calamarins en la seua Tinta Dana-Ona",
    162: "Pintxo Dana-Ona",
    163: "Peix al Forn amb Salsa Holandesa",
    164: "Budín de Lluç",
    165: "Carxofes Farcides",
    166: "Soufflé d'Espàrrecs",
    167: "Còctel de Tomàtigues",
    168: "Paté de Pollastre",
    169: "Pizza Napolitana (Versió 2)",
    170: "Pastís de Formatge",
    171: "Gelat de Maduixes",
    172: "Pastís de Bicarbonat de la Tia Josefina",
    173: "Pastís de Xocolata de la Tia Marita",
    174: "Batut de Llimona o Taronja",
    175: "Batut de Plàtan",
    176: "Batut de Coco",
    177: "Pastís de Xocolata i Nata",
    178: "Flam de Coco",
    179: "Pastís de Llimona Pepita",
    180: "Pastís Teresa Ferri",
    181: "Pastís de Poma Lolita",
    182: "Moca",
    183: "Flam de Coco (Versió 2)",
    184: "Galetes Farcides",
    185: "Crema Pastissera",
    186: "Pomes Rostides",
    187: "Gelat de Coco",
    188: "Crema de Xocolata",
    189: "Xocolata per a Adorn al Bany",
    190: "Creps",
    191: "Budín de Poma",
    192: "Pastís de Taronja Donat",
    193: "Pastís de Pinya",
    194: "Pastís de Bicarbonat Pepica",
    195: "Pastís de Poma Tirol",
    196: "Pastís de Cansalada i Formatge",
    197: "Pastís de Melmelada, Maduixa i Nata",
    198: "Pastís de Pinya i Nata",
    199: "Pastís de Nous",
    200: "Gelat de Plàtan",
    201: "Pastís de Iogurt",
    202: "Bescuit i Tortada",
    203: "Pastís de Llimona Carmela",
    204: "Pastís de Carlota",
    205: "Pastís de Formatge (Versió 2)",
    206: "Llom a la Taronja amb Olla",
    207: "Truites de Pisos",
    208: "Trufat María Teresa",
    209: "Llom Farcit",
    210: "Faisà a la Cassola",
    211: "Faisà a la Belga",
    212: "Espinacs a la Crema",
    213: "Pèsols amb Pernil",
    214: "Vedella a la Italiana",
    215: "Pastís de Ceba",
    216: "Entrepans de Lluç",
    217: "Pollastre amb Mostassa",
    218: "Lluç a la Beixamel",
    219: "Pastís de Patata",
}


def update_valencian_titles():
    """Update Valencian recipe titles with enhanced dialect"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🔶 Enhancing Valencian titles with La Ribera Alta dialect...")
    print("=" * 60)

    for recipe_id, new_title in ENHANCED_VALENCIAN_TITLES.items():
        cursor.execute(
            "UPDATE recipe_translations SET title = ? WHERE recipe_id = ? AND language = 'va'",
            (new_title, recipe_id),
        )
        print(f"✅ Updated recipe {recipe_id}: {new_title}")

    conn.commit()
    conn.close()

    print("=" * 60)
    print(f"✅ Enhanced {len(ENHANCED_VALENCIAN_TITLES)} Valencian titles!")


def enhance_ingredient_translations():
    """Enhance ingredient translations with specific Valencian terms"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("\n🔶 Enhancing ingredient translations...")
    print("=" * 60)

    # Common ingredient translations specific to La Ribera Alta
    ingredient_improvements = {
        "mantequilla": "mantega",
        "cebolla": "ceba",
        "tomate": "tomàtiga",
        "tomaca": "tomàtiga",
        "huevo": "ou",
        "huevos": "ous",
        "aceite": "oli",
        "harina": "farina",
        "azúcar": "sucre",
        "leche": "llet",
        "queso": "formatge",
        "jamón": "pernil",
        "carne": "carn",
        "pollo": "pollastre",
        "pescado": "peix",
        "patata": "patata",
        "limón": "llimona",
        "naranja": "taronja",
        "manzana": "poma",
        "fresa": "maduixa",
        "chocolate": "xocolata",
        "vino": "vi",
        "agua": "aigua",
        "sal": "sal",
        "pimienta": "pebre",
        "ajo": "all",
        "cebolleta": "cebolleta",
        "perejil": "julivert",
        "apio": "àpit",
        "zanahoria": "pastanaga",
        "pimiento": "pebrot",
        "guisantes": "pèsols",
        "judías": "mongetes",
        "garbanzos": "cigrons",
        "arroz": "arròs",
        "pasta": "pasta",
        "pan": "pa",
        "galleta": "galeta",
        "dulce": "dolç",
        "salado": "salat",
        "caliente": "calent",
        "frío": "fred",
        "Bacon": "Cansalada",
        "bacon": "cansalada",
    }

    # Get all Valencian translations
    cursor.execute(
        "SELECT recipe_id, ingredients, instructions FROM recipe_translations WHERE language = 'va'"
    )
    translations = cursor.fetchall()

    updated_count = 0

    for translation in translations:
        recipe_id = translation["recipe_id"]
        ingredients = translation["ingredients"]
        instructions = translation["instructions"]

        # Enhance ingredients
        enhanced_ingredients = ingredients
        for spanish, valencian in ingredient_improvements.items():
            enhanced_ingredients = enhanced_ingredients.replace(spanish, valencian)

        # Enhance instructions
        enhanced_instructions = instructions
        for spanish, valencian in ingredient_improvements.items():
            enhanced_instructions = enhanced_instructions.replace(spanish, valencian)

        # Update if there were changes
        if enhanced_ingredients != ingredients or enhanced_instructions != instructions:
            cursor.execute(
                "UPDATE recipe_translations SET ingredients = ?, instructions = ? WHERE recipe_id = ? AND language = 'va'",
                (enhanced_ingredients, enhanced_instructions, recipe_id),
            )
            updated_count += 1
            print(f"✅ Enhanced recipe {recipe_id}")

    conn.commit()
    conn.close()

    print("=" * 60)
    print(f"✅ Enhanced {updated_count} recipe ingredients and instructions!")


def main():
    """Main function to enhance Valencian translations"""
    print("🔶 Enhancing Valencian translations with La Ribera Alta dialect...")
    print("🔶 This will improve the quality and authenticity of the translations")
    print("=" * 70)

    update_valencian_titles()
    enhance_ingredient_translations()

    print("\n" + "=" * 70)
    print("🎉 ENHANCEMENT COMPLETE!")
    print("✅ Valencian translations now use authentic La Ribera Alta dialect")
    print("✅ Improved titles, ingredients, and instructions")
    print("✅ Ready for use in the web application")


if __name__ == "__main__":
    main()
