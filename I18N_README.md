# 🌍 Internationalization (i18n) Documentation

## Overview

The Tía Carmen's Recipes web application now supports multiple languages using Flask-Babel with professional internationalization features. Users can switch between Spanish and English seamlessly.

## Features

- **Language Selector**: Dropdown menu in the navigation bar
- **Session Persistence**: Language preference is saved in user session
- **Browser Detection**: Automatically detects user's browser language
- **Complete Translation**: All UI elements are translated
- **Flask-Babel Integration**: Professional i18n support with proper .po/.mo files
- **Fallback Support**: Graceful fallback to Spanish if translations are missing

## Supported Languages

- **Spanish (es)**: Default language
- **English (en)**: Full translation available

## Implementation

### Flask-Babel Integration

The application uses Flask-Babel 4.0+ for professional internationalization support:

```python
from flask_babel import Babel, gettext as _, ngettext, lazy_gettext

# Configuration
app.config['LANGUAGES'] = {
    'es': 'Español',
    'en': 'English'
}

babel = Babel(app)

# Context processor for template access
@app.context_processor
def inject_conf_vars():
    return dict(
        LANGUAGES=app.config['LANGUAGES'],
        CURRENT_LANGUAGE=session.get('language', 'es'),
        get_locale=get_locale,
        _=_
    )
```

### Template Usage

In Jinja2 templates, use the `_()` function for translations:

```html
<h1>{{ _('Welcome') }}</h1>
<p>{{ _('Discover traditional recipes') }}</p>
<button>{{ _('Search') }}</button>
```

## Setup Instructions

### Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Install Flask-Babel (already in requirements.txt)
pip install -r requirements.txt

# Initialize/update translations
python babel_manager.py all
```

### Using the Babel Manager

The project includes a `babel_manager.py` script for translation management:

```bash
# Extract translatable strings
python babel_manager.py extract

# Initialize a new language
python babel_manager.py init <language_code>

# Update existing translations
python babel_manager.py update

# Compile translations
python babel_manager.py compile

# Do all steps at once
python babel_manager.py all
```

## Translation Files

Translation files are located in:
```
translations/
├── es/
│   └── LC_MESSAGES/
│       ├── messages.po    # Spanish translations
│       └── messages.mo    # Compiled Spanish
└── en/
    └── LC_MESSAGES/
        ├── messages.po    # English translations
        └── messages.mo    # Compiled English
```

### File Structure

```
babel.cfg              # Babel configuration
babel_manager.py       # Translation management script
app.py                 # Main app with Flask-Babel
translations/          # Translation files
```

## Language Switching

Users can switch languages using:
1. **Language Dropdown**: Click the globe icon in the navigation
2. **URL Parameter**: Add `?language=en` or `?language=es` to any URL
3. **Direct Route**: Visit `/set_language/en` or `/set_language/es`

## Adding New Languages

### Step-by-Step Process

1. **Add language to config**:
```python
app.config['LANGUAGES'] = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français'  # New language
}
```

2. **Initialize the language**:
```bash
python babel_manager.py init fr
```

3. **Translate messages**:
Edit `translations/fr/LC_MESSAGES/messages.po` and add translations

4. **Compile translations**:
```bash
python babel_manager.py compile
```

5. **Update templates**:
Add the new language to the language selector dropdown

## Browser Language Detection

The application automatically detects the user's browser language preference:

Priority order:
1. URL parameter (`?language=en`)
2. Session storage
3. Browser language preference
4. Default (Spanish)

## Current Translations

All UI elements are translated, including:
- Navigation menu
- Search interface
- Recipe cards
- Category pages
- Recipe details
- Footer text
- Error messages
- Help text

### Recipe Content Translation

The application now includes complete translation of recipe content:

#### AI-Powered Translation System

The application uses Claude AI to provide high-quality, natural translations for recipe content:

**Translation Features:**
- **Professional Quality**: Natural, contextual translations that maintain culinary terminology
- **Complete Coverage**: Titles, descriptions, ingredients, and instructions all translated
- **Cooking Context**: Understands culinary terms and maintains recipe structure
- **Category Translation**: Automatic translation of recipe categories

**Translation Scripts:**
1. **`generate_ai_translations.py`**: Uses Claude AI for high-quality translations
2. **`generate_recipe_translations.py`**: Basic dictionary-based translation (fallback)

**Usage:**
```bash
# Generate AI-powered translations
python generate_ai_translations.py

# Generate basic translations (fallback)
python generate_recipe_translations.py
```

**Examples of AI Translation Quality:**

*Spanish Original:*
```
Título: Alcachofas Rellenas
Descripción: Alcachofas cocidas rellenas con un picadillo de magro, jamón y especias, gratinadas con bechamel y queso.
Ingredientes:
- Alcachofas
- Magro
- Jamón
- Especias
```

*AI English Translation:*
```
Title: Stuffed Artichokes
Description: Cooked artichokes stuffed with a mixture of lean meat, ham and spices, gratinated with bechamel and cheese.
Ingredients:
- Artichokes
- Lean meat
- Ham
- Spices
```

**Translation Database Schema:**

The `recipe_translations` table stores translated content:

```sql
CREATE TABLE recipe_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    language TEXT NOT NULL,
    title TEXT,
    description TEXT,
    ingredients TEXT,
    instructions TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    UNIQUE(recipe_id, language)
);
```

## Production Deployment

### Docker with Flask-Babel

The Docker image includes all translation files:

```dockerfile
# Dockerfile includes
COPY translations/ /app/translations/
COPY babel.cfg /app/
COPY babel_manager.py /app/
```

### Environment Variables

```bash
# Language-specific environment variables
BABEL_DEFAULT_LOCALE=es
BABEL_DEFAULT_TIMEZONE=UTC
```

## Testing

Test language switching:
```bash
# Start the application
python app.py

# Test URLs
curl "http://localhost:5014/?language=en"
curl "http://localhost:5014/?language=es"
curl "http://localhost:5014/set_language/en"
```

## Troubleshooting

### Translation Updates

If translations don't appear:
1. Check that .po files exist
2. Ensure .mo files are compiled: `python babel_manager.py compile`
3. Restart the Flask application

### Missing Translations

If some text isn't translated:
1. Check that the text is wrapped with `_()` in templates
2. Extract new strings: `python babel_manager.py extract`
3. Update translations: `python babel_manager.py update`
4. Add translations to .po files
5. Compile: `python babel_manager.py compile`

### Language Not Switching

1. Clear browser cache
2. Check session storage
3. Verify language is in `app.config['LANGUAGES']`
4. Check that locale selector is properly configured

## Development Workflow

### Adding New Translatable Text

1. **In Python code**: Use `_('Text to translate')`
2. **In templates**: Use `{{ _('Text to translate') }}`
3. **Extract**: `python babel_manager.py extract`
4. **Update**: `python babel_manager.py update`
5. **Translate**: Edit .po files
6. **Compile**: `python babel_manager.py compile`
7. **Test**: Restart app and test

### Translation Best Practices

- Keep strings short and simple
- Use context when necessary
- Test with longer translations (German, etc.)
- Consider pluralization for future languages
- Use meaningful variable names in templates

## Performance Considerations

- Translation loading is cached by Flask-Babel
- .mo files are compiled for faster access
- Session storage minimizes database queries
- Browser detection happens once per session

## Future Enhancements

- [ ] Recipe content translation (ingredients, instructions)
- [ ] Database-driven translations
- [ ] Admin interface for managing translations
- [ ] RTL language support
- [ ] Advanced pluralization support
- [ ] Date/time localization
- [ ] Number formatting
- [ ] More languages (French, Portuguese, Italian)

## Contributing Translations

To contribute translations:

1. Fork the repository
2. Initialize a new language: `python babel_manager.py init <lang>`
3. Translate the .po file
4. Test thoroughly
5. Submit a pull request

## Technical Details

### Flask-Babel Configuration

```python
# app.py configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.config['LANGUAGES'] = {
    'es': 'Español',
    'en': 'English'
}
```

### Locale Selection Logic

```python
def get_locale():
    # 1. URL parameter
    if 'language' in request.args:
        language = request.args['language']
        if language in app.config['LANGUAGES']:
            session['language'] = language
            return language
    
    # 2. Session storage
    if 'language' in session:
        if session['language'] in app.config['LANGUAGES']:
            return session['language']
    
    # 3. Browser language
    return request.accept_languages.best_match(
        app.config['LANGUAGES'].keys()
    ) or 'es'
```

For questions or issues, please create an issue in the GitHub repository.