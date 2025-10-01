# Local AI Bot - Private Document Processing Solution

A comprehensive local AI solution for processing confidential documents using Ollama and Open WebUI.

## Features

- 🔒 **Fully Private**: All processing happens locally on your Mac
- 📄 **Document Processing**: Support for PDF, DOCX, TXT, and other formats
- 💬 **Chat Interface**: ChatGPT-like interface via Open WebUI
- 🔍 **Document Analysis**: Extract insights, summaries, and breakdowns
- 🛡️ **Security First**: No data leaves your machine

## Prerequisites

- macOS
- Python 3.8+
- Ollama (already installed at `/Users/yancyshepherd/.ollama/models`)
- Docker (for Open WebUI)

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Open WebUI**
   ```bash
   ./scripts/start-webui.sh
   ```

3. **Process Documents**
   ```bash
   python src/document_processor.py --file path/to/document.pdf
   ```

## Current Models

- `llama3.1:latest` - Main conversational AI
- `nomic-embed-text:latest` - Document embeddings

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Open WebUI    │    │  Document       │    │     Ollama      │
│   (Interface)   │────│  Processor      │────│   (AI Models)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Security Notes

- All data processing happens locally
- No internet connection required for AI processing
- Documents are processed in memory when possible
- Optional encrypted storage for processed documents
