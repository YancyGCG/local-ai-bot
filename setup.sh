#!/bin/bash

# Quick setup script for Local AI Bot
# This script will install dependencies, check prerequisites, and start the system

set -e

echo "🤖 Local AI Bot - Quick Setup"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
echo ""
print_info "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    print_status "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not found. Please install Python 3.8+"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is required but not found"
    exit 1
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    print_status "Ollama found"
    
    # Check if Ollama service is running
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        print_status "Ollama service is running"
    else
        print_warning "Ollama service is not running. Starting it..."
        ollama serve &
        sleep 3
    fi
else
    print_error "Ollama is required but not found. Please install Ollama first:"
    print_error "Visit: https://ollama.ai/"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    if docker info >/dev/null 2>&1; then
        print_status "Docker is running"
    else
        print_warning "Docker is installed but not running. Please start Docker Desktop"
        print_info "You can continue without Docker, but Open WebUI won't be available"
    fi
else
    print_warning "Docker not found. Open WebUI requires Docker"
    print_info "You can still use the document processor without Docker"
fi

# Install Python dependencies
echo ""
print_info "Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    print_status "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Create necessary directories
mkdir -p logs
mkdir -p data/processed
mkdir -p data/uploads

print_status "Directory structure created"

# Check available models
echo ""
print_info "Checking available Ollama models..."
ollama list

# Offer to download recommended models if not present
if ! ollama list | grep -q "llama3.1"; then
    echo ""
    print_warning "Recommended model 'llama3.1' not found"
    read -p "Would you like to download it? (This may take a while) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Downloading llama3.1..."
        ollama pull llama3.1
    fi
fi

if ! ollama list | grep -q "nomic-embed-text"; then
    echo ""
    print_warning "Embedding model 'nomic-embed-text' not found"
    read -p "Would you like to download it? (Recommended for document processing) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Downloading nomic-embed-text..."
        ollama pull nomic-embed-text
    fi
fi

echo ""
print_status "Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Start Open WebUI: ./scripts/start-webui.sh"
echo "2. Process a document: python src/document_processor.py --file path/to/document.pdf"
echo "3. Access web interface: http://localhost:3000"
echo ""
echo "📖 For more information, see README.md"
