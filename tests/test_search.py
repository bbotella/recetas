"""
Unit tests for search and filtering functionality.
"""

import pytest
from unittest.mock import patch, MagicMock

from database import (
    search_recipes,
    search_recipes_with_translation,
    get_categories,
    get_all_recipes,
    get_all_recipes_with_translation,
)


class TestBasicSearch:
    """Test basic search functionality."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_by_title(self, app):
        """Test searching recipes by title."""
        with app.app_context():
            results = search_recipes("Test Recipe 1")
            assert len(results) >= 1
            assert any("Test Recipe 1" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_by_partial_title(self, app):
        """Test searching recipes by partial title."""
        with app.app_context():
            results = search_recipes("Test")
            assert len(results) >= 2  # Should find both test recipes
            titles = [recipe["title"] for recipe in results]
            assert any("Test Recipe 1" in title for title in titles)
            assert any("Test Recipe 2" in title for title in titles)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_by_description(self, app):
        """Test searching recipes by description."""
        with app.app_context():
            results = search_recipes("Test description 1")
            assert len(results) >= 1
            assert any(
                "Test description 1" in recipe["description"] for recipe in results
            )

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_by_ingredients(self, app):
        """Test searching recipes by ingredients."""
        with app.app_context():
            results = search_recipes("Chicken")
            assert len(results) >= 1
            assert any("Chicken" in recipe["ingredients"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_case_insensitive(self, app):
        """Test that search is case insensitive."""
        with app.app_context():
            results_lower = search_recipes("test recipe")
            results_upper = search_recipes("TEST RECIPE")
            results_mixed = search_recipes("Test Recipe")

            # Should return same results regardless of case
            assert len(results_lower) == len(results_upper) == len(results_mixed)
            assert len(results_lower) >= 2

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_empty_query(self, app):
        """Test searching with empty query."""
        with app.app_context():
            results = search_recipes("")
            all_recipes = get_all_recipes()

            # Empty query should return all recipes
            assert len(results) == len(all_recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_no_results(self, app):
        """Test searching with no matching results."""
        with app.app_context():
            results = search_recipes("NonExistentRecipe12345")
            assert len(results) == 0
            assert isinstance(results, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_special_characters(self, app):
        """Test searching with special characters."""
        with app.app_context():
            # Should not crash with special characters
            results = search_recipes("Test's Recipe & More!")
            assert isinstance(results, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_sql_injection_protection(self, app):
        """Test that search is protected against SQL injection."""
        with app.app_context():
            # Try SQL injection patterns
            malicious_queries = [
                "'; DROP TABLE recipes; --",
                "' OR '1'='1",
                "' UNION SELECT * FROM recipe_translations --",
                "'; DELETE FROM recipes; --",
            ]

            for query in malicious_queries:
                results = search_recipes(query)
                # Should not crash and should return empty results
                assert isinstance(results, list)
                assert len(results) == 0


class TestCategoryFiltering:
    """Test category filtering functionality."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_category_filter(self, app):
        """Test searching with category filter."""
        with app.app_context():
            results = search_recipes("Test", category="Postres")
            assert len(results) >= 1
            assert all(recipe["category"] == "Postres" for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_different_categories(self, app):
        """Test searching with different category filters."""
        with app.app_context():
            postres_results = search_recipes("", category="Postres")
            pollo_results = search_recipes("", category="Pollo")

            # Should return different results for different categories
            assert len(postres_results) >= 1
            assert len(pollo_results) >= 1
            assert all(recipe["category"] == "Postres" for recipe in postres_results)
            assert all(recipe["category"] == "Pollo" for recipe in pollo_results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_nonexistent_category(self, app):
        """Test searching with non-existent category."""
        with app.app_context():
            results = search_recipes("Test", category="NonExistentCategory")
            assert len(results) == 0

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_category_case_sensitive(self, app):
        """Test that category filtering is case sensitive."""
        with app.app_context():
            results_correct = search_recipes("", category="Postres")
            results_lowercase = search_recipes("", category="postres")

            # Category should be case sensitive
            assert len(results_correct) >= 1
            assert len(results_lowercase) == 0

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_categories_returns_all_categories(self, app):
        """Test that get_categories returns all available categories."""
        with app.app_context():
            categories = get_categories()
            assert len(categories) >= 2
            assert "Postres" in categories
            assert "Pollo" in categories

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_categories_returns_unique_categories(self, app):
        """Test that get_categories returns unique categories."""
        with app.app_context():
            categories = get_categories()
            unique_categories = list(set(categories))
            assert len(categories) == len(unique_categories)


class TestSearchWithTranslations:
    """Test search functionality with translations."""

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_with_translation_spanish(self, app):
        """Test searching with Spanish language."""
        with app.app_context():
            results = search_recipes_with_translation("Test Recipe 1", language="es")
            assert len(results) >= 1
            assert any("Test Recipe 1" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_with_translation_english(self, app):
        """Test searching with English language."""
        with app.app_context():
            results = search_recipes_with_translation("Test Recipe 1 EN", language="en")
            assert len(results) >= 1
            assert any("Test Recipe 1 EN" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_with_translation_chinese(self, app):
        """Test searching with Chinese language."""
        with app.app_context():
            results = search_recipes_with_translation("Test Recipe 1 ZH", language="zh")
            assert len(results) >= 1
            assert any("Test Recipe 1 ZH" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_with_translation_fallback(self, app):
        """Test search with translation fallback to original."""
        with app.app_context():
            # Search for recipe 2 in English (no translation available)
            results = search_recipes_with_translation("Test Recipe 2", language="en")
            assert len(results) >= 1
            assert any("Test Recipe 2" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_with_translation_and_category(self, app):
        """Test search with translation and category filter."""
        with app.app_context():
            results = search_recipes_with_translation(
                "Test", category="Desserts", language="en"
            )
            assert len(results) >= 1
            # Should find translated content in the specified category
            assert any("Test Recipe 1 EN" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_translated_categories(self, app):
        """Test searching with translated category names."""
        with app.app_context():
            # Search with English category name
            results = search_recipes_with_translation(
                "", category="Desserts", language="en"
            )
            assert len(results) >= 1
            assert any("Test Recipe 1 EN" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_mixed_language_content(self, app):
        """Test search returns both translated and original content."""
        with app.app_context():
            results = search_recipes_with_translation("Test", language="en")
            assert len(results) >= 2

            titles = [recipe["title"] for recipe in results]
            # Should contain both translated and original titles
            assert any("Test Recipe 1 EN" in title for title in titles)  # Translated
            assert any("Test Recipe 2" in title for title in titles)  # Original


class TestAdvancedSearch:
    """Test advanced search functionality."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_multiple_keywords(self, app):
        """Test searching with multiple keywords."""
        with app.app_context():
            results = search_recipes("Test Recipe")
            assert len(results) >= 2
            # Should find recipes containing both words
            assert any("Test Recipe 1" in recipe["title"] for recipe in results)
            assert any("Test Recipe 2" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_partial_matches(self, app):
        """Test searching with partial word matches."""
        with app.app_context():
            results = search_recipes("Rec")  # Partial match for "Recipe"
            assert len(results) >= 2
            # Should find recipes with partial matches
            titles = [recipe["title"] for recipe in results]
            assert any("Recipe" in title for title in titles)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_ingredients_content(self, app):
        """Test searching within ingredients content."""
        with app.app_context():
            results = search_recipes("spices")
            assert len(results) >= 1
            assert any("spices" in recipe["ingredients"].lower() for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_instructions_content(self, app):
        """Test searching within instructions content."""
        with app.app_context():
            results = search_recipes("Cook")
            assert len(results) >= 1
            assert any("Cook" in recipe["instructions"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_across_all_fields(self, app):
        """Test that search works across title, description, ingredients, and instructions."""
        with app.app_context():
            # Search for content that appears in different fields
            title_results = search_recipes("Test Recipe 1")  # In title
            desc_results = search_recipes("Test description")  # In description
            ingr_results = search_recipes("Test ingredients")  # In ingredients
            inst_results = search_recipes("Test instructions")  # In instructions

            assert len(title_results) >= 1
            assert len(desc_results) >= 1
            assert len(ingr_results) >= 1
            assert len(inst_results) >= 1

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_ordering_relevance(self, app):
        """Test that search results are ordered appropriately."""
        with app.app_context():
            results = search_recipes("Test Recipe")

            # Results should be ordered by title (as per current implementation)
            assert len(results) >= 2
            titles = [recipe["title"] for recipe in results]
            assert titles == sorted(titles)  # Should be alphabetically sorted


class TestSearchPerformance:
    """Test search performance and efficiency."""

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.slow
    def test_search_performance_large_query(self, app):
        """Test search performance with large query."""
        with app.app_context():
            # Repeat search multiple times to test performance
            for _ in range(10):
                results = search_recipes("Test Recipe")
                assert isinstance(results, list)
                assert len(results) >= 0

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.slow
    def test_search_with_translation_performance(self, app):
        """Test search with translation performance."""
        with app.app_context():
            languages = ["es", "en", "zh"]

            # Test search performance across different languages
            for lang in languages:
                for _ in range(5):
                    results = search_recipes_with_translation("Test", language=lang)
                    assert isinstance(results, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_empty_database_performance(self, app):
        """Test search performance with empty results."""
        with app.app_context():
            # Search for non-existent content should still be fast
            results = search_recipes("NonExistentContent123456789")
            assert len(results) == 0
            assert isinstance(results, list)


class TestSearchEdgeCases:
    """Test search edge cases and error conditions."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_none_query(self, app):
        """Test search with None query."""
        with app.app_context():
            results = search_recipes(None)
            # Should handle None gracefully
            assert isinstance(results, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_numeric_query(self, app):
        """Test search with numeric query."""
        with app.app_context():
            results = search_recipes("123")
            assert isinstance(results, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_very_long_query(self, app):
        """Test search with very long query."""
        with app.app_context():
            long_query = "a" * 1000  # Very long search query
            results = search_recipes(long_query)
            assert isinstance(results, list)
            assert len(results) == 0  # Should not find anything

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_unicode_characters(self, app):
        """Test search with Unicode characters."""
        with app.app_context():
            unicode_queries = ["café", "中文", "résumé", "naïve"]

            for query in unicode_queries:
                results = search_recipes(query)
                assert isinstance(results, list)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_whitespace_only(self, app):
        """Test search with whitespace-only query."""
        with app.app_context():
            results = search_recipes("   ")
            # Should treat as empty query
            all_recipes = get_all_recipes()
            assert len(results) == len(all_recipes)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_with_newlines_and_tabs(self, app):
        """Test search with newlines and tabs."""
        with app.app_context():
            results = search_recipes("Test\nRecipe\t1")
            assert isinstance(results, list)
            # Should handle special characters gracefully


class TestFilteringIntegration:
    """Test integration between search and filtering."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_and_filter_combination(self, app):
        """Test combination of search query and category filter."""
        with app.app_context():
            # Search with both query and category
            results = search_recipes("Test", category="Postres")
            assert len(results) >= 1
            assert all(recipe["category"] == "Postres" for recipe in results)
            assert all("Test" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_filter_without_search(self, app):
        """Test filtering without search query."""
        with app.app_context():
            results = search_recipes("", category="Pollo")
            assert len(results) >= 1
            assert all(recipe["category"] == "Pollo" for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_without_filter(self, app):
        """Test searching without category filter."""
        with app.app_context():
            results = search_recipes("Test")
            assert len(results) >= 2
            # Should return results from multiple categories
            categories = [recipe["category"] for recipe in results]
            assert len(set(categories)) >= 2  # At least 2 different categories

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_search_filter_with_translations(self, app):
        """Test search and filter combination with translations."""
        with app.app_context():
            # Search with English translation and category filter
            results = search_recipes_with_translation(
                "Test", category="Desserts", language="en"
            )
            assert len(results) >= 1

            # Should return translated content in the specified category
            assert any("Test Recipe 1 EN" in recipe["title"] for recipe in results)

    @pytest.mark.unit
    @pytest.mark.database
    def test_category_list_integrity(self, app):
        """Test that category list is consistent with recipe data."""
        with app.app_context():
            all_recipes = get_all_recipes()
            categories = get_categories()

            # All recipe categories should be in the category list
            recipe_categories = set(recipe["category"] for recipe in all_recipes)
            assert recipe_categories.issubset(set(categories))

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_result_consistency(self, app):
        """Test that search results are consistent with database state."""
        with app.app_context():
            # Search for all recipes
            all_via_search = search_recipes("")
            all_via_direct = get_all_recipes()

            # Should return same number of recipes
            assert len(all_via_search) == len(all_via_direct)

            # Should contain same recipe IDs
            search_ids = set(recipe["id"] for recipe in all_via_search)
            direct_ids = set(recipe["id"] for recipe in all_via_direct)
            assert search_ids == direct_ids
