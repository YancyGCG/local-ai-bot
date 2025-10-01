from __future__ import annotations

"""HTML to PDF export utilities."""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import only for type checking
    from weasyprint import HTML  # type: ignore

def export_pdf(html_content: str, output_path: Path) -> Path:
    """Render HTML into a PDF file."""

    try:
        from weasyprint import HTML  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised via runtime
        raise RuntimeError(
            "weasyprint is required for PDF export. Install it via pip install weasyprint"
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_content, base_url=str(output_path.parent)).write_pdf(str(output_path))
    return output_path
