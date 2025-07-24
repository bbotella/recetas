from flask import Flask, render_template, request, redirect, url_for
from database import init_database, get_all_recipes, search_recipes, get_recipe_by_id, get_categories
import markdown

app = Flask(__name__)

# Initialize database on startup
init_database()

@app.route('/')
def index():
    """Main page with recipe search."""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if query or category:
        recipes = search_recipes(query, category if category else None)
    else:
        recipes = get_all_recipes()
    
    categories = get_categories()
    
    return render_template('index.html', 
                         recipes=recipes, 
                         query=query, 
                         selected_category=category,
                         categories=categories)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Show detailed view of a specific recipe."""
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        return redirect(url_for('index'))
    
    # Convert markdown to HTML for better formatting
    recipe_dict = dict(recipe)
    recipe_dict['ingredients_html'] = markdown.markdown(recipe_dict['ingredients'])
    recipe_dict['instructions_html'] = markdown.markdown(recipe_dict['instructions'])
    
    return render_template('recipe.html', recipe=recipe_dict)

@app.route('/categories')
def categories():
    """Show all categories."""
    categories_list = get_categories()
    return render_template('categories.html', categories=categories_list)

@app.route('/category/<category_name>')
def category_recipes(category_name):
    """Show all recipes in a specific category."""
    recipes = search_recipes('', category_name)
    return render_template('category.html', recipes=recipes, category=category_name)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return {'status': 'healthy', 'recipes_count': len(get_all_recipes())}, 200

if __name__ == '__main__':
    import os
    # Get configuration from environment variables
    debug = os.getenv('FLASK_ENV') == 'development'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5014))
    
    app.run(debug=debug, host=host, port=port)