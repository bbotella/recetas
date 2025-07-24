#!/bin/bash

# Docker deployment script for Tía Carmen's Recipe Website

echo "🐳 Docker Deployment Guide for Tía Carmen's Recipe Website"
echo "=========================================================="
echo ""

# Public Docker Hub image deployment (recommended)
echo "🚀 Option 1: Using Public Docker Hub Image (Recommended)"
echo "--------------------------------------------------------"
echo "1. Quick deployment:"
echo "   ./quick-deploy.sh"
echo ""
echo "2. Manual deployment:"
echo "   docker-compose pull"
echo "   docker-compose up -d"
echo ""
echo "3. With nginx reverse proxy:"
echo "   docker-compose --profile production up -d"
echo ""

# Local development
echo "🛠️  Option 2: Local Development (builds from source)"
echo "----------------------------------------------------"
echo "1. Development deployment:"
echo "   ./dev-deploy.sh"
echo ""
echo "2. Manual development:"
echo "   docker-compose -f docker-compose.dev.yml up -d --build"
echo ""

# Build and push to Docker Hub
echo "📤 Option 3: Build and Push to Docker Hub"
echo "------------------------------------------"
echo "1. Login to Docker Hub:"
echo "   docker login docker.io"
echo ""
echo "2. Build and push:"
echo "   ./push-to-dockerhub.sh"
echo ""

# Manual Docker commands
echo "🔧 Option 4: Manual Docker Commands"
echo "-----------------------------------"
echo "1. Pull and run public image:"
echo "   docker pull docker.io/bbotella/recetas-tia-carmen:latest"
echo "   docker run -d -p 5014:5000 --name tia-carmen-recipes docker.io/bbotella/recetas-tia-carmen:latest"
echo ""
echo "2. Build from source:"
echo "   docker build -t tia-carmen-recipes ."
echo "   docker run -d -p 5014:5000 --name tia-carmen-recipes tia-carmen-recipes"
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
echo "Development:      http://localhost:5014"
echo "With nginx:       http://localhost:80"
echo "Health check:     http://localhost:5014/health"
echo "Docker Hub:       https://hub.docker.com/r/bbotella/recetas-tia-carmen"
echo ""

echo "✅ Ready to deploy! Choose your preferred option above."