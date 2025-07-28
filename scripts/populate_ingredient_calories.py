#!/usr/bin/env python3
"""
Populate ingredient_calories table with common Spanish ingredients.

This script adds nutritional information for ingredients commonly found
in Spanish recipes, including proteins, carbohydrates, and fats.
"""

import sqlite3
import os
import sys

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DATABASE_PATH  # noqa: E402


def populate_ingredient_calories():
    """Populate ingredient_calories table with common Spanish ingredients."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Common Spanish ingredients with nutritional info (per 100g)
    ingredients = [
        # Proteins
        ("pollo", 239, 27.3, 0.0, 13.6),
        ("ternera", 250, 26.0, 0.0, 16.0),
        ("cerdo", 242, 26.0, 0.0, 14.0),
        ("cordero", 294, 25.0, 0.0, 21.0),
        ("tocino", 541, 37.0, 1.4, 42.0),
        ("jamón", 335, 30.0, 0.1, 24.0),
        ("merluza", 92, 17.8, 0.0, 2.2),
        ("lenguado", 91, 18.8, 0.0, 1.7),
        ("gambas", 106, 18.0, 1.5, 2.2),
        ("calamares", 92, 15.6, 3.1, 1.4),
        ("arenques", 216, 19.0, 0.0, 15.0),
        ("huevos", 155, 13.0, 1.1, 11.0),
        ("queso", 402, 25.0, 1.3, 33.0),
        ("mantequilla", 717, 0.9, 0.7, 81.0),
        ("nata", 345, 2.8, 3.4, 36.0),
        ("leche", 42, 3.4, 4.8, 1.0),
        # Vegetables
        ("cebolla", 40, 1.1, 9.3, 0.1),
        ("ajo", 149, 6.4, 33.1, 0.5),
        ("zanahoria", 41, 0.9, 9.6, 0.2),
        ("tomate", 18, 0.9, 3.9, 0.2),
        ("pimiento", 31, 1.9, 6.0, 0.3),
        ("espinacas", 23, 2.9, 3.6, 0.4),
        ("alcachofas", 47, 3.3, 10.5, 0.2),
        ("espárragos", 20, 2.2, 3.9, 0.1),
        ("guisantes", 42, 5.4, 6.5, 0.4),
        ("champiñones", 22, 3.1, 3.3, 0.3),
        ("patata", 77, 2.0, 17.5, 0.1),
        # Grains & Legumes
        ("arroz", 380, 7.0, 77.0, 2.8),
        ("harina", 364, 10.3, 76.3, 1.0),
        ("pan", 265, 8.0, 49.0, 3.2),
        ("pasta", 371, 13.0, 74.0, 1.5),
        ("garbanzos", 364, 19.3, 61.0, 6.0),
        ("lentejas", 336, 23.5, 52.0, 1.9),
        # Fats & Oils
        ("aceite", 884, 0.0, 0.0, 100.0),
        ("oliva", 115, 0.8, 6.3, 11.0),
        ("manteca", 902, 0.0, 0.0, 100.0),
        # Fruits
        ("manzana", 52, 0.3, 13.8, 0.2),
        ("limón", 29, 1.1, 9.3, 0.3),
        ("naranja", 47, 0.9, 11.8, 0.1),
        ("plátano", 89, 1.1, 22.8, 0.3),
        ("piña", 50, 0.5, 13.1, 0.1),
        ("fresa", 32, 0.7, 7.7, 0.3),
        ("coco", 354, 3.3, 15.2, 33.5),
        # Nuts & Seeds
        ("almendra", 579, 21.2, 21.6, 49.9),
        ("nuez", 654, 15.2, 13.7, 65.2),
        # Dairy alternatives
        ("yogurt", 59, 10.0, 4.0, 0.4),
        # Seasonings & Spices
        ("sal", 0, 0.0, 0.0, 0.0),
        ("pimienta", 251, 10.4, 64.8, 3.3),
        ("pimentón", 282, 14.1, 53.9, 12.9),
        ("azafrán", 310, 11.4, 65.4, 5.9),
        ("perejil", 36, 3.0, 6.3, 0.8),
        # Sweets & Desserts
        ("azúcar", 387, 0.0, 99.8, 0.0),
        ("chocolate", 546, 4.9, 63.1, 31.3),
        ("miel", 304, 0.3, 82.4, 0.0),
        ("mermelada", 278, 0.4, 69.0, 0.1),
        # Beverages
        ("vino", 83, 0.1, 2.6, 0.0),
        ("cerveza", 43, 0.5, 3.6, 0.0),
        # Other common ingredients
        ("vinagre", 19, 0.0, 0.0, 0.0),
        ("bicarbonato", 0, 0.0, 0.0, 0.0),
        ("gelatina", 355, 84.4, 0.0, 0.1),
        ("maicena", 381, 0.3, 91.3, 0.7),
    ]

    # Insert ingredients into database
    for ingredient_name, calories, protein, carbs, fat in ingredients:
        cursor.execute(
            """
            INSERT OR IGNORE INTO ingredient_calories
            (ingredient_name, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g)
            VALUES (?, ?, ?, ?, ?)
            """,
            (ingredient_name, calories, protein, carbs, fat),
        )

    conn.commit()

    # Show results
    cursor.execute("SELECT COUNT(*) FROM ingredient_calories")
    count = cursor.fetchone()[0]
    print(f"✅ Successfully populated {count} ingredients in database")

    # Show some examples
    cursor.execute(
        "SELECT ingredient_name, calories_per_100g FROM ingredient_calories ORDER BY calories_per_100g DESC LIMIT 5"
    )
    print("\n🔥 Top 5 highest calorie ingredients:")
    for name, calories in cursor.fetchall():
        print(f"   {name}: {calories} cal/100g")

    conn.close()


if __name__ == "__main__":
    populate_ingredient_calories()
