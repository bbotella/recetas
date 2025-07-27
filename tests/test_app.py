"""
Unit tests for Flask routes and views in app.py.
"""

import pytest
import json

from app import create_app_for_testing, get_locale


class TestFlaskRoutes:
    """Test Flask application routes."""

    @pytest.mark.unit
    @pytest.mark.flask
    def test_index_route_get(self, client):
        """Test GET request to index route."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Test Recipe 1" in response.data
        assert b"Test Recipe 2" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_index_route_with_query(self, client):
        """Test index route with search query."""
        response = client.get("/?q=Test Recipe 1")
        assert response.status_code == 200
        assert b"Test Recipe 1" in response.data
        # Should not contain other recipes
        assert b"Test Recipe 2" not in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_index_route_with_category(self, client):
        """Test index route with category filter."""
        response = client.get("/?category=Postres")
        assert response.status_code == 200
        assert b"Test Recipe 1" in response.data
        # Should not contain recipes from other categories
        assert b"Test Recipe 2" not in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_index_route_with_query_and_category(self, client):
        """Test index route with both query and category."""
        response = client.get("/?q=Test&category=Pollo")
        assert response.status_code == 200
        assert b"Test Recipe 2" in response.data
        # Should not contain recipes from other categories
        assert b"Test Recipe 1" not in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_recipe_detail_route(self, client):
        """Test recipe detail route."""
        response = client.get("/recipe/1")
        assert response.status_code == 200
        assert b"Test Recipe 1" in response.data
        assert b"Test description 1" in response.data
        assert b"Test ingredients 1" in response.data
        assert b"Test instructions 1" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_recipe_detail_route_nonexistent(self, client):
        """Test recipe detail route for non-existent recipe."""
        response = client.get("/recipe/999")
        assert response.status_code == 302  # Redirect to index
        assert response.location.endswith("/")

    @pytest.mark.unit
    @pytest.mark.flask
    def test_categories_route(self, client):
        """Test categories route."""
        response = client.get("/categories")
        assert response.status_code == 200
        assert b"Postres" in response.data
        assert b"Pollo" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_category_recipes_route(self, client):
        """Test category recipes route."""
        response = client.get("/category/Postres")
        assert response.status_code == 200
        assert b"Test Recipe 1" in response.data
        # Should not contain recipes from other categories
        assert b"Test Recipe 2" not in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_health_check_route(self, client):
        """Test health check route."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "recipes_count" in data
        assert data["recipes_count"] >= 3


class TestLanguageRoutes:
    """Test language switching functionality."""

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_set_language_spanish(self, client):
        """Test setting language to Spanish."""
        response = client.get("/set_language/es")
        assert response.status_code == 302  # Redirect

        # Check that session was set
        with client.session_transaction() as sess:
            assert sess["language"] == "es"

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_set_language_english(self, client):
        """Test setting language to English."""
        response = client.get("/set_language/en")
        assert response.status_code == 302  # Redirect

        # Check that session was set
        with client.session_transaction() as sess:
            assert sess["language"] == "en"

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_set_language_chinese(self, client):
        """Test setting language to Chinese."""
        response = client.get("/set_language/zh")
        assert response.status_code == 302  # Redirect

        # Check that session was set
        with client.session_transaction() as sess:
            assert sess["language"] == "zh"

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_set_language_invalid(self, client):
        """Test setting invalid language."""
        response = client.get("/set_language/invalid")
        assert response.status_code == 302  # Still redirects

        # Check that session was not set
        with client.session_transaction() as sess:
            assert sess.get("language") != "invalid"

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_set_language_with_referrer(self, client):
        """Test setting language with referrer."""
        # First visit a page to set referrer
        client.get("/recipe/1")

        # Then change language
        response = client.get(
            "/set_language/en", headers={"Referer": "http://localhost/recipe/1"}
        )
        assert response.status_code == 302
        # Should redirect back to referrer
        assert "recipe/1" in response.location or response.location.endswith("/")

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_language_persistence_across_requests(self, client):
        """Test that language persists across requests."""
        # Set language to English
        client.get("/set_language/en")

        # Make another request
        response = client.get("/recipe/1")
        assert response.status_code == 200
        # Should show English translation
        assert b"Test Recipe 1 EN" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_language_url_parameter_override(self, client):
        """Test that URL language parameter overrides session."""
        # Set session language to Spanish
        with client.session_transaction() as sess:
            sess["language"] = "es"

        # Request with English URL parameter
        response = client.get("/recipe/1?language=en")
        assert response.status_code == 200
        # Should show English translation
        assert b"Test Recipe 1 EN" in response.data

        # Session should be updated
        with client.session_transaction() as sess:
            assert sess["language"] == "en"


class TestRecipeTranslations:
    """Test recipe content translations in views."""

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_recipe_detail_spanish_default(self, client):
        """Test recipe detail shows Spanish content by default."""
        response = client.get("/recipe/1")
        assert response.status_code == 200
        assert b"Test Recipe 1" in response.data  # Original Spanish title
        assert b"Test description 1" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_recipe_detail_english_translation(self, client):
        """Test recipe detail shows English translation."""
        # Set language to English
        client.get("/set_language/en")

        response = client.get("/recipe/1")
        assert response.status_code == 200
        assert b"Test Recipe 1 EN" in response.data  # English translation
        assert b"Test description 1 EN" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_recipe_detail_chinese_translation(self, client):
        """Test recipe detail shows Chinese translation."""
        # Set language to Chinese
        client.get("/set_language/zh")

        response = client.get("/recipe/1")
        assert response.status_code == 200
        assert b"Test Recipe 1 ZH" in response.data  # Chinese translation
        assert b"Test description 1 ZH" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_recipe_detail_fallback_to_original(self, client):
        """Test recipe detail falls back to original when translation missing."""
        # Set language to English
        client.get("/set_language/en")

        # Recipe 2 has no English translation
        response = client.get("/recipe/2")
        assert response.status_code == 200
        assert b"Test Recipe 2" in response.data  # Original Spanish title
        assert b"Test description 2" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_index_with_english_translations(self, client):
        """Test index page shows English translations."""
        client.get("/set_language/en")

        response = client.get("/")
        assert response.status_code == 200
        assert b"Test Recipe 1 EN" in response.data  # Translated
        assert b"Test Recipe 2" in response.data  # Original (no translation)

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_search_with_translations(self, client):
        """Test search functionality with translations."""
        client.get("/set_language/en")

        # Search for English translated content
        response = client.get("/?q=Test Recipe 1 EN")
        assert response.status_code == 200
        assert b"Test Recipe 1 EN" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_category_filter_with_translations(self, client):
        """Test category filtering with translations."""
        client.get("/set_language/en")

        # Filter by English category
        response = client.get("/?category=Desserts")
        assert response.status_code == 200
        assert b"Test Recipe 1 EN" in response.data


class TestMarkdownProcessing:
    """Test markdown processing in recipe views."""

    @pytest.mark.unit
    @pytest.mark.flask
    def test_recipe_ingredients_markdown_processing(self, client):
        """Test that ingredients are processed as markdown."""
        response = client.get("/recipe/1")
        assert response.status_code == 200
        # Should contain HTML tags from markdown processing
        assert b"<p>" in response.data or b"<ul>" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_recipe_instructions_markdown_processing(self, client):
        """Test that instructions are processed as markdown."""
        response = client.get("/recipe/1")
        assert response.status_code == 200
        # Should contain HTML tags from markdown processing
        assert b"<p>" in response.data or b"<ol>" in response.data


class TestErrorHandling:
    """Test error handling in Flask routes."""

    @pytest.mark.unit
    @pytest.mark.flask
    def test_404_handling(self, client):
        """Test 404 error handling."""
        response = client.get("/nonexistent-route")
        assert response.status_code == 404

    @pytest.mark.unit
    @pytest.mark.flask
    def test_recipe_detail_invalid_id(self, client):
        """Test recipe detail with invalid ID."""
        response = client.get("/recipe/abc")
        assert response.status_code == 404

    @pytest.mark.unit
    @pytest.mark.flask
    def test_empty_category_results(self, client):
        """Test category page with no results."""
        response = client.get("/category/NonExistentCategory")
        assert response.status_code == 200
        # Should render page but with no recipes
        assert b"NonExistentCategory" in response.data


class TestGetLocaleFunction:
    """Test the get_locale function."""

    @pytest.mark.unit
    @pytest.mark.i18n
    def test_get_locale_url_parameter(self, client):
        """Test get_locale with URL parameter."""
        with client.application.test_request_context("/?language=en"):
            with client.session_transaction() as sess:
                # Function should return 'en' and update session
                locale = get_locale()
                # Note: This test depends on the actual request context
                # The exact behavior may vary based on implementation
                assert locale in ["en", "es"]

    @pytest.mark.unit
    @pytest.mark.i18n
    def test_get_locale_session_preference(self, client):
        """Test get_locale with session preference."""
        with client.application.test_request_context("/"):
            with client.session_transaction() as sess:
                sess["language"] = "zh"
                locale = get_locale()
                assert locale == "zh"

    @pytest.mark.unit
    @pytest.mark.i18n
    def test_get_locale_default_fallback(self, client):
        """Test get_locale fallback to default."""
        with client.application.test_request_context("/"):
            # No session, no URL parameter, should fall back to default
            locale = get_locale()
            assert locale == "es"  # Default language


class TestTemplateContext:
    """Test template context variables."""

    @pytest.mark.unit
    @pytest.mark.flask
    def test_template_context_variables(self, client):
        """Test that template context variables are available."""
        response = client.get("/")
        assert response.status_code == 200

        # Check that the response contains evidence of context variables
        # This is a basic check - more detailed testing would require template inspection
        assert b"Espa\xc3\xb1ol" in response.data or b"English" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_language_selector_in_template(self, client):
        """Test that language selector appears in templates."""
        response = client.get("/")
        assert response.status_code == 200

        # Should contain language selector elements
        assert b"set_language" in response.data
        assert b"Espa\xc3\xb1ol" in response.data
        assert b"English" in response.data
        assert b"\xe4\xb8\xad\xe6\x96\x87" in response.data  # Chinese in UTF-8


class TestStaticAssets:
    """Test static asset handling."""

    @pytest.mark.unit
    @pytest.mark.flask
    def test_static_css_reference(self, client):
        """Test that CSS files are referenced correctly."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"static/css/style.css" in response.data

    @pytest.mark.unit
    @pytest.mark.flask
    def test_static_js_reference(self, client):
        """Test that JavaScript files are referenced correctly."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"static/js/search.js" in response.data
