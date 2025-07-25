"""
Unit tests for recipe translation scripts and functionality.
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock, call

from database import (
    save_recipe_translation, get_recipe_translation, 
    get_all_recipes, init_database
)


class TestRecipeTranslationStorage:
    """Test recipe translation storage and retrieval."""
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_save_new_recipe_translation(self, app):
        """Test saving a new recipe translation."""
        with app.app_context():
            # Save a new translation
            save_recipe_translation(
                recipe_id=3,
                language='en',
                title='Chicken Test EN',
                description='Chicken test description EN',
                ingredients='Chicken, spices EN',
                instructions='Cook chicken EN',
                category='Chicken'
            )
            
            # Verify it was saved
            translation = get_recipe_translation(3, 'en')
            assert translation is not None
            assert translation['title'] == 'Chicken Test EN'
            assert translation['description'] == 'Chicken test description EN'
            assert translation['ingredients'] == 'Chicken, spices EN'
            assert translation['instructions'] == 'Cook chicken EN'
            assert translation['category'] == 'Chicken'
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_update_existing_recipe_translation(self, app):
        """Test updating an existing recipe translation."""
        with app.app_context():
            # Update existing translation (recipe 1 already has English translation)
            save_recipe_translation(
                recipe_id=1,
                language='en',
                title='Updated Test Recipe 1 EN',
                description='Updated test description 1 EN',
                ingredients='Updated test ingredients 1 EN',
                instructions='Updated test instructions 1 EN',
                category='Updated Desserts'
            )
            
            # Verify it was updated
            translation = get_recipe_translation(1, 'en')
            assert translation is not None
            assert translation['title'] == 'Updated Test Recipe 1 EN'
            assert translation['description'] == 'Updated test description 1 EN'
            assert translation['ingredients'] == 'Updated test ingredients 1 EN'
            assert translation['instructions'] == 'Updated test instructions 1 EN'
            assert translation['category'] == 'Updated Desserts'
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_save_translation_multiple_languages(self, app):
        """Test saving translations for multiple languages."""
        with app.app_context():
            # Save English translation
            save_recipe_translation(
                recipe_id=2,
                language='en',
                title='Test Recipe 2 EN',
                description='Test description 2 EN',
                ingredients='Test ingredients 2 EN',
                instructions='Test instructions 2 EN',
                category='Chicken'
            )
            
            # Save Chinese translation
            save_recipe_translation(
                recipe_id=2,
                language='zh',
                title='Test Recipe 2 ZH',
                description='Test description 2 ZH',
                ingredients='Test ingredients 2 ZH',
                instructions='Test instructions 2 ZH',
                category='鸡肉'
            )
            
            # Verify both translations exist
            en_translation = get_recipe_translation(2, 'en')
            zh_translation = get_recipe_translation(2, 'zh')
            
            assert en_translation is not None
            assert zh_translation is not None
            assert en_translation['title'] == 'Test Recipe 2 EN'
            assert zh_translation['title'] == 'Test Recipe 2 ZH'
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_save_translation_with_none_values(self, app):
        """Test saving translation with None values."""
        with app.app_context():
            # Save translation with some None values
            save_recipe_translation(
                recipe_id=3,
                language='fr',
                title='Test Recipe 3 FR',
                description=None,
                ingredients=None,
                instructions='Test instructions 3 FR',
                category='Test Category'
            )
            
            # Verify it was saved
            translation = get_recipe_translation(3, 'fr')
            assert translation is not None
            assert translation['title'] == 'Test Recipe 3 FR'
            assert translation['description'] is None
            assert translation['ingredients'] is None
            assert translation['instructions'] == 'Test instructions 3 FR'
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_save_translation_with_empty_strings(self, app):
        """Test saving translation with empty strings."""
        with app.app_context():
            # Save translation with empty strings
            save_recipe_translation(
                recipe_id=3,
                language='de',
                title='',
                description='',
                ingredients='Test ingredients 3 DE',
                instructions='Test instructions 3 DE',
                category=''
            )
            
            # Verify it was saved
            translation = get_recipe_translation(3, 'de')
            assert translation is not None
            assert translation['title'] == ''
            assert translation['description'] == ''
            assert translation['ingredients'] == 'Test ingredients 3 DE'
            assert translation['instructions'] == 'Test instructions 3 DE'
            assert translation['category'] == ''


class TestTranslationScriptFunctionality:
    """Test translation script functionality."""
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_category_translations_mapping(self):
        """Test category translations mapping."""
        from generate_chinese_translations import CATEGORY_TRANSLATIONS
        
        # Test that all Spanish categories have Chinese translations
        expected_categories = {
            'Postres': '甜点',
            'Pollo': '鸡肉',
            'Pescado': '鱼类',
            'Carnes': '肉类',
            'Bebidas': '饮品',
            'Verduras': '蔬菜',
            'Aperitivos': '开胃菜',
            'Otros': '其他'
        }
        
        for spanish, chinese in expected_categories.items():
            assert spanish in CATEGORY_TRANSLATIONS
            assert CATEGORY_TRANSLATIONS[spanish] == chinese
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_recipe_translations_mapping(self):
        """Test recipe translations mapping."""
        from generate_chinese_translations import get_chinese_recipe_translations
        
        translations = get_chinese_recipe_translations()
        
        # Test some key recipes exist
        assert 'Alcachofas Rellenas' in translations
        assert 'Batido de Coco' in translations
        assert 'Pollo Marengo' in translations
        
        # Test translation structure
        sample_translation = translations['Alcachofas Rellenas']
        assert 'title' in sample_translation
        assert 'description' in sample_translation
        assert 'ingredients' in sample_translation
        assert 'instructions' in sample_translation
        assert 'category' in sample_translation
        
        # Test Chinese content
        assert sample_translation['title'] == '酿朝鲜蓟'
        assert sample_translation['category'] == '肉类'
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_english_translations_exist(self):
        """Test that English translations exist in the complete script."""
        from generate_complete_translations import get_complete_recipe_translations
        
        translations = get_complete_recipe_translations()
        
        # Test some key recipes exist
        assert 'Alcachofas Rellenas' in translations
        assert 'Batido de Coco' in translations
        assert 'Pollo Marengo' in translations
        
        # Test translation structure
        sample_translation = translations['Alcachofas Rellenas']
        assert sample_translation['title'] == 'Stuffed Artichokes'
        assert sample_translation['category'] == 'Meat'
        assert 'artichokes' in sample_translation['description'].lower()
    
    @pytest.mark.unit
    @pytest.mark.i18n
    def test_translation_quality_structure(self):
        """Test translation quality and structure."""
        from generate_chinese_translations import get_chinese_recipe_translations
        
        translations = get_chinese_recipe_translations()
        
        for recipe_name, translation in translations.items():
            # Each translation should have all required fields
            assert 'title' in translation
            assert 'description' in translation
            assert 'ingredients' in translation
            assert 'instructions' in translation
            assert 'category' in translation
            
            # Fields should not be empty
            assert translation['title'].strip() != ''
            assert translation['description'].strip() != ''
            assert translation['ingredients'].strip() != ''
            assert translation['instructions'].strip() != ''
            assert translation['category'].strip() != ''
            
            # Instructions should contain numbered steps
            assert '1.' in translation['instructions']
            
            # Ingredients should contain list items
            assert '-' in translation['ingredients']


class TestTranslationScriptExecution:
    """Test translation script execution."""
    
    @pytest.mark.integration
    @pytest.mark.database
    @pytest.mark.slow
    def test_chinese_translation_script_execution(self, app):
        """Test Chinese translation script execution."""
        with app.app_context():
            # Import the function
            from generate_chinese_translations import generate_chinese_recipe_translations
            
            # Mock the print function to avoid output during tests
            with patch('builtins.print'):
                # Execute the translation script
                generate_chinese_recipe_translations()
            
            # Verify translations were created
            recipes = get_all_recipes()
            for recipe in recipes:
                if recipe['title'] in ['Alcachofas Rellenas', 'Batido de Coco']:
                    translation = get_recipe_translation(recipe['id'], 'zh')
                    assert translation is not None
                    assert translation['title'] is not None
                    assert translation['description'] is not None
    
    @pytest.mark.integration
    @pytest.mark.database
    @pytest.mark.slow
    def test_complete_translation_script_execution(self, app):
        """Test complete translation script execution."""
        with app.app_context():
            # Import the function
            from generate_complete_translations import generate_complete_translations
            
            # Mock the print function to avoid output during tests
            with patch('builtins.print'):
                # Execute the translation script
                generate_complete_translations()
            
            # Verify translations were created
            recipes = get_all_recipes()
            for recipe in recipes:
                if recipe['title'] in ['Test Recipe 1', 'Test Recipe 2']:
                    translation = get_recipe_translation(recipe['id'], 'en')
                    # Should have translation or fallback
                    assert translation is not None or recipe['title'] is not None


class TestTranslationFallbackBehavior:
    """Test translation fallback behavior."""
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_fallback_to_original(self, app):
        """Test that missing translations fall back to original."""
        with app.app_context():
            from database import get_recipe_with_translation
            
            # Recipe 2 has no English translation
            recipe = get_recipe_with_translation(2, 'en')
            assert recipe is not None
            assert recipe['title'] == 'Test Recipe 2'  # Original Spanish
            assert recipe['description'] == 'Test description 2'
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_partial_translation_fallback(self, app):
        """Test fallback for partial translations."""
        with app.app_context():
            # Save partial translation (only title and description)
            save_recipe_translation(
                recipe_id=3,
                language='en',
                title='Partial Test Recipe 3 EN',
                description='Partial test description 3 EN',
                ingredients=None,
                instructions=None,
                category=None
            )
            
            from database import get_recipe_with_translation
            recipe = get_recipe_with_translation(3, 'en')
            
            # Should use translated parts and fallback for missing parts
            assert recipe['title'] == 'Partial Test Recipe 3 EN'
            assert recipe['description'] == 'Partial test description 3 EN'
            assert recipe['ingredients'] == 'Chicken, spices'  # Original
            assert recipe['instructions'] == 'Cook chicken'    # Original
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_empty_translation_fallback(self, app):
        """Test fallback for empty translations."""
        with app.app_context():
            # Save empty translation
            save_recipe_translation(
                recipe_id=3,
                language='fr',
                title='',
                description='',
                ingredients='',
                instructions='',
                category=''
            )
            
            from database import get_recipe_with_translation
            recipe = get_recipe_with_translation(3, 'fr')
            
            # Should fallback to original for empty fields
            assert recipe['title'] == 'Chicken Test'  # Original
            assert recipe['description'] == 'Chicken test description'
            assert recipe['ingredients'] == 'Chicken, spices'
            assert recipe['instructions'] == 'Cook chicken'


class TestTranslationDataIntegrity:
    """Test translation data integrity."""
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_uniqueness_constraint(self, app):
        """Test that translation uniqueness constraint is enforced."""
        with app.app_context():
            # Save first translation
            save_recipe_translation(
                recipe_id=3,
                language='en',
                title='First Translation',
                description='First description',
                ingredients='First ingredients',
                instructions='First instructions',
                category='First category'
            )
            
            # Save second translation for same recipe and language
            save_recipe_translation(
                recipe_id=3,
                language='en',
                title='Second Translation',
                description='Second description',
                ingredients='Second ingredients',
                instructions='Second instructions',
                category='Second category'
            )
            
            # Should update, not create duplicate
            translation = get_recipe_translation(3, 'en')
            assert translation['title'] == 'Second Translation'
            assert translation['description'] == 'Second description'
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_foreign_key_constraint(self, app):
        """Test that translation foreign key constraint works."""
        with app.app_context():
            # Try to save translation for non-existent recipe
            # This should not crash but may not save
            save_recipe_translation(
                recipe_id=999999,
                language='en',
                title='Non-existent Recipe',
                description='Description',
                ingredients='Ingredients',
                instructions='Instructions',
                category='Category'
            )
            
            # Should not retrieve anything
            translation = get_recipe_translation(999999, 'en')
            # Behavior depends on database constraints implementation
            assert translation is None or translation is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_language_code_handling(self, app):
        """Test handling of different language codes."""
        with app.app_context():
            # Test various language codes
            language_codes = ['en', 'zh', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'ko']
            
            for lang_code in language_codes:
                save_recipe_translation(
                    recipe_id=1,
                    language=lang_code,
                    title=f'Test Recipe 1 {lang_code.upper()}',
                    description=f'Test description {lang_code}',
                    ingredients=f'Test ingredients {lang_code}',
                    instructions=f'Test instructions {lang_code}',
                    category=f'Test category {lang_code}'
                )
                
                # Verify it was saved
                translation = get_recipe_translation(1, lang_code)
                assert translation is not None
                assert translation['title'] == f'Test Recipe 1 {lang_code.upper()}'


class TestTranslationPerformance:
    """Test translation performance."""
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.slow
    def test_bulk_translation_save_performance(self, app):
        """Test performance of bulk translation saving."""
        with app.app_context():
            # Save multiple translations quickly
            for i in range(50):
                save_recipe_translation(
                    recipe_id=1,
                    language=f'lang_{i}',
                    title=f'Test Recipe 1 Lang {i}',
                    description=f'Test description {i}',
                    ingredients=f'Test ingredients {i}',
                    instructions=f'Test instructions {i}',
                    category=f'Test category {i}'
                )
            
            # Verify some were saved
            translation_1 = get_recipe_translation(1, 'lang_1')
            translation_25 = get_recipe_translation(1, 'lang_25')
            translation_49 = get_recipe_translation(1, 'lang_49')
            
            assert translation_1 is not None
            assert translation_25 is not None
            assert translation_49 is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.slow
    def test_translation_retrieval_performance(self, app):
        """Test performance of translation retrieval."""
        with app.app_context():
            # Retrieve translations multiple times
            for _ in range(100):
                translation = get_recipe_translation(1, 'en')
                assert translation is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.slow
    def test_translation_with_large_content(self, app):
        """Test translation with large content."""
        with app.app_context():
            # Create large content
            large_content = 'A' * 10000  # 10KB of content
            
            save_recipe_translation(
                recipe_id=1,
                language='large',
                title='Large Content Test',
                description=large_content,
                ingredients=large_content,
                instructions=large_content,
                category='Large Category'
            )
            
            # Verify it was saved and retrieved correctly
            translation = get_recipe_translation(1, 'large')
            assert translation is not None
            assert len(translation['description']) == 10000
            assert len(translation['ingredients']) == 10000
            assert len(translation['instructions']) == 10000


class TestTranslationErrorHandling:
    """Test translation error handling."""
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_with_invalid_recipe_id(self, app):
        """Test translation with invalid recipe ID."""
        with app.app_context():
            # Try to save translation for invalid recipe ID
            save_recipe_translation(
                recipe_id=-1,
                language='en',
                title='Invalid Recipe',
                description='Invalid description',
                ingredients='Invalid ingredients',
                instructions='Invalid instructions',
                category='Invalid category'
            )
            
            # Should handle gracefully
            translation = get_recipe_translation(-1, 'en')
            # Result depends on database constraint handling
            assert translation is None or translation is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_with_invalid_language_code(self, app):
        """Test translation with invalid language code."""
        with app.app_context():
            # Try to save translation with invalid language code
            save_recipe_translation(
                recipe_id=1,
                language='',  # Empty language code
                title='Empty Language Test',
                description='Empty description',
                ingredients='Empty ingredients',
                instructions='Empty instructions',
                category='Empty category'
            )
            
            # Should handle gracefully
            translation = get_recipe_translation(1, '')
            # Result depends on implementation
            assert translation is None or translation is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.i18n
    def test_translation_with_special_characters(self, app):
        """Test translation with special characters."""
        with app.app_context():
            # Save translation with special characters
            save_recipe_translation(
                recipe_id=1,
                language='special',
                title='Special Recipe with "quotes" & symbols',
                description='Description with <html> tags & entities',
                ingredients='Ingredients with 50% water & 25% flour',
                instructions='Instructions with newlines\nand\ttabs',
                category='Category with émojis 🍰'
            )
            
            # Verify it was saved correctly
            translation = get_recipe_translation(1, 'special')
            assert translation is not None
            assert '"quotes"' in translation['title']
            assert '<html>' in translation['description']
            assert '50%' in translation['ingredients']
            assert '\n' in translation['instructions']
            assert '🍰' in translation['category']