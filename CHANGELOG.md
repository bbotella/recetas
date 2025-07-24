# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- User authentication system (planned)
- Recipe rating and reviews (planned)
- Advanced search filters (planned)
- Mobile app version (planned)

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Tía Carmen's Recipes web application
- 73 traditional Spanish recipes imported from markdown files
- Flask web application with search functionality
- SQLite database for recipe storage
- Responsive Bootstrap-based UI
- Docker and Docker Compose support
- Category-based recipe organization
- Individual recipe detail pages
- Health check endpoint for monitoring
- Comprehensive documentation and setup scripts

### Features
- **Search functionality**: Search recipes by name, ingredients, or description
- **Category filtering**: Browse recipes by type (Postres, Pollo, Pescado, etc.)
- **Responsive design**: Works on desktop and mobile devices
- **Docker deployment**: Easy deployment with Docker and Docker Compose
- **Production ready**: Nginx reverse proxy configuration included
- **Database schema**: SQLite with full-text search capabilities

### Categories
- **Postres** (42 recipes) - Desserts, cakes, ice creams, and sweets
- **Pollo** (4 recipes) - Chicken dishes and poultry
- **Pescado** (8 recipes) - Fish and seafood specialties
- **Carnes** (7 recipes) - Meat dishes and stews
- **Bebidas** (8 recipes) - Beverages and drinks
- **Verduras** (3 recipes) - Vegetable dishes and salads
- **Aperitivos** (1 recipe) - Appetizers and small plates
- **Otros** (3 recipes) - Other traditional dishes

### Technical Details
- Python 3.8+ support
- Flask 2.3+ framework
- SQLite database with full-text search
- Bootstrap 5 for responsive design
- Font Awesome icons
- Docker multi-stage builds
- Nginx reverse proxy support
- Health monitoring endpoints

### Documentation
- Comprehensive README with setup instructions
- Docker deployment guide
- Contributing guidelines
- MIT license
- API documentation
- Database schema documentation

### Security
- Non-root Docker container execution
- Environment variable configuration
- Secure defaults for production deployment
- Input sanitization and validation

## [0.1.0] - 2024-01-XX

### Added
- Initial project structure
- Basic Flask application setup
- Recipe markdown files conversion
- Database import script
- Basic search functionality

---

### Legend
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes