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

# Force update all translations to ensure Docker matches local
RUN python scripts/docker_force_translation_update.py

# Create non-root user for security
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

# Expose port 5014 (default Flask port for this app)
EXPOSE 5014

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5014/health || exit 1

# Run the application
CMD ["python", "app.py"]