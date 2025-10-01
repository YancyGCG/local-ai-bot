from __future__ import annotations

"""Data loading and validation for MTL content."""

from dataclasses import dataclass
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

import yaml
from jsonschema import Draft7Validator, ValidationError

_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "mtl" / "schema" / "mtl.schema.yaml"


class MTLValidationError(Exception):
    """Raised when the provided task definition fails schema validation."""

    def __init__(self, errors: Iterable[ValidationError]):
        formatted = "\n".join(format_error(err) for err in errors)
        super().__init__(formatted)
        self.errors = list(errors)


def format_error(error: ValidationError) -> str:
    """Create a human readable validation error trace."""

    path = " / ".join(str(part) for part in error.absolute_path)
    location = path or "<root>"
    return f"{location}: {error.message}"


@dataclass
class LoadedTask:
    """Container for a validated task definition."""

    source_path: Path
    data: Dict[str, Any]


def load_task(path: Path, schema_path: Path | None = None) -> LoadedTask:
    """Load and validate an MTL task definition from YAML or JSON."""

    schema = _load_schema(schema_path)
    raw = _load_raw(path)
    errors = list(Draft7Validator(schema).iter_errors(raw))
    if errors:
        raise MTLValidationError(errors)

    enriched = _enrich(raw)
    return LoadedTask(source_path=path, data=enriched)


def _load_schema(schema_path: Path | None) -> Mapping[str, Any]:
    target = schema_path or _SCHEMA_PATH
    with target.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _load_raw(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Task file not found: {path}")

    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".json"}:
        import json

        return json.loads(text)

    return yaml.safe_load(text)


def validate_task_dict(payload: Dict[str, Any], schema_path: Path | None = None) -> Dict[str, Any]:
    """Validate a task definition provided as a dictionary."""

    schema = _load_schema(schema_path)
    errors = list(Draft7Validator(schema).iter_errors(payload))
    if errors:
        raise MTLValidationError(errors)

    return _enrich(payload)


def _enrich(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare derived fields to simplify template rendering."""

    payload = deepcopy(payload)
    steps: List[Dict[str, Any]] = []
    for idx, step in enumerate(payload.get("steps", []), start=1):
        step_copy = dict(step)
        step_copy.setdefault("critical", False)
        step_copy.setdefault("tips", [])
        step_copy.setdefault("warnings", [])
        step_copy.setdefault("confirm", "")
        step_copy.setdefault("screenshot", "")
        step_copy["sequence"] = idx
        steps.append(step_copy)

    payload["steps"] = steps

    rubric_entries = []
    for rub in payload.get("teachback", {}).get("rubric", []):
        entry = dict(rub)
        levels_map = {level["label"]: level.get("description", "") for level in entry.get("levels", [])}
        for label in ("Needs Work", "Good", "Better", "Best"):
            levels_map.setdefault(label, "")
        entry["levels_map"] = levels_map
        rubric_entries.append(entry)

    if "teachback" in payload:
        payload["teachback"]["rubric"] = rubric_entries

    return payload
