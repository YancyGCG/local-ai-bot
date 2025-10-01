from __future__ import annotations

from pathlib import Path

import pytest  # type: ignore[import]

from mtlgen import loader, render

_REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def sample_task() -> loader.LoadedTask:
    task_path = _REPO_ROOT / "examples" / "GEN5_Firmware_Flash.yaml"
    return loader.load_task(task_path)


def test_mtl2_markdown_contains_metadata(sample_task: loader.LoadedTask) -> None:
    context = render.build_context(sample_task.data, extras={"document_type": "MTL-2"})
    markdown = render.render_markdown("mtl-2.md", context)
    assert "Step 1" in markdown
    assert "MTL-2" in markdown
    assert "Tools Required" in markdown
