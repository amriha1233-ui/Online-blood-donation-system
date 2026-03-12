#!/bin/bash
# Deploy script for Fly.io

set -e

echo "🚀 Deploying OBDMS to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "Flyctl not found. Please install from https://fly.io/docs/getting-started/installing-flyctl/"
    exit 1
fi

# Authenticate
echo "Authenticating with Fly.io..."
flyctl auth login

# Create app if it doesn't exist
if ! flyctl apps list | grep -q "obdms"; then
    echo "Creating Fly.io app..."
    flyctl apps create obdms
fi

# Deploy
echo "Deploying application..."
flyctl deploy

echo "✅ Deployment complete!"
echo "View app: flyctl open"
