#!/bin/bash
# Build script for Docker image
# This script packages the model and serving code into a deployable container
# Principle: "Only build your binaries once"

set -e  # Exit on any error

IMAGE_NAME="avazu-ctr-api"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "🔨 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"

# Build the Docker image
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .

echo "✅ Docker image built successfully: ${IMAGE_NAME}:${IMAGE_TAG}"

# Optionally, list the image
echo "📦 Built image details:"
docker images "${IMAGE_NAME}:${IMAGE_TAG}"

