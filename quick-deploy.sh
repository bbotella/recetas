#!/bin/bash

# Quick deployment script using public Docker Hub image
echo "🚀 Deploying Tía Carmen's Recipe Website from Docker Hub..."

# Stop any existing containers
docker-compose down 2>/dev/null

# Pull latest image from Docker Hub and run
echo "📥 Pulling latest image from Docker Hub..."
docker-compose pull

echo "🏃 Starting application..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "🌐 Access the website at: http://localhost:5000"
echo "📊 Health check: http://localhost:5000/health"
echo ""
echo "📋 Management commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"

# Wait a moment and check if it's running
sleep 3
if curl -sf http://localhost:5000/health > /dev/null; then
    echo "✅ Application is running and healthy!"
else
    echo "⚠️  Application may still be starting up. Check logs with: docker-compose logs -f"
fi