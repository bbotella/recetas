#!/bin/bash

# Docker deployment script for Tía Carmen's Recipe Website

echo "🐳 Docker Deployment Guide for Tía Carmen's Recipe Website"
echo "=========================================================="
echo ""

# Build and run with Docker Compose (recommended)
echo "🚀 Option 1: Using Docker Compose (Recommended)"
echo "-----------------------------------------------"
echo "1. Simple deployment:"
echo "   docker-compose up -d"
echo ""
echo "2. With nginx reverse proxy:"
echo "   docker-compose --profile production up -d"
echo ""
echo "3. Rebuild and restart:"
echo "   docker-compose down && docker-compose up -d --build"
echo ""

# Manual Docker commands
echo "🔧 Option 2: Manual Docker Commands"
echo "-----------------------------------"
echo "1. Build the image:"
echo "   docker build -t tia-carmen-recipes ."
echo ""
echo "2. Run the container:"
echo "   docker run -d -p 5000:5000 --name tia-carmen-recipes tia-carmen-recipes"
echo ""
echo "3. With persistent data volume:"
echo "   docker run -d -p 5000:5000 -v \$(pwd)/data:/app/data --name tia-carmen-recipes tia-carmen-recipes"
echo ""

# Production deployment
echo "🏭 Production Deployment"
echo "------------------------"
echo "1. For production with nginx:"
echo "   docker-compose --profile production up -d"
echo ""
echo "2. Custom domain setup:"
echo "   - Update nginx.conf with your domain"
echo "   - Add SSL certificates"
echo "   - Configure firewall"
echo ""

# Management commands
echo "📋 Management Commands"
echo "----------------------"
echo "View logs:        docker-compose logs -f"
echo "Stop services:    docker-compose down"
echo "Restart:          docker-compose restart"
echo "Shell access:     docker-compose exec tia-carmen-recipes bash"
echo "Remove all:       docker-compose down -v --rmi all"
echo ""

# URLs
echo "🌐 Access URLs"
echo "--------------"
echo "Development:      http://localhost:5000"
echo "With nginx:       http://localhost:80"
echo "Health check:     http://localhost:5000/health"
echo ""

echo "✅ Ready to deploy! Choose your preferred option above."