import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def init_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create recipes table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            ingredients TEXT,
            instructions TEXT,
            category TEXT,
            filename TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Create recipe translations table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipe_translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            language TEXT NOT NULL,
            title TEXT,
            description TEXT,
            ingredients TEXT,
            instructions TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id),
            UNIQUE(recipe_id, language)
        )
    """
    )

    # Create index for better search performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON recipes(title)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON recipes(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ingredients ON recipes(ingredients)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_translations_recipe ON recipe_translations(recipe_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_translations_language ON recipe_translations(language)"
    )

    conn.commit()
    conn.close()


def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def search_recipes(query, category=None):
    """Search recipes by title, description, or ingredients."""
    conn = get_db_connection()

    if category:
        sql = """
            SELECT * FROM recipes
            WHERE category = ? AND (
                title LIKE ? OR
                description LIKE ? OR
                ingredients LIKE ?
            )
            ORDER BY title
        """
        params = [category, f"%{query}%", f"%{query}%", f"%{query}%"]
    else:
        sql = """
            SELECT * FROM recipes
            WHERE title LIKE ? OR
                  description LIKE ? OR
                  ingredients LIKE ?
            ORDER BY title
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]

    recipes = conn.execute(sql, params).fetchall()
    conn.close()
    return recipes


def get_recipe_by_id(recipe_id):
    """Get a specific recipe by ID."""
    conn = get_db_connection()
    recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", [recipe_id]).fetchone()
    conn.close()
    return recipe


def get_all_recipes():
    """Get all recipes."""
    conn = get_db_connection()
    recipes = conn.execute("SELECT * FROM recipes ORDER BY title").fetchall()
    conn.close()
    return recipes


def get_categories():
    """Get all unique categories."""
    conn = get_db_connection()
    categories = conn.execute(
        "SELECT DISTINCT category FROM recipes ORDER BY category"
    ).fetchall()
    conn.close()
    return [cat["category"] for cat in categories]


def get_recipe_translation(recipe_id, language):
    """Get translation for a recipe in a specific language."""
    conn = get_db_connection()
    translation = conn.execute(
        """
        SELECT * FROM recipe_translations
        WHERE recipe_id = ? AND language = ?
    """,
        [recipe_id, language],
    ).fetchone()
    conn.close()
    return translation


def get_recipe_with_translation(recipe_id, language="es"):
    """Get recipe with translation if available."""
    conn = get_db_connection()

    # Get original recipe
    recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", [recipe_id]).fetchone()
    if not recipe:
        conn.close()
        return None

    # Get translation if available and not Spanish (original language)
    if language != "es":
        translation = conn.execute(
            """
            SELECT * FROM recipe_translations
            WHERE recipe_id = ? AND language = ?
        """,
            [recipe_id, language],
        ).fetchone()

        if translation:
            # Create a merged dictionary with translated content
            recipe_dict = dict(recipe)
            recipe_dict.update(
                {
                    "title": translation["title"] or recipe["title"],
                    "description": translation["description"] or recipe["description"],
                    "ingredients": translation["ingredients"] or recipe["ingredients"],
                    "instructions": translation["instructions"]
                    or recipe["instructions"],
                    "category": translation["category"] or recipe["category"],
                }
            )
            conn.close()
            return recipe_dict

    conn.close()
    return dict(recipe)


def get_all_recipes_with_translation(language="es"):
    """Get all recipes with translations if available."""
    conn = get_db_connection()

    if language == "es":
        # Return original recipes
        recipes = conn.execute("SELECT * FROM recipes ORDER BY title").fetchall()
        conn.close()
        return recipes
    else:
        # Return recipes with translations
        recipes = conn.execute(
            """
            SELECT r.id, r.filename, r.created_at,
                   CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END as title,
                   CASE WHEN t.description IS NOT NULL THEN t.description ELSE r.description END as description,
                   CASE WHEN t.ingredients IS NOT NULL THEN t.ingredients ELSE r.ingredients END as ingredients,
                   CASE WHEN t.instructions IS NOT NULL THEN t.instructions ELSE r.instructions END as instructions,
                   CASE WHEN t.category IS NOT NULL THEN t.category ELSE r.category END as category
            FROM recipes r
            LEFT JOIN recipe_translations t ON r.id = t.recipe_id AND t.language = ?
            ORDER BY CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END
        """,
            [language],
        ).fetchall()
        conn.close()
        return recipes


def search_recipes_with_translation(query, category=None, language="es"):
    """Search recipes with translations if available."""
    conn = get_db_connection()

    if language == "es":
        # Use original search function for Spanish
        return search_recipes(query, category)
    else:
        # Search with translations
        if category:
            sql = """
                SELECT r.id, r.filename, r.created_at,
                       CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END as title,
                       CASE WHEN t.description IS NOT NULL THEN t.description ELSE r.description END as description,
                       CASE WHEN t.ingredients IS NOT NULL THEN t.ingredients ELSE r.ingredients END as ingredients,
                       CASE WHEN t.instructions IS NOT NULL THEN t.instructions ELSE r.instructions END as instructions,
                       CASE WHEN t.category IS NOT NULL THEN t.category ELSE r.category END as category
                FROM recipes r
                LEFT JOIN recipe_translations t ON r.id = t.recipe_id AND t.language = ?
                WHERE CASE WHEN t.category IS NOT NULL THEN t.category ELSE r.category END = ? AND (
                    CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END LIKE ? OR
                    CASE WHEN t.description IS NOT NULL THEN t.description ELSE r.description END LIKE ? OR
                    CASE WHEN t.ingredients IS NOT NULL THEN t.ingredients ELSE r.ingredients END LIKE ?
                )
                ORDER BY CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END
            """
            params = [language, category, f"%{query}%", f"%{query}%", f"%{query}%"]
        else:
            sql = """
                SELECT r.id, r.filename, r.created_at,
                       CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END as title,
                       CASE WHEN t.description IS NOT NULL THEN t.description ELSE r.description END as description,
                       CASE WHEN t.ingredients IS NOT NULL THEN t.ingredients ELSE r.ingredients END as ingredients,
                       CASE WHEN t.instructions IS NOT NULL THEN t.instructions ELSE r.instructions END as instructions,
                       CASE WHEN t.category IS NOT NULL THEN t.category ELSE r.category END as category
                FROM recipes r
                LEFT JOIN recipe_translations t ON r.id = t.recipe_id AND t.language = ?
                WHERE CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END LIKE ? OR
                      CASE WHEN t.description IS NOT NULL THEN t.description ELSE r.description END LIKE ? OR
                      CASE WHEN t.ingredients IS NOT NULL THEN t.ingredients ELSE r.ingredients END LIKE ?
                ORDER BY CASE WHEN t.title IS NOT NULL THEN t.title ELSE r.title END
            """
            params = [language, f"%{query}%", f"%{query}%", f"%{query}%"]

        recipes = conn.execute(sql, params).fetchall()
        conn.close()
        return recipes


def save_recipe_translation(
    recipe_id,
    language,
    title=None,
    description=None,
    ingredients=None,
    instructions=None,
    category=None,
):
    """Save or update a recipe translation."""
    conn = get_db_connection()

    # Check if translation exists
    existing = conn.execute(
        """
        SELECT id FROM recipe_translations
        WHERE recipe_id = ? AND language = ?
    """,
        [recipe_id, language],
    ).fetchone()

    if existing:
        # Update existing translation
        conn.execute(
            """
            UPDATE recipe_translations
            SET title = ?, description = ?, ingredients = ?, instructions = ?, category = ?
            WHERE recipe_id = ? AND language = ?
        """,
            [
                title,
                description,
                ingredients,
                instructions,
                category,
                recipe_id,
                language,
            ],
        )
    else:
        # Insert new translation
        conn.execute(
            """
            INSERT INTO recipe_translations (recipe_id, language, title, description,
            ingredients, instructions, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            [
                recipe_id,
                language,
                title,
                description,
                ingredients,
                instructions,
                category,
            ],
        )

    conn.commit()
    conn.close()
