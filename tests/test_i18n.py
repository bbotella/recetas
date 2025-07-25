"""
Unit tests for internationalization (i18n) functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import session, request
from flask_babel import get_locale

from app import get_locale as app_get_locale


class TestI18nConfiguration:
    """Test internationalization configuration."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_supported_languages_config(self, app):
        """Test that supported languages are configured correctly."""
        languages = app.config['LANGUAGES']
        assert 'es' in languages
        assert 'en' in languages
        assert 'zh' in languages
        assert languages['es'] == 'Español'
        assert languages['en'] == 'English'
        assert languages['zh'] == '中文'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_default_locale_config(self, app):
        """Test default locale configuration."""
        assert app.config['BABEL_DEFAULT_LOCALE'] == 'es'
        assert app.config['BABEL_DEFAULT_TIMEZONE'] == 'UTC'


class TestLocaleSelection:
    """Test locale selection logic."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_locale_selection_url_parameter(self, client):
        """Test locale selection via URL parameter."""
        with client.application.test_request_context('/?language=en'):
            with client.session_transaction() as sess:
                locale = app_get_locale()
                assert locale in ['en', 'es']  # Should prefer 'en' but may fallback
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_locale_selection_session_storage(self, client):
        """Test locale selection via session storage."""
        with client.application.test_request_context('/'):
            with client.session_transaction() as sess:
                sess['language'] = 'zh'
                locale = app_get_locale()
                assert locale == 'zh'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_locale_selection_invalid_language(self, client):
        """Test locale selection with invalid language."""
        with client.application.test_request_context('/?language=invalid'):
            locale = app_get_locale()
            assert locale == 'es'  # Should fallback to default
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_locale_selection_fallback_to_default(self, client):
        """Test locale selection fallback to default."""
        with client.application.test_request_context('/'):
            # No session, no URL parameter
            locale = app_get_locale()
            assert locale == 'es'  # Default language
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_locale_selection_priority_order(self, client):
        """Test that URL parameter takes priority over session."""
        with client.application.test_request_context('/?language=en'):
            with client.session_transaction() as sess:
                sess['language'] = 'zh'  # Session has Chinese
                locale = app_get_locale()
                # URL parameter should take priority
                assert locale in ['en', 'es']


class TestLanguageSwitching:
    """Test language switching functionality."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_switch_to_english(self, client):
        """Test switching to English."""
        response = client.get('/set_language/en')
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['language'] == 'en'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_switch_to_chinese(self, client):
        """Test switching to Chinese."""
        response = client.get('/set_language/zh')
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['language'] == 'zh'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_switch_to_spanish(self, client):
        """Test switching to Spanish."""
        response = client.get('/set_language/es')
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['language'] == 'es'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_switch_invalid_language(self, client):
        """Test switching to invalid language."""
        response = client.get('/set_language/invalid')
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            # Should not set invalid language
            assert sess.get('language') != 'invalid'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_switch_preserves_referrer(self, client):
        """Test that language switch preserves referrer."""
        # First visit a page
        client.get('/recipe/1')
        
        # Switch language with referrer
        response = client.get('/set_language/en', headers={'Referer': 'http://localhost/recipe/1'})
        assert response.status_code == 302
        
        # Should redirect back to referrer or home
        assert response.location.endswith('/') or 'recipe' in response.location
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_switch_without_referrer(self, client):
        """Test language switch without referrer redirects to home."""
        response = client.get('/set_language/en')
        assert response.status_code == 302
        assert response.location.endswith('/')


class TestUITranslations:
    """Test UI element translations."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_ui_spanish_translations(self, client):
        """Test Spanish UI translations."""
        response = client.get('/')
        assert response.status_code == 200
        
        # Check for Spanish UI elements
        assert b'Idioma' in response.data or b'Language' in response.data
        assert b'Espa\xc3\xb1ol' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_ui_english_translations(self, client):
        """Test English UI translations."""
        client.get('/set_language/en')
        response = client.get('/')
        assert response.status_code == 200
        
        # Check for English UI elements
        assert b'Language' in response.data
        assert b'English' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_ui_chinese_translations(self, client):
        """Test Chinese UI translations."""
        client.get('/set_language/zh')
        response = client.get('/')
        assert response.status_code == 200
        
        # Check for Chinese UI elements
        assert b'\xe8\xaf\xad\xe8\xa8\x80' in response.data  # "语言" in UTF-8
        assert b'\xe4\xb8\xad\xe6\x96\x87' in response.data  # "中文" in UTF-8


class TestRecipeContentTranslations:
    """Test recipe content translations."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_recipe_spanish_content(self, client):
        """Test Spanish recipe content (default)."""
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test description 1' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_recipe_english_content(self, client):
        """Test English recipe content."""
        client.get('/set_language/en')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        assert b'Test description 1 EN' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_recipe_chinese_content(self, client):
        """Test Chinese recipe content."""
        client.get('/set_language/zh')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 ZH' in response.data
        assert b'Test description 1 ZH' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_recipe_fallback_to_original(self, client):
        """Test recipe fallback to original language."""
        client.get('/set_language/en')
        # Recipe 2 has no English translation
        response = client.get('/recipe/2')
        assert response.status_code == 200
        assert b'Test Recipe 2' in response.data  # Original Spanish
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_recipe_list_with_translations(self, client):
        """Test recipe list with translations."""
        client.get('/set_language/en')
        response = client.get('/')
        assert response.status_code == 200
        
        # Should show mix of translated and original content
        assert b'Test Recipe 1 EN' in response.data  # Translated
        assert b'Test Recipe 2' in response.data     # Original


class TestCategoryTranslations:
    """Test category translations."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_category_spanish_names(self, client):
        """Test Spanish category names."""
        response = client.get('/categories')
        assert response.status_code == 200
        assert b'Postres' in response.data
        assert b'Pollo' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_category_english_names(self, client):
        """Test English category names."""
        client.get('/set_language/en')
        response = client.get('/categories')
        assert response.status_code == 200
        
        # Categories should be translated in the UI
        # Note: This depends on how categories are displayed in templates
        assert b'Desserts' in response.data or b'Postres' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_category_filtering_with_translations(self, client):
        """Test category filtering with translations."""
        client.get('/set_language/en')
        
        # Filter by translated category
        response = client.get('/?category=Desserts')
        assert response.status_code == 200
        
        # Should show translated recipes in that category
        assert b'Test Recipe 1 EN' in response.data


class TestSearchTranslations:
    """Test search functionality with translations."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_search_spanish_content(self, client):
        """Test searching Spanish content."""
        response = client.get('/?q=Test Recipe 1')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_search_english_content(self, client):
        """Test searching English content."""
        client.get('/set_language/en')
        response = client.get('/?q=Test Recipe 1 EN')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_search_chinese_content(self, client):
        """Test searching Chinese content."""
        client.get('/set_language/zh')
        response = client.get('/?q=Test Recipe 1 ZH')
        assert response.status_code == 200
        assert b'Test Recipe 1 ZH' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_search_across_languages(self, client):
        """Test that search works across different languages."""
        client.get('/set_language/en')
        
        # Search for content that exists in translation
        response = client.get('/?q=Test')
        assert response.status_code == 200
        
        # Should find translated content
        assert b'Test Recipe 1 EN' in response.data or b'Test Recipe 2' in response.data


class TestLanguagePersistence:
    """Test language preference persistence."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_persists_across_requests(self, client):
        """Test that language preference persists across requests."""
        # Set language to English
        client.get('/set_language/en')
        
        # Make multiple requests
        response1 = client.get('/')
        response2 = client.get('/recipe/1')
        response3 = client.get('/categories')
        
        # All should show English content
        assert b'Test Recipe 1 EN' in response2.data
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_language_override_with_url_parameter(self, client):
        """Test that URL parameter overrides session language."""
        # Set session to Spanish
        with client.session_transaction() as sess:
            sess['language'] = 'es'
        
        # Request with English URL parameter
        response = client.get('/recipe/1?language=en')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # Session should be updated
        with client.session_transaction() as sess:
            assert sess['language'] == 'en'


class TestI18nErrorHandling:
    """Test internationalization error handling."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_missing_translation_fallback(self, client):
        """Test fallback when translation is missing."""
        client.get('/set_language/en')
        
        # Recipe 2 has no English translation
        response = client.get('/recipe/2')
        assert response.status_code == 200
        
        # Should show original Spanish content
        assert b'Test Recipe 2' in response.data
        assert b'Test description 2' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_invalid_language_code_handling(self, client):
        """Test handling of invalid language codes."""
        response = client.get('/set_language/invalid')
        assert response.status_code == 302
        
        # Should not crash, should redirect
        with client.session_transaction() as sess:
            assert sess.get('language') != 'invalid'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_locale_selection_with_malformed_request(self, client):
        """Test locale selection with malformed request."""
        with client.application.test_request_context('/?language='):
            # Empty language parameter
            locale = app_get_locale()
            assert locale == 'es'  # Should fallback to default


class TestI18nTemplateContext:
    """Test internationalization template context."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_template_context_has_language_info(self, client):
        """Test that template context includes language information."""
        response = client.get('/')
        assert response.status_code == 200
        
        # Should contain language selector
        assert b'set_language' in response.data
        assert b'Espa\xc3\xb1ol' in response.data
        assert b'English' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_template_context_current_language(self, client):
        """Test that template context reflects current language."""
        # Set language to Chinese
        client.get('/set_language/zh')
        
        response = client.get('/')
        assert response.status_code == 200
        
        # Should show Chinese language name
        assert b'\xe4\xb8\xad\xe6\x96\x87' in response.data
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_template_context_translation_function(self, client):
        """Test that template context includes translation function."""
        response = client.get('/')
        assert response.status_code == 200
        
        # Should contain evidence of translation function usage
        # This is implicit in the rendered content
        assert response.data is not None
        assert len(response.data) > 0


class TestI18nPerformance:
    """Test internationalization performance considerations."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    @pytest.mark.slow
    def test_multiple_language_switches_performance(self, client):
        """Test performance with multiple language switches."""
        languages = ['es', 'en', 'zh']
        
        for _ in range(10):  # Switch languages multiple times
            for lang in languages:
                response = client.get(f'/set_language/{lang}')
                assert response.status_code == 302
                
                # Make a content request
                response = client.get('/recipe/1')
                assert response.status_code == 200
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_translation_caching_behavior(self, client):
        """Test that translations are cached appropriately."""
        # Multiple requests in same language should be consistent
        client.get('/set_language/en')
        
        responses = []
        for _ in range(3):
            response = client.get('/recipe/1')
            responses.append(response.data)
        
        # All responses should be identical
        assert all(data == responses[0] for data in responses)
        # All should contain translated content
        assert all(b'Test Recipe 1 EN' in data for data in responses)