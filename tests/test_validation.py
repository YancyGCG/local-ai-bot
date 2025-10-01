from __future__ import annotations

from pathlib import Path

import pytest  # type: ignore[import]

from mtlgen import loader

_REPO_ROOT = Path(__file__).resolve().parents[1]
_EXAMPLES = _REPO_ROOT / "examples"


@pytest.fixture(scope="module")
def sample_task_path() -> Path:
    return _EXAMPLES / "GEN5_Firmware_Flash.yaml"


def test_loads_valid_sample(sample_task_path: Path) -> None:
    task = loader.load_task(sample_task_path)
    assert task.data["meta"]["title"] == "GEN5 Firmware Flash"
    assert all(step["sequence"] == idx for idx, step in enumerate(task.data["steps"], start=1))
    rubric = task.data["teachback"]["rubric"][0]
    assert set(rubric["levels_map"].keys()) == {"Needs Work", "Good", "Better", "Best"}


def test_invalid_date_fails_validation(sample_task_path: Path, tmp_path: Path) -> None:
    bad_path = tmp_path / "invalid.yaml"
    content = sample_task_path.read_text(encoding="utf-8").replace("10-01-25", "2025-10-01")
    bad_path.write_text(content, encoding="utf-8")

    with pytest.raises(loader.MTLValidationError) as excinfo:
        loader.load_task(bad_path)

    assert "last_updated" in str(excinfo.value)
