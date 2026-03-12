#!/bin/bash
# Deploy script for Railway

set -e

echo "🚀 Deploying OBDMS to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "Logging into Railway..."
railway login

# Link project
railway link

# Set environment variables
echo "Setting environment variables..."
railway variables set DEBUG=False
railway variables set ENVIRONMENT=production

# Deploy
echo "Starting deployment..."
railway up

echo "✅ Deployment complete!"
echo "Check status: railway status"
