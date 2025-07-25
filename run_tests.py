#!/usr/bin/env python3
"""
Simple test runner to validate the testing infrastructure.
"""
import sys
import os
import tempfile
import sqlite3
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_test_environment():
    """Set up test environment variables and database."""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['DATABASE_PATH'] = db_path
    os.environ['FLASK_ENV'] = 'testing'
    
    return db_fd, db_path

def test_database_operations():
    """Test basic database operations."""
    try:
        from database import init_database, get_all_recipes, search_recipes
        
        # Initialize database
        init_database()
        
        # Test getting all recipes
        recipes = get_all_recipes()
        assert len(recipes) > 0, "Should have recipes in database"
        
        # Test search functionality
        search_results = search_recipes("Test")
        assert isinstance(search_results, list), "Search should return a list"
        
        print("✓ Database operations test passed")
        return True
        
    except Exception as e:
        print(f"✗ Database operations test failed: {e}")
        return False

def test_flask_application():
    """Test Flask application functionality."""
    try:
        from app import create_app_for_testing
        
        # Create test app
        app = create_app_for_testing()
        
        with app.test_client() as client:
            # Test index route
            response = client.get('/')
            assert response.status_code == 200, f"Index route failed: {response.status_code}"
            
            # Test health check
            response = client.get('/health')
            assert response.status_code == 200, f"Health check failed: {response.status_code}"
            
            # Test language switching
            response = client.get('/set_language/en')
            assert response.status_code == 302, f"Language switch failed: {response.status_code}"
            
        print("✓ Flask application test passed")
        return True
        
    except Exception as e:
        print(f"✗ Flask application test failed: {e}")
        return False

def test_internationalization():
    """Test internationalization functionality."""
    try:
        from app import create_app_for_testing
        from database import init_database
        
        # Initialize database first
        init_database()
        
        app = create_app_for_testing()
        
        with app.test_client() as client:
            with app.app_context():
                # Test Spanish (default)
                response = client.get('/recipe/1')
                if response.status_code == 302:
                    # Recipe might not exist, try index
                    response = client.get('/')
                assert response.status_code == 200, f"Spanish route failed: {response.status_code}"
                
                # Test English
                client.get('/set_language/en')
                response = client.get('/')
                assert response.status_code == 200, f"English route failed: {response.status_code}"
                
                # Test Chinese
                client.get('/set_language/zh')
                response = client.get('/')
                assert response.status_code == 200, f"Chinese route failed: {response.status_code}"
            
        print("✓ Internationalization test passed")
        return True
        
    except Exception as e:
        print(f"✗ Internationalization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running basic test suite...")
    print("=" * 50)
    
    # Setup test environment
    db_fd, db_path = setup_test_environment()
    
    try:
        # Run tests
        tests = [
            test_database_operations,
            test_flask_application,
            test_internationalization
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            if test():
                passed += 1
            else:
                failed += 1
        
        print("=" * 50)
        print(f"Test Results: {passed} passed, {failed} failed")
        
        if failed > 0:
            print("Some tests failed. Check the output above for details.")
            sys.exit(1)
        else:
            print("All tests passed!")
            
    finally:
        # Clean up temporary database
        os.close(db_fd)
        os.unlink(db_path)

if __name__ == "__main__":
    main()