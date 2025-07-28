FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for persistent database
RUN mkdir -p /app/data

# Initialize database
RUN python -c "from database import init_database; init_database()"

# Import recipes to database (only if recipes directory exists)
RUN if [ -d "recipes" ]; then python scripts/import_recipes.py; fi

# Import all translations from individual JSON files
RUN python scripts/import_all_translations.py

# Fix recipe ID mismatch in translations
RUN python scripts/fix_translation_ids.py

# Compile Flask-Babel translations
RUN python scripts/docker_compile_translations.py

# Copy the built database to the data directory for persistence
RUN cp /app/recipes.db /app/data/recipes.db

# Create non-root user for security
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

# Expose port 5014 (custom Flask port for this app)
EXPOSE 5014

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5014/health || exit 1

# Run the application
CMD ["python", "app.py"]