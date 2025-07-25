FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for persistent database
RUN mkdir -p /app/data

# Import recipes to database
RUN python import_recipes.py

# Generate complete AI translations for all recipes
RUN python generate_complete_translations.py

# Generate Chinese translations for all recipes
RUN python generate_chinese_translations.py

# Compile Flask-Babel translations
RUN python babel_manager.py compile

# Create non-root user for security
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

# Expose port
EXPOSE 5014

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5014/ || exit 1

# Run the application
CMD ["python", "app.py"]