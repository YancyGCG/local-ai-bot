print('=== web_api.py is running ===')

"""
FastAPI application for the Local AI Bot backend.
"""

from __future__ import annotations

import json
import logging
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src import mtl_processor
from src.document_processor import ProcessedDocument


app = FastAPI(
    title="Local AI Bot API",
    description="Private document processing and AI chat API",
    version="1.0.0",
)

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
DATA_DIRECTORY = Path("data")
if DATA_DIRECTORY.exists():
    app.mount("/data", StaticFiles(directory=DATA_DIRECTORY), name="data")

SPA_INDEX = Path("frontend/dist/index.html")
if SPA_INDEX.exists():
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = mtl_processor.get_processor()


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


@app.post("/api/process-document")
async def api_process_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Process an uploaded document and build the full MTL pack."""

    original_filename = file.filename or "uploaded_document"
    suffix = Path(original_filename).suffix

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(await file.read())
        temp_path = Path(tmp_file.name)

    try:
        result = mtl_processor.process_upload(temp_path, original_filename)
        return {
            "success": True,
            "doc_id": result["doc_id"],
            "task": result["task"],
            "artifacts": result["artifacts"],
            "quiz": result["quiz"],
        }
    except Exception as exc:  # pragma: no cover - depends on external LLM
        logging.exception("Failed to process document")
        return {"success": False, "error": str(exc)}
    finally:
        if temp_path.exists():
            temp_path.unlink()


@app.post("/api/save-json")
async def api_save_json(request: Request) -> Dict[str, Any]:
    """Persist edited task data associated with a processed document."""

    payload = await request.json()
    task_data = payload.get("json")
    if not task_data:
        return {"success": False, "error": "No JSON data provided."}

    doc_id = payload.get("doc_id") or str(uuid.uuid4())
    try:
        mtl_processor.save_task_data(doc_id, task_data)
    except Exception as exc:
        logging.exception("Failed to save task data")
        return {"success": False, "error": str(exc)}

    return {"success": True, "doc_id": doc_id}


@app.post("/api/generate-mtl")
async def api_generate_mtl(request: Request) -> FileResponse:
    """Generate an MTL DOCX using the legacy generator."""

    data = await request.json()
    json_data = data.get("json")
    if not json_data:
        raise HTTPException(status_code=400, detail="No JSON data provided.")

    from MTL.mtl_generator import MTLGenerator

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)
        json_path = Path(json_file.name)

    output_path = json_path.with_suffix(".docx")
    try:
        generator = MTLGenerator(str(json_path))
        generator.generate_document(output_path=str(output_path))
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="MTL_Generated.docx",
        )
    finally:
        def _cleanup() -> None:
            for path in (json_path, output_path):
                try:
                    if path.exists():
                        path.unlink()
                except Exception:  # pragma: no cover
                    pass

        import threading

        threading.Timer(10, _cleanup).start()


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Serve the compiled React SPA when available."""

    if SPA_INDEX.exists() and SPA_INDEX.stat().st_size > 0:
        return FileResponse(SPA_INDEX, media_type="text/html")

    return HTMLResponse(
        content="<h1>React SPA not built. Run 'npm run build' in frontend directory.</h1>",
        status_code=500,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Proxy chat requests to the configured Ollama instance."""

    response = requests.post(
        f"{processor.ollama_url}/api/generate",
        json={
            "model": request.model,
            "prompt": request.message,
            "stream": False,
            "context": request.context,
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get response from AI model")

    result = response.json()
    return ChatResponse(
        response=result.get("response", "No response generated"),
        model=request.model,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    analysis_type: str = "summary",
) -> Dict[str, Any]:
    """Legacy document upload endpoint that performs analysis only."""

    suffix = Path(file.filename or "uploaded").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(await file.read())
        temp_path = Path(tmp_file.name)

    try:
        result = mtl_processor.process_upload(temp_path, file.filename or "uploaded")
        processed_doc: ProcessedDocument = result["processed"]
        analysis = processor.analyze_document(processed_doc, analysis_type)
        return {
            "message": "Document processed successfully",
            "document_id": result["doc_id"],
            "metadata": {
                "filename": processed_doc.filename,
                "file_type": processed_doc.metadata.get("file_type"),
                "word_count": processed_doc.metadata.get("word_count"),
                "chunks": processed_doc.metadata.get("chunks_count"),
            },
            "analysis": analysis,
        }
    finally:
        if temp_path.exists():
            temp_path.unlink()


@app.get("/status")
async def get_status() -> Dict[str, Any]:
    """Return health information about the backend and Ollama."""

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
        "processed_documents": len(mtl_processor.list_documents()),
        "api_status": "✅ Running",
    }


@app.get("/documents")
async def list_documents() -> Dict[str, Any]:
    """List metadata for all processed documents."""

    return {"documents": mtl_processor.list_documents()}


@app.get("/documents/{document_id}")
async def get_document(document_id: str) -> Dict[str, Any]:
    """Retrieve a processed document and its structured task data."""

    try:
        processed = mtl_processor.get_processed_document(document_id)
        task_data = mtl_processor.get_task_data(document_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")

    preview = processed.content
    if len(preview) > 1000:
        preview = f"{preview[:1000]}..."

    return {
        "id": document_id,
        "filename": processed.filename,
        "content": preview,
        "metadata": processed.metadata,
        "chunks_count": len(processed.chunks),
        "processed_at": processed.processed_at,
        "task": task_data,
    }


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str) -> Dict[str, Any]:
    """Remove a processed document and all derived artifacts."""

    try:
        mtl_processor.delete_document(document_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"success": True, "message": f"Document {document_id} deleted."}


@app.put("/documents/{document_id}")
async def edit_document(document_id: str, request: Request) -> Dict[str, Any]:
    """Update the structured task data for a processed document."""

    payload = await request.json()
    task_data = payload.get("json")
    if not task_data:
        raise HTTPException(status_code=400, detail="No JSON data provided.")

    mtl_processor.save_task_data(document_id, task_data)
    return {"success": True, "message": f"Document {document_id} updated."}


@app.post("/mtl-create")
async def mtl_create(request: Request) -> Dict[str, Any]:
    """Create a new task payload suitable for manual editing."""

    data = await request.json()
    required = [
        "MTL_TITLE",
        "MTL_NUMBER",
        "VERSION_NUMBER",
        "REVISION_NUMBER",
        "CREATED_BY",
        "STEPS",
    ]
    for field in required:
        if not data.get(field):
            return {"success": False, "detail": f"Missing required field: {field}"}

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
        "title": data["MTL_TITLE"],
        "mtl_number": data["MTL_NUMBER"],
        "version": data["VERSION_NUMBER"],
        "created_date": data.get("CREATED_DATE", ""),
        "created_by": data["CREATED_BY"],
        "steps": data["STEPS"],
    }

    doc_id = str(uuid.uuid4())
    mtl_processor.save_task_data(doc_id, mtl_json)
    return {"success": True, "doc_id": doc_id, "message": "MTL saved."}


@app.get("/{path:path}")
async def spa_catchall(path: str) -> HTMLResponse:
    """Serve the SPA for any unmatched routes."""

    if SPA_INDEX.exists():
        return FileResponse(SPA_INDEX, media_type="text/html")

    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Local AI Bot Web API")
    parser.add_argument("--port", type=int, default=8899, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=args.port,
        log_level="info",
        reload=False,
        timeout_keep_alive=300,
        timeout_graceful_shutdown=300,
    )
