#!/bin/bash

# Start Open WebUI with Ollama integration
# This script sets up Open WebUI to work with your local Ollama installation

echo "🚀 Starting Open WebUI for Local AI Bot..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "🔄 Starting Ollama..."
    ollama serve &
    sleep 5
fi

echo "✅ Ollama is running"

# Pull and run Open WebUI
echo "🔄 Starting Open WebUI..."
docker run -d \
  --name open-webui \
  --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://localhost:11434 \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:main

echo "⏳ Waiting for Open WebUI to start..."
sleep 10

# Check if Open WebUI is running
if curl -s http://localhost:3000 >/dev/null 2>&1; then
    echo "✅ Open WebUI is running at http://localhost:3000"
    echo "🎉 You can now access your private AI chat interface!"
    echo ""
    echo "📋 Available models:"
    ollama list
else
    echo "❌ Failed to start Open WebUI. Checking logs..."
    docker logs open-webui
fi
