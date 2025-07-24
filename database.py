import sqlite3
import os

DATABASE_PATH = 'recipes.db'

def init_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create recipes table
    cursor.execute('''
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
    ''')
    
    # Create index for better search performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON recipes(title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON recipes(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ingredients ON recipes(ingredients)')
    
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
        sql = '''
            SELECT * FROM recipes 
            WHERE category = ? AND (
                title LIKE ? OR 
                description LIKE ? OR 
                ingredients LIKE ?
            )
            ORDER BY title
        '''
        params = [category, f'%{query}%', f'%{query}%', f'%{query}%']
    else:
        sql = '''
            SELECT * FROM recipes 
            WHERE title LIKE ? OR 
                  description LIKE ? OR 
                  ingredients LIKE ?
            ORDER BY title
        '''
        params = [f'%{query}%', f'%{query}%', f'%{query}%']
    
    recipes = conn.execute(sql, params).fetchall()
    conn.close()
    return recipes

def get_recipe_by_id(recipe_id):
    """Get a specific recipe by ID."""
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', [recipe_id]).fetchone()
    conn.close()
    return recipe

def get_all_recipes():
    """Get all recipes."""
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes ORDER BY title').fetchall()
    conn.close()
    return recipes

def get_categories():
    """Get all unique categories."""
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM recipes ORDER BY category').fetchall()
    conn.close()
    return [cat['category'] for cat in categories]