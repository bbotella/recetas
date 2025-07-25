from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, gettext as _, ngettext, lazy_gettext, get_locale
from database import (init_database, get_all_recipes_with_translation,
                     search_recipes_with_translation, get_recipe_with_translation,
                     get_categories)
import markdown
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Babel configuration
app.config['LANGUAGES'] = {
    'es': 'Español',
    'en': 'English',
    'zh': '中文'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'


def get_locale():
    """Get the best matching locale for the user."""
    # 1. Check if language is forced in URL
    if 'language' in request.args:
        language = request.args['language']
        if language in app.config['LANGUAGES']:
            session['language'] = language
            return language

    # 2. Check if language is stored in session
    if 'language' in session:
        if session['language'] in app.config['LANGUAGES']:
            return session['language']

    # 3. Try to match browser language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'es'


# Initialize Babel with the app and configure locale selector
babel = Babel()
babel.init_app(app, locale_selector=get_locale)


# For Flask-Babel 4.0+, use the context processor approach
@app.context_processor
def inject_conf_vars():
    """Inject configuration variables into templates."""
    return dict(
        LANGUAGES=app.config['LANGUAGES'],
        CURRENT_LANGUAGE=session.get('language', 'es'),
        get_locale=get_locale,
        _=_
    )

# Initialize database on startup
init_database()

@app.route('/set_language/<language>')
def set_language(language=None):
    """Set the user's language preference."""
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))


@app.route('/')
def index():
    """Main page with recipe search."""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    current_language = get_locale()

    if query or category:
        recipes = search_recipes_with_translation(
            query, category if category else None, current_language
        )
    else:
        recipes = get_all_recipes_with_translation(current_language)

    categories = get_categories()

    return render_template('index.html',
                         recipes=recipes,
                         query=query,
                         selected_category=category,
                         categories=categories)


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Show detailed view of a specific recipe."""
    current_language = get_locale()
    recipe = get_recipe_with_translation(recipe_id, current_language)
    if not recipe:
        return redirect(url_for('index'))

    # Convert markdown to HTML for better formatting
    recipe['ingredients_html'] = markdown.markdown(recipe['ingredients'])
    recipe['instructions_html'] = markdown.markdown(recipe['instructions'])

    return render_template('recipe.html', recipe=recipe)


@app.route('/categories')
def categories():
    """Show all categories."""
    categories_list = get_categories()
    return render_template('categories.html', categories=categories_list)

@app.route('/category/<category_name>')
def category_recipes(category_name):
    """Show all recipes in a specific category."""
    current_language = get_locale()
    recipes = search_recipes_with_translation('', category_name, current_language)
    return render_template('category.html', recipes=recipes, category=category_name)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return {'status': 'healthy', 'recipes_count': len(get_all_recipes_with_translation())}, 200


def create_app_for_testing(config=None):
    """Create Flask app instance for testing."""
    test_app = Flask(__name__)
    
    # Default test configuration
    test_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'LANGUAGES': {
            'es': 'Español',
            'en': 'English',
            'zh': '中文'
        },
        'BABEL_DEFAULT_LOCALE': 'es',
        'BABEL_DEFAULT_TIMEZONE': 'UTC'
    })
    
    if config:
        test_app.config.update(config)
    
    # Configure Babel for testing
    babel_test = Babel()
    babel_test.init_app(test_app, locale_selector=get_locale)

    # Register context processor
    @test_app.context_processor
    def inject_conf_vars():
        """Inject configuration variables into templates."""
        return dict(
            LANGUAGES=test_app.config['LANGUAGES'],
            CURRENT_LANGUAGE=session.get('language', 'es'),
            get_locale=get_locale,
            _=_
        )
    
    # Register routes
    test_app.add_url_rule('/set_language/<language>', 'set_language', set_language)
    test_app.add_url_rule('/', 'index', index)
    test_app.add_url_rule('/recipe/<int:recipe_id>', 'recipe_detail', recipe_detail)
    test_app.add_url_rule('/categories', 'categories', categories)
    test_app.add_url_rule('/category/<category_name>', 'category_recipes', category_recipes)
    test_app.add_url_rule('/health', 'health_check', health_check)
    
    return test_app


if __name__ == '__main__':
    # Get configuration from environment variables
    debug = os.getenv('FLASK_ENV') == 'development'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5014))

    app.run(debug=debug, host=host, port=port)