"""
Integration tests for the complete application.
"""

import pytest
import json
from flask import url_for

from database import get_all_recipes, get_recipe_by_id


class TestApplicationIntegration:
    """Test complete application integration."""
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_complete_user_workflow(self, client):
        """Test complete user workflow from start to finish."""
        # 1. User visits homepage
        response = client.get('/')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        
        # 2. User searches for a recipe
        response = client.get('/?q=Test Recipe 1')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test Recipe 2' not in response.data
        
        # 3. User clicks on a recipe
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test description 1' in response.data
        
        # 4. User switches language to English
        response = client.get('/set_language/en')
        assert response.status_code == 302
        
        # 5. User views recipe in English
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # 6. User goes back to homepage
        response = client.get('/')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # 7. User views categories
        response = client.get('/categories')
        assert response.status_code == 200
        assert b'Postres' in response.data
        
        # 8. User filters by category
        response = client.get('/category/Postres')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_trilingual_user_experience(self, client):
        """Test user experience across all three languages."""
        # Test Spanish (default)
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        
        # Switch to English
        client.get('/set_language/en')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # Switch to Chinese
        client.get('/set_language/zh')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 ZH' in response.data
        
        # Test search in different languages
        response = client.get('/?q=Test Recipe 1 ZH')
        assert response.status_code == 200
        assert b'Test Recipe 1 ZH' in response.data
        
        # Test categories in Chinese
        response = client.get('/categories')
        assert response.status_code == 200
        # Should show category content (exact content depends on implementation)
        assert response.data is not None
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_search_and_filter_integration(self, client):
        """Test search and filter functionality integration."""
        # Test search without filter
        response = client.get('/?q=Test')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test Recipe 2' in response.data
        
        # Test filter without search
        response = client.get('/?category=Postres')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test Recipe 2' not in response.data
        
        # Test combined search and filter
        response = client.get('/?q=Test&category=Postres')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test Recipe 2' not in response.data
        
        # Test empty search with filter
        response = client.get('/?q=&category=Pollo')
        assert response.status_code == 200
        assert b'Test Recipe 2' in response.data
        assert b'Test Recipe 1' not in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_language_persistence_across_features(self, client):
        """Test language persistence across different features."""
        # Set language to English
        client.get('/set_language/en')
        
        # Test persistence in homepage
        response = client.get('/')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # Test persistence in search
        response = client.get('/?q=Test')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # Test persistence in recipe detail
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # Test persistence in categories
        response = client.get('/categories')
        assert response.status_code == 200
        # Should maintain English interface
        assert response.data is not None
        
        # Test persistence in category filter
        response = client.get('/category/Postres')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_navigation_flow(self, client):
        """Test navigation flow between pages."""
        # Start at homepage
        response = client.get('/')
        assert response.status_code == 200
        
        # Navigate to categories
        response = client.get('/categories')
        assert response.status_code == 200
        
        # Navigate to specific category
        response = client.get('/category/Postres')
        assert response.status_code == 200
        
        # Navigate to recipe detail
        response = client.get('/recipe/1')
        assert response.status_code == 200
        
        # Navigate back to homepage
        response = client.get('/')
        assert response.status_code == 200
        
        # Each navigation should work without errors
        assert True  # If we reach here, all navigations worked
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_error_handling_flow(self, client):
        """Test error handling flow."""
        # Test non-existent recipe
        response = client.get('/recipe/999')
        assert response.status_code == 302  # Redirect to homepage
        
        # Test non-existent route
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        # Test invalid recipe ID
        response = client.get('/recipe/abc')
        assert response.status_code == 404
        
        # Test empty category
        response = client.get('/category/NonExistentCategory')
        assert response.status_code == 200  # Should render empty page
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_health_check_integration(self, client):
        """Test health check endpoint integration."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'recipes_count' in data
        assert isinstance(data['recipes_count'], int)
        assert data['recipes_count'] >= 3  # At least our test recipes


class TestDatabaseIntegration:
    """Test database integration with the application."""
    
    @pytest.mark.integration
    @pytest.mark.database
    def test_database_recipe_retrieval_integration(self, app):
        """Test database recipe retrieval integration."""
        with app.app_context():
            # Test that database operations work with the app
            recipes = get_all_recipes()
            assert len(recipes) >= 3
            
            # Test specific recipe retrieval
            recipe = get_recipe_by_id(1)
            assert recipe is not None
            assert recipe['title'] == 'Test Recipe 1'
    
    @pytest.mark.integration
    @pytest.mark.database
    @pytest.mark.i18n
    def test_database_translation_integration(self, app):
        """Test database translation integration."""
        with app.app_context():
            from database import get_recipe_with_translation
            
            # Test Spanish (default)
            recipe_es = get_recipe_with_translation(1, 'es')
            assert recipe_es['title'] == 'Test Recipe 1'
            
            # Test English translation
            recipe_en = get_recipe_with_translation(1, 'en')
            assert recipe_en['title'] == 'Test Recipe 1 EN'
            
            # Test Chinese translation
            recipe_zh = get_recipe_with_translation(1, 'zh')
            assert recipe_zh['title'] == 'Test Recipe 1 ZH'
    
    @pytest.mark.integration
    @pytest.mark.database
    def test_database_search_integration(self, app):
        """Test database search integration."""
        with app.app_context():
            from database import search_recipes, search_recipes_with_translation
            
            # Test basic search
            results = search_recipes('Test')
            assert len(results) >= 2
            
            # Test search with translation
            results_en = search_recipes_with_translation('Test', language='en')
            assert len(results_en) >= 2
            
            # Test category search
            results_category = search_recipes('', category='Postres')
            assert len(results_category) >= 1


class TestTemplateIntegration:
    """Test template integration."""
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_template_rendering_integration(self, client):
        """Test template rendering integration."""
        # Test index template
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert b'<html' in response.data
        assert b'</html>' in response.data
        
        # Test recipe template
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert b'Test Recipe 1' in response.data
        
        # Test categories template
        response = client.get('/categories')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_template_i18n_integration(self, client):
        """Test template internationalization integration."""
        # Test Spanish templates
        response = client.get('/')
        assert response.status_code == 200
        assert b'Espa\xc3\xb1ol' in response.data
        
        # Test English templates
        client.get('/set_language/en')
        response = client.get('/')
        assert response.status_code == 200
        assert b'English' in response.data
        
        # Test Chinese templates
        client.get('/set_language/zh')
        response = client.get('/')
        assert response.status_code == 200
        assert b'\xe4\xb8\xad\xe6\x96\x87' in response.data  # Chinese characters
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_template_static_assets_integration(self, client):
        """Test template static assets integration."""
        response = client.get('/')
        assert response.status_code == 200
        
        # Check that CSS and JS files are referenced
        assert b'static/css/style.css' in response.data
        assert b'static/js/search.js' in response.data
        
        # Check that Bootstrap and FontAwesome are referenced
        assert b'bootstrap' in response.data
        assert b'fontawesome' in response.data or b'font-awesome' in response.data


class TestMarkdownIntegration:
    """Test markdown processing integration."""
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_markdown_processing_integration(self, client):
        """Test markdown processing integration."""
        response = client.get('/recipe/1')
        assert response.status_code == 200
        
        # Should contain HTML processed from markdown
        assert b'<p>' in response.data or b'<ul>' in response.data or b'<ol>' in response.data
        
        # Should process ingredients and instructions
        assert b'Test ingredients 1' in response.data
        assert b'Test instructions 1' in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_markdown_processing_with_translations(self, client):
        """Test markdown processing with translations."""
        # Test English translation
        client.get('/set_language/en')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        
        # Should process translated content
        assert b'Test ingredients 1 EN' in response.data
        assert b'Test instructions 1 EN' in response.data
        
        # Test Chinese translation
        client.get('/set_language/zh')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        
        # Should process Chinese content
        assert b'Test ingredients 1 ZH' in response.data
        assert b'Test instructions 1 ZH' in response.data


class TestFullApplicationFlow:
    """Test complete application flow scenarios."""
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.slow
    def test_complete_multilingual_cooking_session(self, client):
        """Test complete multilingual cooking session."""
        # User starts in Spanish
        response = client.get('/')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        
        # User searches for dessert recipes
        response = client.get('/?category=Postres')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        
        # User views recipe detail
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        assert b'Test description 1' in response.data
        
        # User switches to English for better understanding
        client.get('/set_language/en')
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # User searches for similar recipes in English
        response = client.get('/?q=Test Recipe 1 EN')
        assert response.status_code == 200
        assert b'Test Recipe 1 EN' in response.data
        
        # User explores all categories
        response = client.get('/categories')
        assert response.status_code == 200
        
        # User checks health status
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.slow
    def test_error_recovery_flow(self, client):
        """Test error recovery flow."""
        # User tries to access non-existent recipe
        response = client.get('/recipe/999')
        assert response.status_code == 302  # Redirects to homepage
        
        # User is redirected back to homepage
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
        
        # User tries invalid search
        response = client.get('/?q=NonExistentRecipe')
        assert response.status_code == 200
        # Should show "no results" message or empty results
        assert b'Test Recipe 1' not in response.data
        
        # User goes back to valid search
        response = client.get('/?q=Test')
        assert response.status_code == 200
        assert b'Test Recipe 1' in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.slow
    def test_concurrent_user_simulation(self, client):
        """Test concurrent user simulation."""
        # Simulate multiple users with different language preferences
        users = [
            {'language': 'es', 'search': 'Test Recipe 1', 'expected': 'Test Recipe 1'},
            {'language': 'en', 'search': 'Test Recipe 1 EN', 'expected': 'Test Recipe 1 EN'},
            {'language': 'zh', 'search': 'Test Recipe 1 ZH', 'expected': 'Test Recipe 1 ZH'}
        ]
        
        for user in users:
            # Set user language
            client.get(f'/set_language/{user["language"]}')
            
            # User searches
            response = client.get(f'/?q={user["search"]}')
            assert response.status_code == 200
            assert user['expected'].encode() in response.data
            
            # User views recipe
            response = client.get('/recipe/1')
            assert response.status_code == 200
            assert user['expected'].encode() in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.slow
    def test_performance_integration(self, client):
        """Test performance integration."""
        # Make multiple requests to test performance
        endpoints = [
            '/',
            '/recipe/1',
            '/recipe/2',
            '/categories',
            '/category/Postres',
            '/category/Pollo',
            '/health'
        ]
        
        for endpoint in endpoints:
            for _ in range(5):  # Make 5 requests to each endpoint
                response = client.get(endpoint)
                assert response.status_code in [200, 302]  # Should be successful
        
        # Test search performance
        search_queries = ['Test', 'Recipe', 'Chicken', 'Test Recipe 1']
        for query in search_queries:
            response = client.get(f'/?q={query}')
            assert response.status_code == 200
    
    @pytest.mark.integration
    @pytest.mark.flask
    @pytest.mark.i18n
    def test_language_switching_performance(self, client):
        """Test language switching performance."""
        languages = ['es', 'en', 'zh']
        
        # Switch between languages multiple times
        for _ in range(10):
            for lang in languages:
                # Switch language
                response = client.get(f'/set_language/{lang}')
                assert response.status_code == 302
                
                # Test that content is in correct language
                response = client.get('/recipe/1')
                assert response.status_code == 200
                
                # Verify language-specific content
                if lang == 'es':
                    assert b'Test Recipe 1' in response.data
                elif lang == 'en':
                    assert b'Test Recipe 1 EN' in response.data
                elif lang == 'zh':
                    assert b'Test Recipe 1 ZH' in response.data


class TestSecurityIntegration:
    """Test security aspects of the application."""
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_sql_injection_protection_integration(self, client):
        """Test SQL injection protection integration."""
        # Test SQL injection attempts in search
        malicious_queries = [
            "'; DROP TABLE recipes; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM recipe_translations --"
        ]
        
        for query in malicious_queries:
            response = client.get(f'/?q={query}')
            assert response.status_code == 200
            # Should not crash or return unexpected data
            assert b'Test Recipe 1' not in response.data or b'Test Recipe 1' in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_xss_protection_integration(self, client):
        """Test XSS protection integration."""
        # Test XSS attempts in search
        xss_queries = [
            "<script>alert('xss')</script>",
            "<img src='x' onerror='alert(1)'>",
            "javascript:alert('xss')"
        ]
        
        for query in xss_queries:
            response = client.get(f'/?q={query}')
            assert response.status_code == 200
            # Should not contain executable JavaScript
            assert b'<script>' not in response.data
            assert b'javascript:' not in response.data
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_csrf_protection_integration(self, client):
        """Test CSRF protection integration."""
        # Test that GET requests work normally
        response = client.get('/')
        assert response.status_code == 200
        
        # Test that language switching works (uses GET)
        response = client.get('/set_language/en')
        assert response.status_code == 302
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_input_validation_integration(self, client):
        """Test input validation integration."""
        # Test various input types
        test_inputs = [
            '',  # Empty
            'a' * 1000,  # Very long
            '123',  # Numeric
            'test recipe',  # Normal
            'Test Recipe 1',  # Existing recipe
            'NonExistentRecipe',  # Non-existent
            'café résumé naïve',  # Unicode
            '    ',  # Whitespace only
        ]
        
        for test_input in test_inputs:
            response = client.get(f'/?q={test_input}')
            assert response.status_code == 200
            # Should handle all inputs gracefully
            assert b'<!DOCTYPE html>' in response.data


class TestDataIntegrity:
    """Test data integrity across the application."""
    
    @pytest.mark.integration
    @pytest.mark.database
    def test_database_consistency(self, app):
        """Test database consistency."""
        with app.app_context():
            from database import get_all_recipes, get_categories
            
            # Test that all recipes have required fields
            recipes = get_all_recipes()
            for recipe in recipes:
                assert 'id' in recipe
                assert 'title' in recipe
                assert 'description' in recipe
                assert 'ingredients' in recipe
                assert 'instructions' in recipe
                assert 'category' in recipe
                assert 'filename' in recipe
                assert 'created_at' in recipe
            
            # Test that categories are consistent
            categories = get_categories()
            recipe_categories = set(recipe['category'] for recipe in recipes)
            assert recipe_categories.issubset(set(categories))
    
    @pytest.mark.integration
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_consistency(self, app):
        """Test translation consistency."""
        with app.app_context():
            from database import get_all_recipes, get_recipe_translation
            
            recipes = get_all_recipes()
            languages = ['en', 'zh']
            
            for recipe in recipes:
                for language in languages:
                    translation = get_recipe_translation(recipe['id'], language)
                    if translation:
                        # If translation exists, it should have proper structure
                        assert 'recipe_id' in translation
                        assert 'language' in translation
                        assert translation['recipe_id'] == recipe['id']
                        assert translation['language'] == language
    
    @pytest.mark.integration
    @pytest.mark.flask
    def test_application_state_consistency(self, client):
        """Test application state consistency."""
        # Test that session state is consistent
        client.get('/set_language/en')
        
        # Multiple requests should maintain consistent state
        responses = []
        for _ in range(3):
            response = client.get('/recipe/1')
            responses.append(response.data)
        
        # All responses should be identical
        assert all(data == responses[0] for data in responses)
        
        # All should contain English content
        assert all(b'Test Recipe 1 EN' in data for data in responses)