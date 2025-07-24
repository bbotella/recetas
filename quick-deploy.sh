#!/bin/bash

# Quick deployment script
echo "🚀 Deploying Tía Carmen's Recipe Website..."

# Build and run with Docker Compose
docker-compose down 2>/dev/null
docker-compose up -d --build

echo "✅ Deployment complete!"
echo "🌐 Access the website at: http://localhost:5000"
echo "📊 Health check: http://localhost:5000/health"
echo ""
echo "📋 Management commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"