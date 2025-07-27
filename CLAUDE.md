# CLAUDE.md - Project Knowledge Base

## Project Overview

**Recetas de la Tía Carmen** is a multilingual Flask web application for traditional Spanish family recipes. The application features comprehensive internationalization support (Spanish, English, Chinese), full-text search capabilities, and a modern CI/CD pipeline.

## Architecture

### Core Components

**Backend:**
- **Flask** (v2.3.3): Web framework with Jinja2 templating
- **SQLite**: Database for recipes and translations
- **Flask-Babel** (v4.0.0): Internationalization support
- **Markdown** (v3.5.1): Recipe content formatting

**Frontend:**
- **Bootstrap**: Responsive UI framework
- **FontAwesome**: Icons and visual elements
- **Custom CSS/JS**: Enhanced search and interaction

**Infrastructure:**
- **Docker**: Containerized deployment
- **GitHub Actions**: CI/CD pipeline
- **Docker Hub**: Container registry

### Database Schema

```sql
-- Main recipes table
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    ingredients TEXT,
    instructions TEXT,
    category TEXT,
    filename TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Translation support
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

### File Structure

```
tiaCarmen/
├── app.py                          # Main Flask application
├── database.py                     # Database operations
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Production container
├── Dockerfile.test                 # Testing container
├── docker-compose.yml             # Local development
├── recipes/                        # Recipe markdown files
├── static/                         # CSS, JS, images
├── templates/                      # Jinja2 templates
├── translations/                   # Flask-Babel translations
├── tests/                          # Comprehensive test suite
├── .github/workflows/              # CI/CD pipelines
├── data/                          # Database storage
└── scripts/                       # Utility scripts
```

## Key Features

### 1. Multilingual Support
- **Languages**: Spanish (default), English, Chinese (中文), Valencian (Català), Basque (Euskera)
- **Translation System**: AI-powered translation with contextual understanding
- **Dynamic Content**: Recipe translations stored in database
- **UI Localization**: Complete interface translation using Flask-Babel
- **Language Switching**: Session-based preference storage
- **CRITICAL**: All translations MUST be generated using AI models, NOT dictionaries

### 2. Recipe Management
- **Content Format**: Markdown for ingredients and instructions
- **Categories**: Organized by food type (Postres, Pollo, Pescado, etc.)
- **Search**: Full-text search across all fields
- **Filtering**: Category-based filtering
- **Translations**: Automatic and manual translation support

### 3. Search Functionality
- **Full-text Search**: Searches title, description, ingredients, instructions
- **Category Filtering**: Filter by recipe categories
- **Multilingual Search**: Search in any supported language
- **Case-insensitive**: Robust search experience
- **SQL Injection Protection**: Parameterized queries

## Development Workflow

### Local Development

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# IMPORTANT: Flask-Babel is installed in the venv
# Use the virtual environment for all translation compilation tasks

# Database initialization
python -c "from database import init_database; init_database()"

# Run application
python app.py
```

### Testing

```bash
# Quick test suite
python run_tests.py

# Full pytest suite (if available)
pytest tests/ -v --cov=.

# Coverage analysis
python coverage_report.py

# Linting
make lint  # or individual tools
```

### Docker Development

```bash
# Build and run locally
docker build -t tia-carmen .
docker run -p 5000:5000 -e FLASK_PORT=5000 tia-carmen

# Development with docker-compose
docker-compose up --build
```

## CI/CD Pipeline

### Two-Tier Workflow System

**1. Pull Request Tests (`.github/workflows/pr-tests.yml`)**
- Triggers: Pull requests to main/master/develop
- Purpose: Fast feedback without deployment
- Matrix testing: Python 3.9, 3.10, 3.11
- Non-blocking linting and security scans
- Automated PR summary generation

**2. CI/CD Pipeline (`.github/workflows/ci-cd.yml`)**
- Triggers: Push to main/master/develop
- Purpose: Full pipeline with deployment
- Quality gates: Deploy only after all tests pass
- Multi-platform Docker builds (amd64, arm64)
- Docker Hub integration with automated updates

### Quality Gates

**Pull Request Requirements:**
- All tests must pass across Python versions
- Application must start successfully
- Linting/security issues are informational

**Deployment Requirements:**
- All tests must pass
- Docker container must build and pass health checks
- Only deploys from main/master branches

### Test Suite

**Coverage: 28.6%** (191 total tests)
- `tests/test_database.py`: 25 tests - Database operations
- `tests/test_app.py`: 35 tests - Flask routes and views
- `tests/test_i18n.py`: 38 tests - Internationalization
- `tests/test_search.py`: 43 tests - Search and filtering
- `tests/test_translations.py`: 23 tests - Translation functionality
- `tests/test_integration.py`: 27 tests - End-to-end testing

**Test Categories:**
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.database`: Database tests
- `@pytest.mark.flask`: Flask application tests
- `@pytest.mark.i18n`: Internationalization tests
- `@pytest.mark.slow`: Performance tests

## Configuration

### Environment Variables

```bash
# Application
FLASK_ENV=development|production|testing
FLASK_HOST=0.0.0.0
FLASK_PORT=5014
SECRET_KEY=your-secret-key

# Database
DATABASE_PATH=recipes.db

# Internationalization
BABEL_DEFAULT_LOCALE=es
BABEL_DEFAULT_TIMEZONE=UTC
```

### Docker Configuration

```dockerfile
# Key Docker settings
EXPOSE 5000
WORKDIR /app
USER flaskuser  # Non-root user for security
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3
```

## Database Operations

### Key Functions

```python
# Database initialization
init_database()

# Recipe operations
get_all_recipes()
get_recipe_by_id(recipe_id)
search_recipes(query, category=None)

# Translation operations
get_recipe_translation(recipe_id, language)
save_recipe_translation(recipe_id, language, ...)
get_recipe_with_translation(recipe_id, language)

# Search with translations
search_recipes_with_translation(query, category, language)
get_all_recipes_with_translation(language)
```

### Translation System

**Fallback Logic:**
1. Check for specific language translation
2. Fall back to original Spanish content
3. Handle partial translations gracefully

**Storage:**
- Original recipes in `recipes` table
- Translations in `recipe_translations` table
- Unique constraint on `(recipe_id, language)`

## Flask Application Structure

### Routes

```python
@app.route('/')                           # Main page with search
@app.route('/recipe/<int:recipe_id>')     # Recipe detail view
@app.route('/categories')                 # Category listing
@app.route('/category/<category_name>')   # Category recipes
@app.route('/set_language/<language>')    # Language switching
@app.route('/health')                     # Health check endpoint
```

### Internationalization

```python
# Locale selection priority:
# 1. URL parameter (?language=en)
# 2. Session storage
# 3. Browser language preferences
# 4. Default (Spanish)

def get_locale():
    if 'language' in request.args:
        language = request.args['language']
        if language in app.config['LANGUAGES']:
            session['language'] = language
            return language
    
    if 'language' in session:
        if session['language'] in app.config['LANGUAGES']:
            return session['language']
    
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'es'
```

## Security Considerations

### Application Security
- **Input Validation**: All user inputs are validated
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Jinja2 auto-escaping
- **CSRF Protection**: Session-based protection
- **Non-root Container**: Docker runs as non-root user

### CI/CD Security
- **Security Scanning**: Bandit and Safety checks
- **Dependency Scanning**: Automated vulnerability detection
- **Secret Management**: GitHub secrets for sensitive data
- **Container Security**: Multi-stage builds, minimal base images

## Performance Optimizations

### Database
- **Indexing**: Strategic indexes on searchable fields
- **Query Optimization**: Efficient search operations
- **Connection Management**: Proper connection handling

### Application
- **Caching**: Flask-Babel translation caching
- **Static Assets**: Optimized CSS/JS delivery
- **Markdown Processing**: Efficient content rendering

### Docker
- **Multi-stage Builds**: Optimized image sizes
- **Layer Caching**: GitHub Actions cache optimization
- **Multi-platform**: amd64 and arm64 support

## Monitoring and Debugging

### Health Checks
- **Application**: `/health` endpoint with recipe count
- **Docker**: Built-in health check with curl
- **CI/CD**: Automated container health validation

### Logging
- **Application**: Flask default logging
- **CI/CD**: Comprehensive step logging
- **Docker**: Container logs for debugging

### Debugging Tools
- **Coverage Analysis**: `coverage_report.py`
- **CI/CD Validation**: `validate_cicd.py`
- **Test Runner**: `run_tests.py`
- **Makefile**: Convenient command shortcuts

## Translation Management

### Supported Languages
- **Spanish (es)**: Default/original language
- **English (en)**: Full translation support using AI
- **Chinese (zh)**: Full translation support using AI
- **Valencian (ca)**: Full translation support using AI  
- **Basque (eu)**: Full translation support using AI

### Translation Workflow
1. **Content Creation**: Original recipes in Spanish
2. **AI Translation**: All translations generated using AI models with contextual understanding
3. **Database Storage**: Translations stored in `recipe_translations`
4. **Fallback Handling**: Graceful degradation to original content

### Translation Scripts
- `enhanced_translation_system.py`: **PRIMARY** - Enhanced AI-powered translation system providing complete translations for all recipe components (titles, descriptions, ingredients, instructions)
- `ai_translation_system.py`: AI-powered translation system for all languages
- `babel_manager.py`: Flask-Babel management and compilation
- `docker_compile_translations.py`: Docker-compatible compilation with fallback support

### Translation Compilation
**IMPORTANT**: Flask-Babel is installed in the virtual environment. Always activate the venv before compiling translations:
```bash
source venv/bin/activate
python -c "from babel.messages.pofile import read_po; from babel.messages.mofile import write_mo; ..."
```

### ⚠️ CRITICAL TRANSLATION POLICY
**STRICTLY FORBIDDEN**: Dictionary-based translations, pre-defined lookup tables, or hardcoded translation mappings.

**REQUIRED**: All translations must be generated using AI models with proper contextual understanding for culinary content.

## Deployment

### Production Deployment
- **Container Registry**: Docker Hub (`bbotella/recetas-tia-carmen`)
- **Multi-platform**: linux/amd64, linux/arm64
- **Health Checks**: Automated validation before deployment
- **Rollback**: Git-based version control

### Environment Configuration
```bash
# Production environment
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DATABASE_PATH=/app/data/recipes.db
```

## Development Tools

### Local Development
- **Pre-commit Hooks**: Automated testing before commits
- **Makefile**: Convenient command shortcuts
- **Docker Compose**: Local development environment
- **Virtual Environment**: Isolated Python environment

### Code Quality
- **Black**: Code formatting
- **Flake8**: Style checking
- **Pylint**: Code analysis
- **Type Hints**: Improved code documentation

### Testing Tools
- **pytest**: Test framework with fixtures
- **Coverage**: Code coverage analysis
- **Docker Testing**: Container-based testing
- **CI/CD Integration**: Automated testing pipeline

## Troubleshooting

### Common Issues

**Database Issues:**
- Check `DATABASE_PATH` environment variable
- Ensure database is initialized with `init_database()`
- Verify file permissions and disk space

**Docker Issues:**
- Port conflicts: Ensure 5000 is available
- Build failures: Check Dockerfile syntax
- Health check failures: Verify curl is installed

**CI/CD Issues:**
- Test failures: Check test logs and fix issues
- Deployment failures: Verify Docker Hub credentials
- Linting issues: Run formatters locally

**Translation Issues:**
- Missing translations: Check fallback logic
- Encoding issues: Ensure UTF-8 support
- Language switching: Verify session handling

### Debug Commands

```bash
# Test application locally
python run_tests.py

# Check database
python -c "from database import get_all_recipes; print(len(get_all_recipes()))"

# Validate CI/CD setup
python validate_cicd.py

# Check Docker build
docker build -t test-app .
docker run --rm test-app python run_tests.py
```

## Future Enhancements

### Planned Features
- [ ] User authentication and favorites
- [ ] Recipe rating and reviews
- [ ] Image upload and management
- [ ] Advanced search filters
- [ ] Recipe sharing and social features
- [ ] Mobile app development
- [ ] Performance monitoring
- [ ] Advanced analytics

### Technical Improvements
- [ ] Increase test coverage to 80%+
- [ ] Implement caching layer (Redis)
- [ ] Add API endpoints for mobile apps
- [ ] Implement real-time features
- [ ] Add monitoring and alerting
- [ ] Optimize database queries
- [ ] Implement content delivery network (CDN)

### DevOps Enhancements
- [ ] Kubernetes deployment
- [ ] Blue-green deployment strategy
- [ ] Automated backups
- [ ] Monitoring and alerting
- [ ] Load balancing
- [ ] Auto-scaling capabilities

## Contact and Support

### Development Team
- **Primary Developer**: Claude (AI Assistant)
- **Repository**: https://github.com/bbotella/recetas
- **Docker Hub**: https://hub.docker.com/r/bbotella/recetas-tia-carmen

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request
5. CI/CD will automatically test changes
6. Merge after review and approval

### Getting Help
- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: Check README.md and TESTING.md
- **CI/CD**: Review `.github/workflows/README.md`
- **Architecture**: This CLAUDE.md file

---

*Last updated: $(date)*
*This document is automatically maintained and should be updated with each significant change to the project.*