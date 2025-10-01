"""Application entrypoint for the Local AI Bot service."""

from __future__ import annotations

import os

import uvicorn
from dotenv import load_dotenv

from src.web_api import app  # noqa: E402  # ensure FastAPI app is imported
from src.utils.file_utils import DOCS_DIR, LOG_DIR, OUTPUT_DIR, PROCESSED_DIR  # noqa: F401

load_dotenv()


def _default_host() -> str:
    return os.getenv("APP_HOST", "0.0.0.0")


def _default_port() -> int:
    try:
        return int(os.getenv("APP_PORT", "8899"))
    except ValueError:
        return 8899


def run() -> None:
    """Launch the FastAPI application using Uvicorn."""

    uvicorn.run(
        app,
        host=_default_host(),
        port=_default_port(),
        log_level=os.getenv("APP_LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    run()
