"""Utility helpers for filesystem access managed via environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

load_dotenv()

DOCS_DIR = Path(os.getenv("DOCS_DIR", "../data/uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "../data/outputs"))
PROCESSED_DIR = Path(os.getenv("PROCESSED_DIR", "../data/processed"))
LOG_DIR = Path(os.getenv("LOG_DIR", "../logs"))

_DIRECTORIES: Iterable[Path] = (DOCS_DIR, OUTPUT_DIR, PROCESSED_DIR, LOG_DIR)

for directory in _DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)


def resolve_under_output(*parts: str) -> Path:
    """Return a path rooted under the configured output directory."""

    return OUTPUT_DIR.joinpath(*parts)


def resolve_under_processed(*parts: str) -> Path:
    """Return a path rooted under the processed data directory."""

    return PROCESSED_DIR.joinpath(*parts)


def resolve_under_uploads(*parts: str) -> Path:
    """Return a path rooted under the uploads directory."""

    return DOCS_DIR.joinpath(*parts)


def resolve_log_path(filename: str) -> Path:
    """Return a path inside the log directory for the given file."""

    return LOG_DIR / filename
