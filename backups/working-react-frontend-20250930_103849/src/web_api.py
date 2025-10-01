print('=== web_api.py is running ===')

"""
Simple Web API for Local AI Bot
Alternative to Open WebUI with document processing capabilities
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import tempfile
import uvicorn
from pathlib import Path
import shutil
import logging

from src.document_processor import DocumentProcessor, ProcessedDocument
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Local AI Bot API",
    description="Private document processing and AI chat API",
    version="1.0.0"
)

# Serve static files (templates, assets, data)
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/data", StaticFiles(directory="data"), name="data")

# Check if built frontend exists and mount it for SPA routes
SPA_INDEX = Path("frontend/dist/index.html")
if SPA_INDEX.exists():
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
    print('Serving frontend SPA assets from frontend/dist/assets')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global processor instance
# Use localhost when running outside Docker, ollama:11434 when in Docker
processor = DocumentProcessor(ollama_url="http://localhost:11434")

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    model: str = "phi3:3.8b"
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model: str
    timestamp: str

class DocumentAnalysisRequest(BaseModel):
    analysis_type: str = "summary"

class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    metadata: Dict[str, Any]

class MtlCreateRequest(BaseModel):
    MTL_TITLE: str
    MTL_NUMBER: str
    VERSION_NUMBER: str
    REVISION_NUMBER: str
    CREATED_BY: str
    PRE_REQS: List[str] = []
    EQUIPMENT_LIST: List[str] = []
    COMPLETION_CRITERIA: List[str] = []
    STEPS: List[str] = []

import threading

# Persistent storage directories
DATA_DIR = Path("data/uploads")
DATA_DIR.mkdir(parents=True, exist_ok=True)
JSON_DIR = Path("data/processed")
JSON_DIR.mkdir(parents=True, exist_ok=True)

processed_documents: Dict[str, ProcessedDocument] = {}
json_templates: Dict[str, dict] = {}

def save_document(doc_id: str, processed_doc: ProcessedDocument):
    doc_path = DATA_DIR / f"{doc_id}.json"
    with open(doc_path, "w", encoding="utf-8") as f:
        json.dump({
            "filename": processed_doc.filename,
            "content": processed_doc.content,
            "metadata": processed_doc.metadata,
            "chunks": processed_doc.chunks,
            "embeddings": processed_doc.embeddings,
            "processed_at": processed_doc.processed_at
        }, f, indent=2, ensure_ascii=False)

def load_documents():
    docs = {}
    for file in DATA_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            docs[file.stem] = ProcessedDocument(
                filename=data["filename"],
                content=data["content"],
                metadata=data["metadata"],
                chunks=data["chunks"],
                embeddings=data.get("embeddings"),
                processed_at=data.get("processed_at")
            )
    return docs

def save_json(doc_id: str, mtl_json: dict):
    json_path = JSON_DIR / f"{doc_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(mtl_json, f, indent=2, ensure_ascii=False)

def load_json_templates():
    templates = {}
    for file in JSON_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            templates[file.stem] = json.load(f)
    return templates
@app.post("/api/process-document")
async def api_process_document(file: UploadFile = File(...)):
    """Process uploaded document and return AI-generated MTL JSON."""
    try:
        original_filename = file.filename or ''
        suffix = Path(original_filename).suffix if original_filename else ''
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        try:
            processed_doc = processor.process_document(tmp_file_path)
            processed_doc.filename = original_filename  # Store original filename
            doc_id = str(uuid.uuid4())
            processed_documents[doc_id] = processed_doc
            save_document(doc_id, processed_doc)
            # Use new AI extraction method for MTL JSON
            mtl_json = processor.extract_mtl_json(processed_doc, mtl_type="MTL 2")
            json_templates[doc_id] = mtl_json
            save_json(doc_id, mtl_json)
            return {"success": True, "json_template": mtl_json, "doc_id": doc_id}
        finally:
            os.unlink(tmp_file_path)
    except Exception as e:
        return {"success": False, "error": str(e)}
@app.post("/api/save-json")
async def api_save_json(request: Request):
    """Save edited JSON template in persistent storage"""
    try:
        data = await request.json()
        json_data = data.get("json")
        doc_id = data.get("doc_id")
        if not json_data:
            return {"success": False, "error": "No JSON data provided."}
        if doc_id:
            json_templates[doc_id] = json_data
            save_json(doc_id, json_data)
        else:
            doc_id = str(uuid.uuid4())
            json_templates[doc_id] = json_data
            save_json(doc_id, json_data)
        return {"success": True, "doc_id": doc_id}
    except Exception as e:
        return {"success": False, "error": str(e)}
@app.post("/api/generate-mtl")
async def api_generate_mtl(request: Request):
    """Generate MTL DOCX from JSON and return as file download"""
    try:
        data = await request.json()
        json_data = data.get("json")
        if not json_data:
            raise HTTPException(status_code=400, detail="No JSON data provided.")
        # Use final_mtl_generator.py or mtl_generator.py logic
        from MTL.mtl_generator import MTLGenerator
        import datetime
        # Save JSON to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=2, ensure_ascii=False)
            json_path = json_file.name
        # Generate DOCX to temp file
        output_path = json_path.replace(".json", ".docx")
        try:
            generator = MTLGenerator(json_path)
            generator.generate_document(output_path=output_path)
            # Return DOCX file
            return FileResponse(output_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="MTL_Generated.docx")
        finally:
            # Clean up temp files after response
            def cleanup():
                try:
                    os.unlink(json_path)
                except Exception:
                    pass
                try:
                    os.unlink(output_path)
                except Exception:
                    pass
            import threading
            threading.Timer(10, cleanup).start()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the React SPA"""
    try:
        # Always serve the React SPA - no fallback needed
        spa_index = Path("frontend/dist/index.html")
        if spa_index.exists() and spa_index.stat().st_size > 0:
            return FileResponse(spa_index, media_type="text/html")
        else:
            return HTMLResponse(content="<h1>React SPA not built. Run 'npm run build' in frontend directory.</h1>", status_code=500)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading React SPA: {e}</h1>", status_code=500)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI model"""
    try:
        import requests
        from datetime import datetime
        
        response = requests.post(
            f"{processor.ollama_url}/api/generate",
            json={
                "model": "phi3:3.8b",
                "prompt": request.message,
                "stream": False,
                "context": request.context
            },
            timeout=60
        );
        
        if response.status_code == 200:
            result = response.json();
            return ChatResponse(
                response=result.get('response', 'No response generated'),
                model=request.model,
                timestamp=datetime.now().isoformat()
            );
        else:
            raise HTTPException(status_code=500, detail="Failed to get response from AI model");
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e));

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    analysis_type: str = "summary"
):
    """Upload and analyze a document"""
    try:
        # Save uploaded file temporarily
        suffix = Path(file.filename).suffix if file.filename else ''
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Process the document
            processed_doc = processor.process_document(tmp_file_path)
            
            # Generate a unique ID and store
            doc_id = f"doc_{len(processed_documents) + 1}"
            processed_documents[doc_id] = processed_doc
            
            # Analyze the document
            analysis = processor.analyze_document(processed_doc, analysis_type)
            
            return {
                "message": "Document processed successfully",
                "document_id": doc_id,
                "metadata": {
                    "filename": processed_doc.filename,
                    "file_type": processed_doc.metadata.get("file_type"),
                    "word_count": processed_doc.metadata.get("word_count"),
                    "chunks": processed_doc.metadata.get("chunks_count")
                },
                "analysis": analysis
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Get system status"""
    try:
        import requests
        # Check Ollama status
        try:
            response = requests.get(f"{processor.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = [model["name"] for model in response.json().get("models", [])]
                ollama_status = "✅ Running"
            else:
                models = []
                ollama_status = "❌ Error"
        except Exception:
            models = []
            ollama_status = "❌ Not available"
        return {
            "ollama_status": ollama_status,
            "models": models,
            "processed_documents": len(processed_documents),
            "api_status": "✅ Running"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """List all processed documents"""
    docs = load_documents()
    return {
        "documents": [
            {
                "id": doc_id,
                "filename": doc.filename,
                "processed_at": doc.processed_at,
                "metadata": doc.metadata
            }
            for doc_id, doc in docs.items()
        ]
    }

@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Get a specific processed document"""
    docs = load_documents()
    if document_id not in docs:
        raise HTTPException(status_code=404, detail="Document not found")
    doc = docs[document_id]
    return {
        "id": document_id,
        "filename": doc.filename,
        "content": doc.content[:1000] + "..." if len(doc.content) > 1000 else doc.content,
        "metadata": doc.metadata,
        "chunks_count": len(doc.chunks),
        "processed_at": doc.processed_at
    }

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a processed document and its JSON"""
    doc_path = DATA_DIR / f"{document_id}.json"
    json_path = JSON_DIR / f"{document_id}.json"
    deleted = False
    if doc_path.exists():
        doc_path.unlink()
        deleted = True
    if json_path.exists():
        json_path.unlink()
        deleted = True
    if deleted:
        return {"success": True, "message": f"Document {document_id} deleted."}
    else:
        raise HTTPException(status_code=404, detail="Document not found")

@app.put("/documents/{document_id}")
async def edit_document(document_id: str, request: Request):
    """Edit a processed document's JSON template"""
    data = await request.json()
    new_json = data.get("json")
    if not new_json:
        raise HTTPException(status_code=400, detail="No JSON data provided.")
    save_json(document_id, new_json)
    json_templates[document_id] = new_json
    return {"success": True, "message": f"Document {document_id} updated."}

@app.post("/mtl-create")
async def mtl_create(request: Request):
    """Create a new MTL JSON file from form data"""
    try:
        data = await request.json()
        # Validate required fields
        required = ["MTL_TITLE", "MTL_NUMBER", "VERSION_NUMBER", "REVISION_NUMBER", "CREATED_BY", "STEPS"]
        for field in required:
            if not data.get(field):
                return {"success": False, "detail": f"Missing required field: {field}"}
        # Prepare data for generator compatibility (add alternate keys)
        mtl_json = {
            "MTL_TITLE": data["MTL_TITLE"],
            "MTL_NUMBER": data["MTL_NUMBER"],
            "MTL_#": data["MTL_NUMBER"],
            "VERSION_NUMBER": data["VERSION_NUMBER"],
            "VERSION": data["VERSION_NUMBER"],
            "REVISION_NUMBER": data["REVISION_NUMBER"],
            "CREATED_BY": data["CREATED_BY"],
            "PRE_REQS": data.get("PRE_REQS", []),
            "EQUIPMENT_LIST": data.get("EQUIPMENT_LIST", []),
            "COMPLETION_CRITERIA": data.get("COMPLETION_CRITERIA", []),
            "STEPS": data["STEPS"],
            # For mtl_generator.py compatibility
            "title": data["MTL_TITLE"],
            "mtl_number": data["MTL_NUMBER"],
            "version": data["VERSION_NUMBER"],
            "created_date": "",  # Can be filled later
            "created_by": data["CREATED_BY"],
            "steps": data["STEPS"]
        }
        # Save to MTLs directory
        mtl_dir = Path("MTLs")
        mtl_dir.mkdir(exist_ok=True)
        filename = f"{data['MTL_NUMBER'].replace(' ', '_')}_{data['MTL_TITLE'].replace(' ', '_')}.json"
        filepath = mtl_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(mtl_json, f, indent=2, ensure_ascii=False)
        return {"success": True, "message": f"MTL saved as {filepath}"}
    except Exception as e:
        return {"success": False, "detail": str(e)}

# SPA catch-all route for client-side routing (MUST BE LAST)
@app.get("/{path:path}")
async def spa_catchall(path: str):
    """Catch-all route for SPA client-side routing"""
    # Only serve SPA for paths that don't conflict with API routes
    spa_index = Path("frontend/dist/index.html")
    if spa_index.exists():
        return FileResponse(spa_index, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Local AI Bot Web API")
    parser.add_argument('--port', type=int, default=8899, help='Port to run the server on')
    args = parser.parse_args()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=args.port,
        log_level="info",
        reload=False,
        timeout_keep_alive=300,
        timeout_graceful_shutdown=300
    )
