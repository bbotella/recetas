#!/bin/bash

# Build Docker image specifically for AMD64/x86_64 architecture (most NAS devices)
# Use this if you're having issues with multi-arch builds

set -e

# Configuration
DOCKER_USERNAME="bbotella"
IMAGE_NAME="recetas-tia-carmen"
VERSION="latest"
FULL_IMAGE_NAME="docker.io/${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

echo "🐳 Building Docker image for AMD64/x86_64 architecture"
echo "======================================================"
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

# Build for AMD64 architecture specifically
echo "🏗️  Building Docker image for AMD64/x86_64..."
echo "Image name: ${FULL_IMAGE_NAME}"
echo "Platform: linux/amd64"
echo ""

docker buildx build \
    --platform linux/amd64 \
    --push \
    --tag ${FULL_IMAGE_NAME} \
    .

echo ""
echo "✅ AMD64 image built and pushed successfully!"
echo ""

# Show image info
echo "📋 Image Information:"
echo "  Registry: Docker Hub (public)"
echo "  Full name: ${FULL_IMAGE_NAME}"
echo "  Platform: linux/amd64 (Intel/AMD x86_64)"
echo ""

# Verify it's available
echo "🔍 Verifying image is available..."
docker pull ${FULL_IMAGE_NAME}

echo ""
echo "🎉 Success! Your AMD64 image is now available on Docker Hub:"
echo "   https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
echo ""
echo "📋 This image is compatible with:"
echo "   - Most NAS devices (Synology, QNAP, etc.)"
echo "   - Intel/AMD servers"
echo "   - x86_64 Linux systems"
echo ""
echo "💡 To use this image on your NAS:"
echo "   docker run -d -p 5014:5014 ${FULL_IMAGE_NAME}"