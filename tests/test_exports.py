from __future__ import annotations

from pathlib import Path

import pytest  # type: ignore[import]

from mtlgen import export_docx, export_pdf, loader, pipeline, render

_REPO_ROOT = Path(__file__).resolve().parents[1]
_TEMPLATE = _REPO_ROOT / "mtlgen" / "styles" / "mtl.docx"


@pytest.fixture(scope="module")
def sample_task() -> loader.LoadedTask:
    task_path = _REPO_ROOT / "examples" / "GEN5_Firmware_Flash.yaml"
    return loader.load_task(task_path)


@pytest.mark.parametrize("doc_type", ["mtl-1", "mtl-2", "mtl-3"])
def test_export_docx_creates_file(tmp_path: Path, sample_task: loader.LoadedTask, doc_type: str) -> None:
    output_path = tmp_path / f"{doc_type}.docx"
    export_docx.export_docx(sample_task.data, doc_type, output_path, template_path=_TEMPLATE)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_export_pdf_creates_file(tmp_path: Path, sample_task: loader.LoadedTask) -> None:
    pytest.importorskip("weasyprint")
    context = render.build_context(sample_task.data, extras={"document_type": "MTL-2"})
    html = render.render_full_html("mtl-2.md", context)
    output_path = tmp_path / "MTL-2.pdf"
    export_pdf.export_pdf(html, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_pipeline_creates_all_outputs(tmp_path: Path, sample_task: loader.LoadedTask) -> None:
    artifacts = pipeline.build_pack(sample_task.data, tmp_path, template_path=_TEMPLATE)
    assert len(artifacts) == 3
    for artifact in artifacts:
        assert artifact.markdown.exists()
        assert artifact.docx.exists()
        assert artifact.pdf.exists()
