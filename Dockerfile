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

# Import recipes to database (only if recipes directory exists)
RUN if [ -d "recipes" ]; then python scripts/import_recipes.py; fi

# Generate translations (only if translation scripts exist)
RUN if [ -f "scripts/generate_complete_translations.py" ]; then python scripts/generate_complete_translations.py; fi
RUN if [ -f "scripts/generate_chinese_translations.py" ]; then python scripts/generate_chinese_translations.py; fi

# Compile Flask-Babel translations (always run to ensure translations are available)
RUN python scripts/babel_manager.py compile

# Create non-root user for security
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

# Expose port 5000 (matching the workflow)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]