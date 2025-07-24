#!/bin/bash

# Development deployment script - builds from source
echo "🛠️  Deploying Tía Carmen's Recipe Website for development..."

# Build and run with Docker Compose
docker-compose -f docker-compose.dev.yml down 2>/dev/null
docker-compose -f docker-compose.dev.yml up -d --build

echo "✅ Development deployment complete!"
echo "🌐 Access the website at: http://localhost:5000"
echo "📊 Health check: http://localhost:5000/health"
echo ""
echo "📋 Management commands:"
echo "  View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "  Stop: docker-compose -f docker-compose.dev.yml down"
echo "  Restart: docker-compose -f docker-compose.dev.yml restart"
echo ""
echo "💡 For production deployment, use: ./quick-deploy.sh"