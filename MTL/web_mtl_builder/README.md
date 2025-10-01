# MTL Document Builder Web Interface

This web application provides a user-friendly interface for generating MTL documents from JSON files.

## Features

- Drag-and-drop upload of JSON files
- Selection of MTL types (MTL1, MTL2, MTL3)
- Generate documents in DOCX or PDF format
- Specify revision number for documents
- View and download all generated files
- Direct file download after generation

## Development Setup

### Prerequisites

- Python 3.7+ with pip
- LibreOffice (for PDF conversion)
- Docker and Docker Compose (optional)

### Running Locally

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install LibreOffice (required for PDF conversion):
   - Mac: `brew install --cask libreoffice`
   - Linux: `apt-get install libreoffice`
   - Windows: Download from https://www.libreoffice.org/download/

3. Run the application:
   ```bash
   python app.py
   ```

4. Open a browser and navigate to:
   ```
   http://localhost:5555
   ```

### Running with Docker

From the `web_mtl_builder` directory:

```bash
docker-compose build
docker-compose up
```

Or from the `MTL` parent directory:

```bash
docker-compose -f web_mtl_builder/docker-compose.yml build
docker-compose -f web_mtl_builder/docker-compose.yml up
```

The application will be available at http://localhost:8080

## Project Structure

```
MTL/
├── final_mtl_generator.py  # Core MTL generator logic
├── templates/              # MTL document templates
│   ├── MTL1 Template GT-00X-0X.docx
│   ├── MTL2 Template GT-00X-0X.docx
│   └── MTL3 Template GT-00X-0X.docx
├── uploads/                # Uploaded JSON files (volume)
├── generated_mtls/         # Generated documents (volume)
├── web_mtl_builder/
│   ├── app.py              # Flask web application
│   ├── mtl_pdf_generator.py # Document generation wrapper
│   ├── Dockerfile          # Docker build config
│   ├── docker-compose.yml  # Docker Compose config
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML templates for web interface
│       ├── index.html      # Upload form
│       └── files.html      # File listing
```

## Usage

1. Open the web interface at http://localhost:5555 (local) or http://localhost:8080 (Docker)
2. Drag and drop your JSON file or click to select one
3. Select the MTL type (MTL1, MTL2, or MTL3)
4. Enter the revision number
5. Select the output format (DOCX or PDF)
6. Click "Generate Document"
7. The file will download automatically

## Troubleshooting

- If PDF generation fails, ensure LibreOffice is installed and accessible in the system PATH
- Check permissions on the templates, uploads, and generated_mtls directories
- For Docker deployment, ensure volumes are correctly mapped

## Notes

- The templates folder should contain DOCX templates named according to the pattern in the code
- JSON files should have the expected structure with fields matching the placeholders in the templates
- For large files or batch processing, use the "View Generated Files" link after generation
│   ├── templates/          # HTML templates
│   │   ├── index.html      # Main UI
│   │   └── files.html      # File listing UI
```

## Docker Configuration

- Build context is set to the parent `MTL` directory to access all necessary files
- Volumes are mounted for persistent storage of uploads and generated files
- Flask runs in development mode with debug enabled

## API Endpoints

- `/` - Main page for uploading files and generating PDFs
- `/generated` - View all generated files
- `/download/<filename>` - Download a specific generated file
