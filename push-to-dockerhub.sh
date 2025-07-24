#!/bin/bash

# Build and push Docker image to Docker Hub (public registry)
# This script ensures we push to the public registry, not company internal

set -e

# Configuration
DOCKER_USERNAME="bbotella"
IMAGE_NAME="recetas-tia-carmen"
VERSION="latest"
FULL_IMAGE_NAME="docker.io/${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

echo "🐳 Building and pushing Docker image to Docker Hub (public registry)"
echo "=================================================================="
echo ""

# Check if Docker is logged in
echo "🔐 Checking Docker Hub authentication..."
if ! docker info | grep -q "Username: ${DOCKER_USERNAME}"; then
    echo "❌ Not logged in to Docker Hub. Please run:"
    echo "   docker login docker.io"
    echo ""
    echo "   Username: ${DOCKER_USERNAME}"
    echo "   Password: [your-docker-hub-token]"
    echo ""
    exit 1
fi

echo "✅ Authenticated with Docker Hub"
echo ""

# Build the image
echo "🏗️  Building Docker image..."
echo "Image name: ${FULL_IMAGE_NAME}"
echo ""

docker build -t ${FULL_IMAGE_NAME} .

echo ""
echo "✅ Image built successfully!"
echo ""

# Push to Docker Hub
echo "📤 Pushing to Docker Hub (public registry)..."
echo "Registry: docker.io"
echo "Repository: ${DOCKER_USERNAME}/${IMAGE_NAME}"
echo "Tag: ${VERSION}"
echo ""

docker push ${FULL_IMAGE_NAME}

echo ""
echo "✅ Image pushed successfully!"
echo ""

# Show image info
echo "📋 Image Information:"
echo "  Registry: Docker Hub (public)"
echo "  Full name: ${FULL_IMAGE_NAME}"
echo "  Size: $(docker images ${FULL_IMAGE_NAME} --format "table {{.Size}}" | tail -1)"
echo ""

# Verify it's available
echo "🔍 Verifying image is available..."
docker pull ${FULL_IMAGE_NAME}

echo ""
echo "🎉 Success! Your image is now available on Docker Hub:"
echo "   https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
echo ""
echo "📋 To use this image:"
echo "   docker run -d -p 5000:5000 ${FULL_IMAGE_NAME}"
echo ""
echo "🔄 Next steps:"
echo "   1. Update docker-compose.yml to use this image"
echo "   2. Test the deployment"
echo "   3. Update documentation"