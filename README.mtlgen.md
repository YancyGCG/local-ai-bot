# MTL Generator Toolkit

The `mtlgen` package builds standardized MTL deliverables (Markdown, DOCX, PDF) from a single YAML definition. The initial milestone focuses on the MTL-2 walkthrough document while laying the groundwork for future surfaces.

## Installation

```bash
# from repo root
pip install -r requirements.txt
```

## Usage

```bash
# Validate a task definition
python -m mtlgen.cli validate examples/GEN5_Firmware_Flash.yaml

# Build MTL-2 artifacts
python -m mtlgen.cli build examples/GEN5_Firmware_Flash.yaml --out dist/GEN5_Firmware_Flash/

# Preview HTML in the browser
python -m mtlgen.cli preview examples/GEN5_Firmware_Flash.yaml
```

Outputs are generated on demand and are not committed. The CLI currently produces:

- `MTL-2_*.md`
- `MTL-2_*.docx`
- `MTL-2_*.pdf`

## Project Layout

- `mtl/schema/mtl.schema.yaml` – JSON Schema used for validation
- `mtl/templates/` – Jinja2 templates for Markdown surfaces
- `mtlgen/` – Python package with loader, renderer, and export helpers
- `examples/GEN5_Firmware_Flash.yaml` – Sample task definition used in tests
- `tests/` – Unit tests covering validation, rendering, and exports

## DOCX Styling

`mtlgen/styles/mtl.docx` is cloned from the legacy MTL-2 template and reused for consistent fonts, margins, and numbering. The exporter falls back to neutral formatting if a requested style is missing so the build never fails.

## PDF Pipeline

HTML is rendered with `markdown-it-py` and inlined CSS (`mtlgen/assets/styles.css`), then converted to PDF through WeasyPrint. Update the stylesheet to adjust colors, typography, or page layout.

## Next Steps

- Extend `export_docx` to cover MTL-1 and MTL-3 layouts.
- Add screenshot asset handling/copying.
- Enrich templates with numbered callouts per `NUMBERING_FORMAT.md` guidance.
- Update `LMS-DEV-SPEC.md` once ingestion details are finalized.
