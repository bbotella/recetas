# Contributing to Tía Carmen's Recipes

First off, thank you for considering contributing to Tía Carmen's Recipes! It's people like you that make this project a great tool for preserving family culinary traditions.

## 🍽️ Ways to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you create a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include screenshots if applicable**
- **Specify your environment** (OS, Python version, browser, etc.)

### 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **Include mockups or examples if applicable**

### 🔧 Code Contributions

#### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/bbotella/recetas.git
   cd recetas
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python import_recipes.py
   ```

5. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Coding Standards

- **Follow PEP 8** for Python code style
- **Use meaningful variable and function names**
- **Add docstrings** to functions and classes
- **Keep functions small and focused**
- **Add comments** for complex logic
- **Use type hints** where appropriate

#### Example Code Style

```python
def search_recipes(query: str, category: str = None) -> List[Dict]:
    """
    Search recipes by title, description, or ingredients.
    
    Args:
        query: Search term to look for
        category: Optional category filter
        
    Returns:
        List of recipe dictionaries matching the search criteria
    """
    # Implementation here
    pass
```

#### Testing

- **Test your changes** thoroughly before submitting
- **Ensure the application runs without errors**
- **Test both development and Docker environments**
- **Verify search functionality works correctly**

## 📝 Pull Request Process

1. **Update documentation** if needed
2. **Ensure all tests pass** and the application runs correctly
3. **Update the README.md** with details of changes if applicable
4. **Follow the pull request template**
5. **Request review** from maintainers

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Local development testing
- [ ] Docker deployment testing
- [ ] Search functionality testing
- [ ] Recipe display testing

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information about the implementation.
```

## 🎨 Design Guidelines

### UI/UX Principles

- **Keep it simple and intuitive**
- **Maintain consistency** with existing design
- **Ensure mobile responsiveness**
- **Use Bootstrap components** when possible
- **Follow accessibility guidelines**

### Color Scheme

- Primary: `#8B4513` (Saddle Brown)
- Secondary: `#D2691E` (Chocolate)
- Accent: `#CD853F` (Peru)
- Background: `#FFF8DC` (Cornsilk)

## 🌐 Adding New Recipes

### Recipe Format

New recipes should follow this markdown structure:

```markdown
# Recipe Name

## Descripción
Brief description of the dish in Spanish.

## Ingredientes
- Ingredient 1
- Ingredient 2
- ...

## Preparación
1. Step 1
2. Step 2
3. ...

---
*Receta de Tía Carmen*
```

### Recipe Categories

Current categories:
- **Postres** - Desserts and sweets
- **Pollo** - Chicken dishes
- **Pescado** - Fish and seafood
- **Carnes** - Meat dishes
- **Bebidas** - Beverages
- **Verduras** - Vegetable dishes
- **Aperitivos** - Appetizers
- **Otros** - Other dishes

## 🚀 Deployment Contributions

### Docker Improvements

- **Optimize Dockerfile** for smaller images
- **Improve security** configurations
- **Add monitoring** capabilities
- **Enhance logging**

### Infrastructure

- **CI/CD pipelines**
- **Automated testing**
- **Performance monitoring**
- **Security scanning**

## 📚 Documentation

### Areas for Improvement

- **API documentation**
- **Installation guides**
- **Troubleshooting guides**
- **Architecture documentation**
- **Translation guides**

## 🤝 Community

### Code of Conduct

- **Be respectful** to all contributors
- **Welcome newcomers** and help them get started
- **Provide constructive feedback**
- **Focus on the project goals**

### Getting Help

- **Check existing issues** and documentation first
- **Ask questions** in GitHub discussions
- **Be specific** about your problem
- **Provide context** and examples

## 🎯 Roadmap

### High Priority
- [ ] User authentication system
- [ ] Recipe rating and reviews
- [ ] Advanced search filters
- [ ] Mobile app version

### Medium Priority
- [ ] Recipe scaling calculator
- [ ] Print-friendly format
- [ ] Social sharing
- [ ] Recipe suggestions

### Low Priority
- [ ] Multi-language support
- [ ] Recipe import from external sources
- [ ] Advanced analytics
- [ ] Recipe video support

## 📄 License

By contributing to Tía Carmen's Recipes, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **GitHub contributors** page
- **Release notes** for significant contributions

---

Thank you for helping preserve family culinary traditions! 🍽️❤️