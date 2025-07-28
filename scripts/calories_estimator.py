#!/usr/bin/env python3
"""
Calories estimation system for recipes.

This module provides functionality to estimate calories for recipes by parsing
ingredient lists and matching them with nutritional data.
"""

import re
import sqlite3
import os
import sys

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DATABASE_PATH  # noqa: E402


class CaloriesEstimator:
    """Estimates calories for recipes based on ingredient analysis."""

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.conn.row_factory = sqlite3.Row

        # Common Spanish quantity patterns
        self.quantity_patterns = [
            r"(\d+(?:\.\d+)?)\s*k?g",  # kg, g
            r"(\d+(?:\.\d+)?)\s*gramos?",  # gramos
            r"(\d+(?:\.\d+)?)\s*g\b",  # g
            r"(\d+(?:\.\d+)?)\s*litros?",  # litros
            r"(\d+(?:\.\d+)?)\s*l\b",  # l
            r"(\d+(?:\.\d+)?)\s*ml",  # ml
            r"(\d+(?:\.\d+)?)\s*cucharadas?",  # cucharadas
            r"(\d+(?:\.\d+)?)\s*cucharaditas?",  # cucharaditas
            r"(\d+(?:\.\d+)?)\s*tazas?",  # tazas
            r"(\d+(?:\.\d+)?)\s*unidades?",  # unidades
            r"(\d+(?:\.\d+)?)\s*piezas?",  # piezas
            r"(\d+(?:\.\d+)?)\s*lonchas?",  # lonchas
            r"(\d+(?:\.\d+)?)\s*rebanadas?",  # rebanadas
            r"(\d+(?:\.\d+)?)\s*dientes?",  # dientes de ajo
            r"(\d+(?:\.\d+)?)\s*",  # just number
        ]

        # Unit conversion to grams
        self.unit_conversions = {
            "kg": 1000,
            "g": 1,
            "gramos": 1,
            "gramo": 1,
            "litros": 1000,  # assuming 1L = 1000g for liquids
            "litro": 1000,
            "l": 1000,
            "ml": 1,  # 1ml ≈ 1g for most liquids
            "cucharadas": 15,  # 1 tablespoon ≈ 15g
            "cucharada": 15,
            "cucharaditas": 5,  # 1 teaspoon ≈ 5g
            "cucharadita": 5,
            "tazas": 200,  # 1 cup ≈ 200g
            "taza": 200,
            "unidades": 100,  # average unit weight
            "unidad": 100,
            "piezas": 100,
            "pieza": 100,
            "lonchas": 20,  # average slice
            "loncha": 20,
            "rebanadas": 30,
            "rebanada": 30,
            "dientes": 3,  # garlic clove
            "diente": 3,
        }

    def get_ingredient_calories(self, ingredient_name):
        """Get calories per 100g for an ingredient."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT calories_per_100g FROM ingredient_calories WHERE ingredient_name = ?",
            (ingredient_name.lower(),),
        )
        result = cursor.fetchone()
        return result[0] if result else None

    def find_matching_ingredient(self, ingredient_text):
        """Find matching ingredient in database using fuzzy matching."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT ingredient_name, calories_per_100g FROM ingredient_calories"
        )
        ingredients = cursor.fetchall()

        ingredient_lower = ingredient_text.lower()

        # Try exact match first
        for ingredient in ingredients:
            if ingredient[0] in ingredient_lower:
                return ingredient[0], ingredient[1]

        # Try partial matching
        for ingredient in ingredients:
            if any(word in ingredient_lower for word in ingredient[0].split()):
                return ingredient[0], ingredient[1]

        return None, None

    def extract_quantity_and_unit(self, ingredient_line):
        """Extract quantity and unit from ingredient line."""
        for pattern in self.quantity_patterns:
            match = re.search(pattern, ingredient_line, re.IGNORECASE)
            if match:
                quantity = float(match.group(1))

                # Extract unit
                unit_match = re.search(
                    r"\d+(?:\.\d+)?\s*(\w+)", ingredient_line, re.IGNORECASE
                )
                unit = unit_match.group(1).lower() if unit_match else ""

                return quantity, unit

        return None, None

    def convert_to_grams(self, quantity, unit):
        """Convert quantity and unit to grams."""
        if not quantity or not unit:
            return 100  # Default assumption

        conversion_factor = self.unit_conversions.get(unit.lower(), 1)
        return quantity * conversion_factor

    def parse_ingredients(self, ingredients_text):
        """Parse ingredients text and return list of ingredients with quantities."""
        if not ingredients_text:
            return []

        # Split by lines and filter out empty lines
        lines = [line.strip() for line in ingredients_text.split("\n") if line.strip()]

        parsed_ingredients = []

        for line in lines:
            # Skip headers and markdown formatting
            if line.startswith("#") or line.startswith("###") or line.startswith("-"):
                line = line.lstrip("#-").strip()

            if not line:
                continue

            # Extract quantity and unit
            quantity, unit = self.extract_quantity_and_unit(line)
            grams = self.convert_to_grams(quantity, unit)

            # Find matching ingredient
            ingredient_name, calories_per_100g = self.find_matching_ingredient(line)

            if ingredient_name and calories_per_100g:
                calories = (grams / 100) * calories_per_100g
                parsed_ingredients.append(
                    {
                        "original_text": line,
                        "ingredient_name": ingredient_name,
                        "quantity": quantity,
                        "unit": unit,
                        "grams": grams,
                        "calories_per_100g": calories_per_100g,
                        "total_calories": calories,
                    }
                )

        return parsed_ingredients

    def estimate_recipe_calories(self, recipe_id):
        """Estimate total calories for a recipe."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT ingredients FROM recipes WHERE id = ?", (recipe_id,))
        result = cursor.fetchone()

        if not result:
            return None

        ingredients_text = result[0]
        parsed_ingredients = self.parse_ingredients(ingredients_text)

        total_calories = sum(ing["total_calories"] for ing in parsed_ingredients)

        return {
            "recipe_id": recipe_id,
            "total_calories": int(total_calories),
            "ingredients": parsed_ingredients,
            "matched_ingredients": len(
                [ing for ing in parsed_ingredients if ing["ingredient_name"]]
            ),
            "total_ingredients": len(parsed_ingredients),
        }

    def update_recipe_calories(self, recipe_id, estimated_calories):
        """Update recipe with estimated calories."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE recipes SET estimated_calories = ? WHERE id = ?",
            (estimated_calories, recipe_id),
        )
        self.conn.commit()

    def estimate_all_recipes(self):
        """Estimate calories for all recipes in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title FROM recipes")
        recipes = cursor.fetchall()

        results = []

        for recipe in recipes:
            recipe_id, title = recipe
            estimation = self.estimate_recipe_calories(recipe_id)

            if estimation:
                self.update_recipe_calories(recipe_id, estimation["total_calories"])
                results.append(
                    {
                        "recipe_id": recipe_id,
                        "title": title,
                        "estimated_calories": estimation["total_calories"],
                        "matched_ingredients": estimation["matched_ingredients"],
                        "total_ingredients": estimation["total_ingredients"],
                    }
                )

        return results

    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """Main function to estimate calories for all recipes."""
    estimator = CaloriesEstimator()

    print("🔥 Estimating calories for all recipes...")
    results = estimator.estimate_all_recipes()

    print(f"\n✅ Processed {len(results)} recipes")
    print("\n📊 Sample results:")

    for result in results[:10]:  # Show first 10 results
        match_rate = (
            (result["matched_ingredients"] / result["total_ingredients"] * 100)
            if result["total_ingredients"] > 0
            else 0
        )
        print(
            f"   {result['title']}: {result['estimated_calories']} cal ({match_rate:.0f}% ingredients matched)"
        )

    # Show statistics
    total_calories = sum(r["estimated_calories"] for r in results)
    avg_calories = total_calories / len(results) if results else 0

    print("\n📈 Statistics:")
    print(f"   Average calories per recipe: {avg_calories:.0f} cal")
    print(f"   Total calories database: {total_calories:,} cal")

    # Show highest calorie recipes
    highest_recipes = sorted(
        results, key=lambda x: x["estimated_calories"], reverse=True
    )[:5]
    print("\n🔥 Top 5 highest calorie recipes:")
    for recipe in highest_recipes:
        print(f"   {recipe['title']}: {recipe['estimated_calories']} cal")

    estimator.close()


if __name__ == "__main__":
    main()
