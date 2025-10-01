#!/bin/bash

# Local AI Bot Launcher
# Choose between Open WebUI or built-in web interface

echo "🤖 Local AI Bot Launcher"
echo "========================"
echo ""
echo "Choose your interface:"
echo "1) Open WebUI (Docker-based, ChatGPT-like interface)"
echo "2) Built-in Web API (Python-based, document-focused)"
echo "3) Command Line (Document processor only)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Starting Open WebUI..."
        ./scripts/start-webui.sh
        ;;
    2)
        echo "🚀 Starting built-in web API..."
        cd src && python3 web_api.py --port 8899
        ;;
    3)
        echo "📄 Command line mode - use: python src/document_processor.py --help"
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        ;;
esac
