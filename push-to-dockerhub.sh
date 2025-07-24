#!/bin/bash

# Build and push Docker image to Docker Hub (public registry)
# This script ensures we push to the public registry, not company internal
# Builds multi-architecture image for compatibility with different platforms

set -e

# Configuration
DOCKER_USERNAME="bbotella"
IMAGE_NAME="recetas-tia-carmen"
VERSION="latest"
FULL_IMAGE_NAME="docker.io/${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

echo "🐳 Building and pushing multi-architecture Docker image to Docker Hub"
echo "====================================================================="
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

# Create buildx builder if it doesn't exist
echo "🔧 Setting up multi-architecture builder..."
if ! docker buildx inspect multiarch-builder >/dev/null 2>&1; then
    echo "Creating new buildx builder..."
    docker buildx create --name multiarch-builder --use
else
    echo "Using existing buildx builder..."
    docker buildx use multiarch-builder
fi

# Bootstrap the builder
docker buildx inspect --bootstrap

echo ""
echo "✅ Multi-architecture builder ready"
echo ""

# Build and push multi-architecture image
echo "🏗️  Building multi-architecture Docker image..."
echo "Image name: ${FULL_IMAGE_NAME}"
echo "Platforms: linux/amd64, linux/arm64"
echo ""

docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag ${FULL_IMAGE_NAME} \
    .

echo ""
echo "✅ Multi-architecture image built and pushed successfully!"
echo ""

# Show image info
echo "📋 Image Information:"
echo "  Registry: Docker Hub (public)"
echo "  Full name: ${FULL_IMAGE_NAME}"
echo "  Platforms: linux/amd64, linux/arm64"
echo ""

# Verify it's available
echo "🔍 Verifying image is available..."
docker pull ${FULL_IMAGE_NAME}

echo ""
echo "🎉 Success! Your multi-architecture image is now available on Docker Hub:"
echo "   https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
echo ""
echo "📋 To use this image on any platform:"
echo "   docker run -d -p 5014:5014 ${FULL_IMAGE_NAME}"
echo ""
echo "🖥️  Supported platforms:"
echo "   - Intel/AMD x86_64 (most servers, NAS devices)"
echo "   - ARM64 (Apple Silicon, ARM servers)"
echo ""
echo "🔄 Next steps:"
echo "   1. Test the deployment on your NAS"
echo "   2. Update docker-compose.yml (already done)"
echo "   3. Deploy with confidence!"