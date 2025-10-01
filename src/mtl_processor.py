"""End-to-end orchestration for processing documents into MTL packs."""

from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from dotenv import load_dotenv

from mtlgen import pipeline
from mtlgen.pipeline import ArtifactSet
from src.document_processor import DocumentProcessor, ProcessedDocument
from src.quiz_generator import build_quiz_payload
from src.utils.file_utils import DOCS_DIR, OUTPUT_DIR, PROCESSED_DIR

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

_PROCESSOR = DocumentProcessor(ollama_url=OLLAMA_URL)
_PROCESSED_CACHE: Dict[str, ProcessedDocument] = {}
_TASK_CACHE: Dict[str, Dict[str, Any]] = {}

_DOCUMENTS_DIR = PROCESSED_DIR / "documents"
_TASKS_DIR = PROCESSED_DIR / "tasks"
for directory in (_DOCUMENTS_DIR, _TASKS_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def get_processor() -> DocumentProcessor:
    """Expose the shared document processor instance."""

    return _PROCESSOR


def process_upload(temp_path: Path, original_filename: str) -> Dict[str, Any]:
    """Process an uploaded file and generate the associated MTL pack."""

    doc_id = str(uuid.uuid4())
    stored_upload = _persist_upload(temp_path, doc_id, original_filename)

    processed_doc = _PROCESSOR.process_document(str(temp_path))
    processed_doc.filename = original_filename
    processed_doc.processed_at = processed_doc.processed_at or datetime.utcnow().isoformat()
    processed_doc.metadata.setdefault("stored_path", str(stored_upload))

    _persist_processed_document(doc_id, processed_doc)

    task_data = _PROCESSOR.extract_mtl_task(processed_doc, mtl_number="MTL 2")  # type: ignore[attr-defined]
    _persist_task_data(doc_id, task_data)

    artifact_dir = OUTPUT_DIR / doc_id
    artifacts = pipeline.build_pack(task_data, artifact_dir)
    quiz_items = build_quiz_payload(task_data)

    return {
        "doc_id": doc_id,
        "processed": processed_doc,
        "task": task_data,
        "artifacts": _serialize_artifacts(artifacts),
        "quiz": quiz_items,
    }


def list_documents() -> List[Dict[str, Any]]:
    """Return metadata for all processed documents."""

    documents: List[Dict[str, Any]] = []
    for doc_id in _iter_document_ids():
        processed = get_processed_document(doc_id)
        documents.append(
            {
                "id": doc_id,
                "filename": processed.filename,
                "processed_at": processed.processed_at,
                "metadata": processed.metadata,
            }
        )
    return documents


def get_processed_document(doc_id: str) -> ProcessedDocument:
    """Load a processed document from cache or disk."""

    if doc_id in _PROCESSED_CACHE:
        return _PROCESSED_CACHE[doc_id]

    path = _DOCUMENTS_DIR / f"{doc_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Processed document not found: {doc_id}")

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    processed = ProcessedDocument(
        filename=payload["filename"],
        content=payload["content"],
        metadata=payload["metadata"],
        chunks=payload["chunks"],
        embeddings=payload.get("embeddings"),
        processed_at=payload.get("processed_at"),
    )
    _PROCESSED_CACHE[doc_id] = processed
    return processed


def get_task_data(doc_id: str) -> Dict[str, Any]:
    """Load the structured task data for a document."""

    if doc_id in _TASK_CACHE:
        return _TASK_CACHE[doc_id]

    path = _TASKS_DIR / f"{doc_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Task data not found: {doc_id}")

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    _TASK_CACHE[doc_id] = data
    return data


def save_task_data(doc_id: str, task_data: Dict[str, Any]) -> None:
    """Persist updated task data back to disk."""

    _persist_task_data(doc_id, task_data)


def delete_document(doc_id: str) -> None:
    """Delete all persisted artifacts associated with a document."""

    for path in (
        _DOCUMENTS_DIR / f"{doc_id}.json",
        _TASKS_DIR / f"{doc_id}.json",
    ):
        if path.exists():
            path.unlink()

    artifact_dir = OUTPUT_DIR / doc_id
    if artifact_dir.exists():
        shutil.rmtree(artifact_dir)

    upload_dir = DOCS_DIR / doc_id
    if upload_dir.exists():
        shutil.rmtree(upload_dir)

    _PROCESSED_CACHE.pop(doc_id, None)
    _TASK_CACHE.pop(doc_id, None)


def _persist_upload(temp_path: Path, doc_id: str, original_filename: str) -> Path:
    upload_dir = DOCS_DIR / doc_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / original_filename
    shutil.copy2(temp_path, destination)
    return destination


def _persist_processed_document(doc_id: str, processed_doc: ProcessedDocument) -> None:
    payload = asdict(processed_doc)
    path = _DOCUMENTS_DIR / f"{doc_id}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    _PROCESSED_CACHE[doc_id] = processed_doc


def _persist_task_data(doc_id: str, task_data: Dict[str, Any]) -> None:
    path = _TASKS_DIR / f"{doc_id}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(task_data, handle, indent=2, ensure_ascii=False)
    _TASK_CACHE[doc_id] = task_data


def _serialize_artifacts(artifacts: Iterable[ArtifactSet]) -> List[Dict[str, str]]:
    serialized: List[Dict[str, str]] = []
    for artifact in artifacts:
        serialized.append(
            {
                "doc_type": artifact.doc_type,
                "markdown": str(artifact.markdown),
                "docx": str(artifact.docx),
                "pdf": str(artifact.pdf),
            }
        )
    return serialized


def _iter_document_ids() -> Iterable[str]:
    for path in _DOCUMENTS_DIR.glob("*.json"):
        yield path.stem
