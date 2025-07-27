"""
Unit tests for database.py functions.
"""

import pytest

from database import (
    init_database,
    get_db_connection,
    get_all_recipes,
    get_recipe_by_id,
    search_recipes,
    get_categories,
    get_recipe_translation,
    get_recipe_with_translation,
    get_all_recipes_with_translation,
    search_recipes_with_translation,
    save_recipe_translation,
)


class TestDatabaseInitialization:
    """Test database initialization and setup."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_init_database_creates_tables(self, app):
        """Test that init_database creates all required tables."""
        with app.app_context():
            # Get connection and check if tables exist
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check recipes table
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='recipes'"
            )
            assert cursor.fetchone() is not None

            # Check recipe_translations table
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='recipe_translations'"
            )
            assert cursor.fetchone() is not None

            # Check indexes
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_title'"
            )
            assert cursor.fetchone() is not None

            conn.close()

    @pytest.mark.unit
    @pytest.mark.database
    def test_init_database_creates_correct_schema(self, app):
        """Test that tables have the correct schema."""
        with app.app_context():
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check recipes table schema
            cursor.execute("PRAGMA table_info(recipes)")
            columns = [column[1] for column in cursor.fetchall()]
            expected_columns = [
                "id",
                "title",
                "description",
                "ingredients",
                "instructions",
                "category",
                "filename",
                "created_at",
            ]
            for col in expected_columns:
                assert col in columns

            # Check recipe_translations table schema
            cursor.execute("PRAGMA table_info(recipe_translations)")
            columns = [column[1] for column in cursor.fetchall()]
            expected_columns = [
                "id",
                "recipe_id",
                "language",
                "title",
                "description",
                "ingredients",
                "instructions",
                "category",
                "created_at",
            ]
            for col in expected_columns:
                assert col in columns

            conn.close()


class TestRecipeOperations:
    """Test basic recipe CRUD operations."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_all_recipes(self, app):
        """Test getting all recipes."""
        with app.app_context():
            recipes = get_all_recipes()
            assert len(recipes) >= 3  # We have at least 3 test recipes
            assert all("title" in recipe for recipe in recipes)
            assert all("description" in recipe for recipe in recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_by_id(self, app):
        """Test getting a recipe by ID."""
        with app.app_context():
            recipe = get_recipe_by_id(1)
            assert recipe is not None
            assert recipe["title"] == "Test Recipe 1"
            assert recipe["description"] == "Test description 1"

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_by_id_nonexistent(self, app):
        """Test getting a non-existent recipe."""
        with app.app_context():
            recipe = get_recipe_by_id(999)
            assert recipe is None

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_recipes_by_title(self, app):
        """Test searching recipes by title."""
        with app.app_context():
            recipes = search_recipes("Test Recipe 1")
            assert len(recipes) >= 1
            assert any("Test Recipe 1" in recipe["title"] for recipe in recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_recipes_by_ingredients(self, app):
        """Test searching recipes by ingredients."""
        with app.app_context():
            recipes = search_recipes("Chicken")
            assert len(recipes) >= 1
            assert any("Chicken" in recipe["ingredients"] for recipe in recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_recipes_with_category(self, app):
        """Test searching recipes with category filter."""
        with app.app_context():
            recipes = search_recipes("Test", category="Pollo")
            assert len(recipes) >= 1
            assert all(recipe["category"] == "Pollo" for recipe in recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_recipes_no_results(self, app):
        """Test searching recipes with no results."""
        with app.app_context():
            recipes = search_recipes("NonExistentRecipe")
            assert len(recipes) == 0

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_categories(self, app):
        """Test getting all categories."""
        with app.app_context():
            categories = get_categories()
            assert len(categories) >= 2  # We have at least Postres and Pollo
            assert "Postres" in categories
            assert "Pollo" in categories


class TestTranslationOperations:
    """Test translation-related database operations."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_translation(self, app):
        """Test getting a recipe translation."""
        with app.app_context():
            translation = get_recipe_translation(1, "en")
            assert translation is not None
            assert translation["title"] == "Test Recipe 1 EN"
            assert translation["language"] == "en"

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_translation_nonexistent(self, app):
        """Test getting a non-existent translation."""
        with app.app_context():
            translation = get_recipe_translation(1, "fr")
            assert translation is None

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_with_translation_spanish(self, app):
        """Test getting recipe with Spanish (default) translation."""
        with app.app_context():
            recipe = get_recipe_with_translation(1, "es")
            assert recipe is not None
            assert recipe["title"] == "Test Recipe 1"  # Original Spanish

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_with_translation_english(self, app):
        """Test getting recipe with English translation."""
        with app.app_context():
            recipe = get_recipe_with_translation(1, "en")
            assert recipe is not None
            assert recipe["title"] == "Test Recipe 1 EN"  # Translated

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_with_translation_fallback(self, app):
        """Test getting recipe with fallback to original when translation doesn't exist."""
        with app.app_context():
            recipe = get_recipe_with_translation(
                2, "en"
            )  # Recipe 2 has no English translation
            assert recipe is not None
            assert recipe["title"] == "Test Recipe 2"  # Falls back to original

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_all_recipes_with_translation_spanish(self, app):
        """Test getting all recipes with Spanish translations."""
        with app.app_context():
            recipes = get_all_recipes_with_translation("es")
            assert len(recipes) >= 3
            # Should return original Spanish recipes
            assert any(recipe["title"] == "Test Recipe 1" for recipe in recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_all_recipes_with_translation_english(self, app):
        """Test getting all recipes with English translations."""
        with app.app_context():
            recipes = get_all_recipes_with_translation("en")
            assert len(recipes) >= 3
            # Should return mix of translated and original
            titles = [recipe["title"] for recipe in recipes]
            assert "Test Recipe 1 EN" in titles  # Translated
            assert "Test Recipe 2" in titles  # Original (no translation)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_recipes_with_translation(self, app):
        """Test searching recipes with translations."""
        with app.app_context():
            recipes = search_recipes_with_translation("Test", language="en")
            assert len(recipes) >= 1
            # Should find both translated and original recipes
            titles = [recipe["title"] for recipe in recipes]
            assert any("Test Recipe 1 EN" in title for title in titles)

    @pytest.mark.unit
    @pytest.mark.database
    def test_save_recipe_translation_new(self, app):
        """Test saving a new recipe translation."""
        with app.app_context():
            # Save new translation
            save_recipe_translation(
                recipe_id=2,
                language="en",
                title="Test Recipe 2 EN",
                description="Test description 2 EN",
                ingredients="Test ingredients 2 EN",
                instructions="Test instructions 2 EN",
                category="Chicken",
            )

            # Verify it was saved
            translation = get_recipe_translation(2, "en")
            assert translation is not None
            assert translation["title"] == "Test Recipe 2 EN"

    @pytest.mark.unit
    @pytest.mark.database
    def test_save_recipe_translation_update(self, app):
        """Test updating an existing recipe translation."""
        with app.app_context():
            # Update existing translation
            save_recipe_translation(
                recipe_id=1,
                language="en",
                title="Updated Test Recipe 1 EN",
                description="Updated description",
                ingredients="Updated ingredients",
                instructions="Updated instructions",
                category="Updated Desserts",
            )

            # Verify it was updated
            translation = get_recipe_translation(1, "en")
            assert translation is not None
            assert translation["title"] == "Updated Test Recipe 1 EN"
            assert translation["description"] == "Updated description"


class TestDatabaseErrorHandling:
    """Test database error handling and edge cases."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_db_connection_returns_connection(self, app):
        """Test that get_db_connection returns a valid connection."""
        with app.app_context():
            conn = get_db_connection()
            assert conn is not None
            assert hasattr(conn, "execute")
            assert hasattr(conn, "commit")
            conn.close()

    @pytest.mark.unit
    @pytest.mark.database
    def test_database_connection_row_factory(self, app):
        """Test that database connections use row factory."""
        with app.app_context():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes LIMIT 1")
            row = cursor.fetchone()

            # Should be able to access columns by name
            assert hasattr(row, "keys")
            assert "title" in row.keys()
            assert "description" in row.keys()

            conn.close()

    @pytest.mark.unit
    @pytest.mark.database
    def test_empty_search_query(self, app):
        """Test searching with empty query."""
        with app.app_context():
            recipes = search_recipes("")
            # Should return all recipes when query is empty
            assert len(recipes) >= 3

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_special_characters(self, app):
        """Test searching with special characters."""
        with app.app_context():
            recipes = search_recipes("Test's Recipe")
            # Should handle special characters without crashing
            assert isinstance(recipes, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_recipe_with_translation_nonexistent_recipe(self, app):
        """Test getting translation for non-existent recipe."""
        with app.app_context():
            recipe = get_recipe_with_translation(999, "en")
            assert recipe is None
