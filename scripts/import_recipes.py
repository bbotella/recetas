import os
import re
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_database, get_db_connection


def parse_markdown_recipe(file_path):
    """Parse a markdown recipe file and extract structured data."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title (first # header)
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(file_path)

    # Extract description (text after ## Descripción)
    desc_match = re.search(
        r"## Descripción\s*\n(.+?)(?=\n##|\n---|\Z)", content, re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract ingredients (text after ## Ingredientes)
    ingredients_match = re.search(
        r"## Ingredientes\s*\n(.+?)(?=\n## Preparación|\n---|\Z)", content, re.DOTALL
    )
    ingredients = ingredients_match.group(1).strip() if ingredients_match else ""

    # Extract instructions (text after ## Preparación)
    instructions_match = re.search(
        r"## Preparación\s*\n(.+?)(?=\n---|\Z)", content, re.DOTALL
    )
    instructions = instructions_match.group(1).strip() if instructions_match else ""

    # Determine category based on keywords
    category = categorize_recipe(title, description, ingredients)

    return {
        "title": title,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "category": category,
        "filename": os.path.basename(file_path),
    }


def categorize_recipe(title, description, ingredients):
    """Categorize recipe based on content."""
    title_lower = title.lower()
    desc_lower = description.lower()
    ing_lower = ingredients.lower()

    # Define categories and their keywords
    categories = {
        "Postres": [
            "tarta",
            "flan",
            "helado",
            "bizcocho",
            "chocolate",
            "crema",
            "moka",
            "galleta",
            "mousse",
            "puding",
        ],
        "Bebidas": ["batido", "coco", "limón", "naranja", "plátano"],
        "Pollo": ["pollo", "pularda"],
        "Pescado": [
            "pescado",
            "merluza",
            "lenguado",
            "arenque",
            "rosada",
            "bacalao",
            "calamares",
        ],
        "Carnes": ["cordero", "lomo", "ternera", "faisán", "liebre", "jamón"],
        "Verduras": [
            "espinacas",
            "alcachofas",
            "guisantes",
            "cebolla",
            "patata",
            "espárragos",
        ],
        "Aperitivos": ["cocktail", "paté", "pinchito", "emparedado", "tortilla"],
    }

    # Check each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in desc_lower or keyword in ing_lower:
                return category

    return "Otros"


def import_all_recipes():
    """Import all markdown recipes to the database."""
    init_database()

    recipes_dir = "recipes"
    if not os.path.exists(recipes_dir):
        print(f"Error: {recipes_dir} directory not found!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing recipes
    cursor.execute("DELETE FROM recipes")

    imported_count = 0

    for filename in sorted(os.listdir(recipes_dir)):
        if filename.endswith(".md"):
            file_path = os.path.join(recipes_dir, filename)
            try:
                recipe_data = parse_markdown_recipe(file_path)

                cursor.execute(
                    """
                    INSERT INTO recipes (
                        title,
                        description,
                        ingredients,
                        instructions,
                        category,
                        filename)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        recipe_data["title"],
                        recipe_data["description"],
                        recipe_data["ingredients"],
                        recipe_data["instructions"],
                        recipe_data["category"],
                        recipe_data["filename"],
                    ),
                )

                imported_count += 1
                print(f"Imported: {recipe_data['title']} ({recipe_data['category']})")

            except Exception as e:
                print(f"Error importing {filename}: {str(e)}")

    conn.commit()
    conn.close()

    print(f"\nImported {imported_count} recipes successfully!")


if __name__ == "__main__":
    import_all_recipes()
