#!/bin/bash

# Run script for Tía Carmen's Recipe Website
# This script activates the virtual environment and runs the application

echo "🍽️  Starting Tía Carmen's Recipe Website..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if database exists
if [ ! -f "recipes.db" ]; then
    echo "📚 Database not found. Importing recipes..."
    python import_recipes.py
fi

# Run the application
echo "🚀 Starting Flask application..."
echo "📱 Open your browser to: http://localhost:5014"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python app.py