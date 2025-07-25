"""
Pytest configuration and fixtures for the Tía Carmen's Recipes application.
"""

import os
import tempfile
import pytest
from flask import Flask
from flask_babel import Babel
import sqlite3

# Import the application modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app_for_testing
from database import init_database, get_db_connection


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Create app with testing configuration
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'DATABASE_PATH': db_path,
        'SECRET_KEY': 'test-secret-key',
        'LANGUAGES': {
            'es': 'Español',
            'en': 'English',
            'zh': '中文'
        },
        'BABEL_DEFAULT_LOCALE': 'es',
        'BABEL_DEFAULT_TIMEZONE': 'UTC'
    })
    
    # Configure Babel
    babel = Babel()
    
    def get_locale():
        return 'es'
    
    babel.init_app(app, locale_selector=get_locale)
    
    # Initialize database with test data
    with app.app_context():
        # Temporarily set the database path for testing
        import database
        original_db_path = database.DATABASE_PATH
        database.DATABASE_PATH = db_path
        
        init_database()
        
        # Add test data
        conn = get_db_connection()
        
        # Insert test recipes
        test_recipes = [
            {
                'title': 'Test Recipe 1',
                'description': 'Test description 1',
                'ingredients': 'Test ingredients 1',
                'instructions': 'Test instructions 1',
                'category': 'Postres',
                'filename': 'test_recipe_1.md'
            },
            {
                'title': 'Test Recipe 2',
                'description': 'Test description 2',
                'ingredients': 'Test ingredients 2',
                'instructions': 'Test instructions 2',
                'category': 'Pollo',
                'filename': 'test_recipe_2.md'
            },
            {
                'title': 'Chicken Test',
                'description': 'Chicken test description',
                'ingredients': 'Chicken, spices',
                'instructions': 'Cook chicken',
                'category': 'Pollo',
                'filename': 'chicken_test.md'
            }
        ]
        
        for recipe in test_recipes:
            conn.execute('''
                INSERT INTO recipes (title, description, ingredients, instructions, category, filename)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (recipe['title'], recipe['description'], recipe['ingredients'], 
                  recipe['instructions'], recipe['category'], recipe['filename']))
        
        # Insert test translations
        conn.execute('''
            INSERT INTO recipe_translations (recipe_id, language, title, description, ingredients, instructions, category)
            VALUES (1, 'en', 'Test Recipe 1 EN', 'Test description 1 EN', 'Test ingredients 1 EN', 'Test instructions 1 EN', 'Desserts')
        ''')
        
        conn.execute('''
            INSERT INTO recipe_translations (recipe_id, language, title, description, ingredients, instructions, category)
            VALUES (1, 'zh', 'Test Recipe 1 ZH', 'Test description 1 ZH', 'Test ingredients 1 ZH', 'Test instructions 1 ZH', '甜点')
        ''')
        
        conn.commit()
        conn.close()
        
        # Restore original database path
        database.DATABASE_PATH = original_db_path
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def db_connection(app):
    """Get a database connection for the test database."""
    with app.app_context():
        conn = get_db_connection()
        yield conn
        conn.close()


# Mock data fixtures
@pytest.fixture
def sample_recipes():
    """Sample recipe data for testing."""
    return [
        {
            'id': 1,
            'title': 'Test Recipe 1',
            'description': 'Test description 1',
            'ingredients': 'Test ingredients 1',
            'instructions': 'Test instructions 1',
            'category': 'Postres',
            'filename': 'test_recipe_1.md'
        },
        {
            'id': 2,
            'title': 'Test Recipe 2',
            'description': 'Test description 2',
            'ingredients': 'Test ingredients 2',
            'instructions': 'Test instructions 2',
            'category': 'Pollo',
            'filename': 'test_recipe_2.md'
        }
    ]


@pytest.fixture
def sample_translations():
    """Sample translation data for testing."""
    return [
        {
            'recipe_id': 1,
            'language': 'en',
            'title': 'Test Recipe 1 EN',
            'description': 'Test description 1 EN',
            'ingredients': 'Test ingredients 1 EN',
            'instructions': 'Test instructions 1 EN',
            'category': 'Desserts'
        },
        {
            'recipe_id': 1,
            'language': 'zh',
            'title': 'Test Recipe 1 ZH',
            'description': 'Test description 1 ZH',
            'ingredients': 'Test ingredients 1 ZH',
            'instructions': 'Test instructions 1 ZH',
            'category': '甜点'
        }
    ]