from __future__ import annotations

"""High-level orchestration utilities for generating full MTL packs."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from . import export_docx, export_pdf, render

_DOC_TYPES = ("mtl-1", "mtl-2", "mtl-3")
_DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "styles" / "mtl.docx"


@dataclass(slots=True)
class ArtifactSet:
    """Output file paths for a single MTL surface."""

    doc_type: str
    markdown: Path
    docx: Path
    pdf: Path


def build_base_filename(doc_type: str, meta: Dict[str, str]) -> str:
    task_slug = meta.get("task_id", "task").replace(" ", "_").replace("/", "-")
    version = meta.get("version", "v1")
    return f"{doc_type.upper()}_{task_slug}_{version}"


def build_pack(
    task_data: Dict,
    output_dir: Path,
    *,
    template_path: Path | None = None,
    css_name: str = "styles.css",
) -> List[ArtifactSet]:
    """Render Markdown, DOCX, and PDF outputs for the provided task data."""

    output_dir.mkdir(parents=True, exist_ok=True)
    template = template_path or _DEFAULT_TEMPLATE

    artifacts: List[ArtifactSet] = []
    for doc_type in _DOC_TYPES:
        context = render.build_context(task_data, extras={"document_type": doc_type.upper()})
        template_name = f"{doc_type}.md"
        markdown = render.render_markdown(template_name, context)
        html = render.render_full_html(template_name, context, css_name=css_name)

        base_name = build_base_filename(doc_type, task_data.get("meta", {}))
        md_path = output_dir / f"{base_name}.md"
        docx_path = output_dir / f"{base_name}.docx"
        pdf_path = output_dir / f"{base_name}.pdf"

        md_path.write_text(markdown, encoding="utf-8")
        export_docx.export_docx(task_data, doc_type, docx_path, template_path=template)
        export_pdf.export_pdf(html, pdf_path)

        artifacts.append(ArtifactSet(doc_type=doc_type, markdown=md_path, docx=docx_path, pdf=pdf_path))

    return artifacts
