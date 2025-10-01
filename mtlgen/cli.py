from __future__ import annotations

"""Command line interface for the MTL generator."""

import argparse
import webbrowser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

from . import loader, pipeline, render

DOC_TYPES = ("mtl-1", "mtl-2", "mtl-3")
_TEMPLATE_MAP: Dict[str, str] = {doc_type: f"{doc_type}.md" for doc_type in DOC_TYPES}


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 1

    if args.command == "validate":
        return _cmd_validate(args)
    if args.command == "build":
        return _cmd_build(args)
    if args.command == "preview":
        return _cmd_preview(args)

    parser.error(f"Unknown command: {args.command}")
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mtlgen", description="MTL pack generation toolkit")
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="Validate a task definition against the schema")
    validate_parser.add_argument("task_path", type=Path, help="Path to the task YAML/JSON file")

    build_parser = subparsers.add_parser("build", help="Render outputs for all MTL surfaces")
    build_parser.add_argument("task_path", type=Path, help="Path to the task YAML/JSON file")
    build_parser.add_argument("--out", type=Path, required=True, help="Output directory for generated artifacts")
    build_parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent / "styles" / "mtl.docx",
        help="Optional DOCX template to seed styles",
    )

    preview_parser = subparsers.add_parser("preview", help="Render HTML and open in the default browser")
    preview_parser.add_argument("task_path", type=Path, help="Path to the task YAML/JSON file")
    preview_parser.add_argument("--doc", choices=sorted(_TEMPLATE_MAP), default="mtl-2")

    return parser


def _cmd_validate(args: argparse.Namespace) -> int:
    try:
        loader.load_task(args.task_path)
    except loader.MTLValidationError as exc:
        print("Validation failed:\n" + str(exc))
        return 1
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    print("Validation passed.")
    return 0


def _cmd_build(args: argparse.Namespace) -> int:
    try:
        task = loader.load_task(args.task_path)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to load task: {exc}")
        return 1

    output_dir = args.out
    output_dir.mkdir(parents=True, exist_ok=True)

    artifacts = pipeline.build_pack(task.data, output_dir, template_path=args.template)
    for artifact in artifacts:
        print(
            "Generated",
            artifact.doc_type,
            artifact.markdown.name,
            artifact.docx.name,
            artifact.pdf.name,
        )

    return 0


def _cmd_preview(args: argparse.Namespace) -> int:
    try:
        task = loader.load_task(args.task_path)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to load task: {exc}")
        return 1

    template = _TEMPLATE_MAP[args.doc]
    context = render.build_context(task.data, extras={"document_type": args.doc.upper()})
    html = render.render_full_html(template, context)

    with TemporaryDirectory() as temp_dir:
        preview_path = Path(temp_dir) / f"preview_{args.doc}.html"
        preview_path.write_text(html, encoding="utf-8")
        webbrowser.open(preview_path.as_uri())

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
