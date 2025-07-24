#!/bin/bash

# Setup script for Tía Carmen's Recipe Website
# This script creates a virtual environment and sets up the application

echo "🍽️  Setting up Tía Carmen's Recipe Website..."
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project directory."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Import recipes to database
echo "📚 Importing recipes to database..."
python import_recipes.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the app: python app.py"
echo "   3. Open browser: http://localhost:5000"
echo "   4. When done: deactivate"
echo ""
echo "🔧 To run setup again: ./setup.sh"
echo ""