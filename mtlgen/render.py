from __future__ import annotations

"""Template rendering helpers."""

from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "mtl" / "templates"
_ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def _create_environment() -> Environment:
    loader = FileSystemLoader(str(_TEMPLATES_DIR))
    env = Environment(loader=loader, autoescape=select_autoescape(enabled_extensions=(".html", "htm")))
    env.globals.update({
        "ASSETS_DIR": _ASSETS_DIR,
    })
    return env


_ENV = _create_environment()


def build_context(task: Dict[str, Any], *, extras: Dict[str, Any] | None = None) -> Dict[str, Any]:
    context = dict(task)
    if extras:
        context.update(extras)
    return context


def render_markdown(template_name: str, context: Dict[str, Any]) -> str:
    template = _ENV.get_template(template_name)
    return template.render(**context)


def markdown_to_html(markdown_text: str, *, title: str | None = None, css_path: Path | None = None) -> str:
    md = MarkdownIt("commonmark", {})
    md.enable("table")
    md.enable("strikethrough")
    body = md.render(markdown_text)
    css = css_path.read_text(encoding="utf-8") if css_path else ""
    title_tag = title or "MTL Document"
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        f"  <meta charset=\"utf-8\" />\n"
        f"  <title>{title_tag}</title>\n"
        f"  <style>{css}</style>\n"
        "</head>\n"
        "<body>\n"
        f"{body}\n"
        "</body>\n"
        "</html>"
    )


def render_full_html(template_name: str, context: Dict[str, Any], *, css_name: str = "styles.css") -> str:
    markdown_output = render_markdown(template_name, context)
    css_path = _ASSETS_DIR / css_name
    return markdown_to_html(markdown_output, title=context.get("meta", {}).get("title"), css_path=css_path)
