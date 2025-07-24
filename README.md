# 🍽️ Recetas de Tía Carmen

A beautiful web application to preserve and share traditional Spanish family recipes. Built with Flask, this application provides an elegant interface to browse, search, and discover 73 authentic recipes from Tía Carmen's collection.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 🌟 Features

- **🔍 Smart Search**: Search recipes by name, ingredients, or description
- **📂 Category Filtering**: Browse recipes organized by type (Desserts, Chicken, Fish, etc.)
- **📱 Responsive Design**: Beautiful interface that works on all devices
- **🎨 Modern UI**: Clean, intuitive design with Bootstrap styling
- **🐳 Docker Ready**: Easy deployment with Docker and Docker Compose
- **🗄️ SQLite Database**: Lightweight, fast, and reliable data storage
- **🔄 Real-time Search**: Instant results as you type
- **📄 Individual Recipe Pages**: Detailed view with ingredients and step-by-step instructions

## 📸 Screenshots

| Home Page | Recipe Detail | Search Results |
|-----------|---------------|----------------|
| ![Home](docs/screenshots/home.png) | ![Recipe](docs/screenshots/recipe.png) | ![Search](docs/screenshots/search.png) |

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/bbotella/recetas.git
cd recetas

# Deploy using public Docker Hub image
./quick-deploy.sh

# Access the application
open http://localhost:5000
```

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/bbotella/recetas.git
cd recetas

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Import recipes to database
python import_recipes.py

# Run the application
python app.py
```

### Option 3: Quick Setup Script

```bash
# Clone and run setup script
git clone https://github.com/yourusername/tia-carmen-recipes.git
cd tia-carmen-recipes
./setup.sh
```

## 🏗️ Project Structure

```
recetas/
├── 📁 recipes/              # 73 original markdown recipe files
├── 📁 templates/            # HTML templates (Jinja2)
├── 📁 static/              # CSS, JavaScript, and assets
├── 📄 app.py               # Main Flask application
├── 📄 database.py          # Database operations
├── 📄 import_recipes.py    # Script to import recipes to database
├── 📄 requirements.txt     # Python dependencies
├── 📄 Dockerfile          # Docker configuration
├── 📄 docker-compose.yml  # Docker Compose setup
├── 📄 setup.sh            # Quick setup script
├── 📄 deploy.sh           # Deployment guide
└── 📄 README.md           # This file
```

## 🍳 Recipe Categories

The application automatically categorizes recipes into:

- **🍰 Postres** (42 recipes) - Desserts, cakes, ice creams, and sweets
- **🍗 Pollo** (4 recipes) - Chicken dishes and poultry
- **🐟 Pescado** (8 recipes) - Fish and seafood specialties
- **🥩 Carnes** (7 recipes) - Meat dishes and stews
- **🥤 Bebidas** (8 recipes) - Beverages and drinks
- **🥬 Verduras** (3 recipes) - Vegetable dishes and salads
- **🍤 Aperitivos** (1 recipe) - Appetizers and small plates
- **🍽️ Otros** (3 recipes) - Other traditional dishes

## 🔧 Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Optional: Docker and Docker Compose

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bbotella/recetas.git
   cd recetas
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python import_recipes.py
   ```

5. **Run development server**
   ```bash
   python app.py
   ```

### Database Schema

```sql
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
```

## 🐳 Docker Deployment

### Using Public Docker Hub Image (Recommended)

```bash
# Quick deployment
./quick-deploy.sh

# Or manual deployment
docker-compose pull
docker-compose up -d
```

### Production Deployment with Nginx

```bash
docker-compose --profile production up -d
```

### Development (builds from source)

```bash
# Development deployment
./dev-deploy.sh

# Or manual development
docker-compose -f docker-compose.dev.yml up -d --build
```

### Docker Hub Repository

The application is available as a public Docker image:
- **Registry**: Docker Hub (public)
- **Repository**: `docker.io/bbotella/recetas-tia-carmen`
- **URL**: https://hub.docker.com/r/bbotella/recetas-tia-carmen

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_HOST`: Host to bind to (default: `0.0.0.0`)
- `FLASK_PORT`: Port to run on (default: `5000`)

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with search |
| `/recipe/<id>` | GET | Individual recipe details |
| `/categories` | GET | List all categories |
| `/category/<name>` | GET | Recipes by category |
| `/health` | GET | Health check endpoint |

## 🧪 Testing

```bash
# Run basic health check
curl http://localhost:5000/health

# Test search functionality
curl "http://localhost:5000/?q=pollo"

# Test category filtering
curl "http://localhost:5000/?category=Postres"
```

## 📝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code style
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly

## 🎯 Future Enhancements

- [ ] User authentication and favorites
- [ ] Recipe rating and reviews
- [ ] Social sharing functionality
- [ ] Recipe suggestions based on ingredients
- [ ] Mobile app version
- [ ] Recipe import from external sources
- [ ] Advanced search filters
- [ ] Recipe scaling calculator
- [ ] Print-friendly recipe format
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tía Carmen** - For preserving these wonderful family recipes
- **Bootstrap** - For the beautiful UI components
- **Flask** - For the excellent web framework
- **Font Awesome** - For the icons
- **Docker** - For making deployment simple

## 📬 Contact

- **Author**: Bernardo Botella
- **Email**: bernardobotellacorbi@gmail.com
- **GitHub**: [@bbotella](https://github.com/bbotella)

---

<div align="center">
  <p><strong>Made with ❤️ to preserve family culinary traditions</strong></p>
  <p><em>Preserving the past, one recipe at a time</em></p>
</div>
