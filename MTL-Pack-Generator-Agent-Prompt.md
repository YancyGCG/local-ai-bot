# MTL Pack Generator — VS Code Agent Prompt

**Purpose:** Guide the agent to generate clean, multi‑file MTL packs (MTL‑1/2/3) from a single structured source, export to Markdown/DOCX/PDF, and update `LMS-DEV-SPEC.md`—without breaking existing code.

---

## Role & Guardrails
- Work locally in a new feature branch: `feature/mtl-pack-generator`.
- Do **not** delete or rewrite existing app logic; encapsulate changes in new modules.
- Make small, reviewable commits with clear messages.
- Write deterministic code and unit tests. No flaky network calls.
- Use **MM-DD-YY** for dates unless explicitly set in content.
- Content **source of truth** = one YAML or JSON file per task. Render to MTL‑1/2/3 (Markdown → DOCX/PDF).

---

## Deliverables (Definition of Done)

1) **Schema & Templates**
- `/mtl/schema/mtl.schema.yaml` — strict schema for all MTLs.
- `/mtl/templates/mtl-1.md`, `/mtl/templates/mtl-2.md`, `/mtl/templates/mtl-3.md`.
- Shared partials: `/mtl/templates/partials/*` (callouts, tool lists, step blocks).

2) **Generator CLI**
- Python package `mtlgen/` with CLI:  
  `python -m mtlgen build path/to/task.yaml --out dist/MTL_NAME/`
- Outputs:
  - `MTL-1.md`, `MTL-2.md`, `MTL-3.md`
  - `MTL-1.docx`, `MTL-2.docx`, `MTL-3.docx`
  - `MTL-1.pdf`, `MTL-2.pdf`, `MTL-3.pdf`
- Screenshot support: copy local images from `assets/screenshots/` and embed with captions.

3) **Formatting**
- DOCX via `python-docx` with custom styles.
- PDF via **WeasyPrint** (HTML→PDF) *or* `wkhtmltopdf` (choose one; document the choice).

4) **Validation & Tests**
- JSON Schema or Pydantic validation.
- Unit tests for: schema validation, template rendering, export pipeline.

5) **Docs**
- `README.mtlgen.md` (install, usage, schema examples).
- Update `LMS-DEV-SPEC.md` with: data model, pipeline, file outputs, and how LMS ingests these.

6) **Sample Pack**
- `examples/GEN5_Firmware_Flash.yaml` → full build in `dist/GEN5_Firmware_Flash/`.

---

## Content Schema (author‑friendly, strict)

Create `mtl.schema.yaml`:

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: MTL Task
type: object
required: [meta, tools_required, prerequisites, steps, confirmations, teachback]
properties:
  meta:
    type: object
    required: [task_id, title, version, owner, last_updated, estimated_time_min, difficulty, tags]
    properties:
      task_id: { type: string }
      title: { type: string }
      version: { type: string }
      owner: { type: string }
      last_updated: { type: string, pattern: "^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-\\d{2}$" } # MM-DD-YY
      estimated_time_min: { type: integer }
      difficulty: { type: string, enum: [Beginner, Intermediate, Advanced] }
      tags: { type: array, items: { type: string } }
  tools_required:
    type: array
    items:
      type: object
      required: [name]
      properties:
        name: { type: string }
        qty: { type: string }
        notes: { type: string }
  prerequisites:
    type: array
    items: { type: string }
  environment:
    type: object
    properties:
      models: { type: array, items: { type: string } }
      sw_versions: { type: array, items: { type: string } }
      connections: { type: array, items: { type: string } }
  steps:
    type: array
    items:
      type: object
      required: [id, text]
      properties:
        id: { type: string }
        text: { type: string }
        critical: { type: boolean, default: false }
        confirm: { type: string }   # what success looks like
        screenshot: { type: string } # relative path
        tips: { type: array, items: { type: string } }
        warnings: { type: array, items: { type: string } }
  confirmations:
    type: array
    items:
      type: object
      required: [item, accept]
      properties:
        item: { type: string }
        accept: { type: array, items: { type: string } } # acceptable outcomes
  teachback:
    type: object
    required: [prompts, rubric]
    properties:
      prompts:
        type: array
        items: { type: string }
      rubric:
        type: array
        items:
          type: object
          required: [criterion, levels]
          properties:
            criterion: { type: string }
            levels:
              type: array
              items:
                type: object
                required: [label, description]
                properties:
                  label: { type: string, enum: [Needs Work, Good, Better, Best] }
                  description: { type: string }
  signoff:
    type: object
    properties:
      trainee_name: { type: string }
      trainer_name: { type: string }
      date: { type: string }
```

Provide a matching example at `examples/GEN5_Firmware_Flash.yaml` using realistic content and 2–3 sample screenshots.

---

## Markdown Templates (MTL‑1/2/3)

Create **Jinja2** Markdown templates:

`/mtl/templates/mtl-1.md`
```md
# {{ meta.title }} — MTL-1 (At-a-Glance)

**Task ID:** {{ meta.task_id }}  
**Version:** {{ meta.version }} • **Owner:** {{ meta.owner }} • **Updated:** {{ meta.last_updated }}  
**Difficulty:** {{ meta.difficulty }} • **Est. Time:** {{ meta.estimated_time_min }} min  
**Tags:** {{ meta.tags | join(", ") }}

## Purpose
Brief: why this matters and when to run it.

## Tools Required
{% for t in tools_required %}- **{{t.name}}**{% if t.qty %} ({{t.qty}}){% endif %}{% if t.notes %} — {{t.notes}}{% endif %}
{% endfor %}

## Prerequisites
{% for p in prerequisites %}- {{p}}
{% endfor %}

## Success Criteria (Confirmations)
{% for c in confirmations %}- **{{ c.item }}** → Accept: {{ c.accept | join("; ") }}
{% endfor %}
```

`/mtl/templates/mtl-2.md`
```md
# {{ meta.title }} — MTL-2 (Detailed Walkthrough)

> **CRITICAL steps are flagged.** Complete confirmations after each major action.

## Environment
- Models: {{ environment.models | default([]) | join(", ") }}
- Software Versions: {{ environment.sw_versions | default([]) | join(", ") }}
- Connections: {{ environment.connections | default([]) | join(", ") }}

## Tools Required
{% for t in tools_required %}- **{{t.name}}**{% if t.qty %} ({{t.qty}}){% endif %}{% if t.notes %} — {{t.notes}}{% endif %}
{% endfor %}

## Step-by-Step
{% for s in steps %}
### Step {{ loop.index }} — {{ s.id }}
{% if s.critical %}**CRITICAL:** {% endif %}{{ s.text }}

{% if s.screenshot %}![screenshot]({{ s.screenshot }})  
*Figure {{ loop.index }}: {{ s.id }}*{% endif %}

{% if s.warnings and s.warnings|length %}> **Warnings:**  
> {% for w in s.warnings %}- {{ w }}
> {% endfor %}{% endif %}

{% if s.tips and s.tips|length %}> **Tips:**  
> {% for t in s.tips %}- {{ t }}
> {% endfor %}{% endif %}

{% if s.confirm %}**Confirm:** {{ s.confirm }}{% endif %}

---
{% endfor %}

## Final Confirmations
{% for c in confirmations %}- **{{ c.item }}** → Accept: {{ c.accept | join("; ") }}
{% endfor %}
```

`/mtl/templates/mtl-3.md`
```md
# {{ meta.title }} — MTL-3 (Teachback & Sign-off)

## Teachback Prompts
{% for p in teachback.prompts %}- {{ p }}
{% endfor %}

## Rubric (Needs Work → Best)
| Criterion | Needs Work | Good | Better | Best |
|---|---|---|---|---|
{% for r in teachback.rubric -%}
| {{ r.criterion }} | {{ (r.levels | selectattr("label","equalto","Needs Work") | list)[0].description }} | {{ (r.levels | selectattr("label","equalto","Good") | list)[0].description }} | {{ (r.levels | selectattr("label","equalto","Better") | list)[0].description }} | {{ (r.levels | selectattr("label","equalto","Best") | list)[0].description }} |
{% endfor %}

## Sign-off
- Trainee: {{ signoff.trainee_name | default("________________") }}  
- Trainer: {{ signoff.trainer_name | default("________________") }}  
- Date: {{ signoff.date | default("____-____-____") }}
```
---

## Generator Implementation

Create Python package `mtlgen/`:

- `__init__.py`
- `cli.py` — argparse CLI: `build`, `validate`, `preview`.
- `loader.py` — load YAML/JSON, validate (jsonschema or Pydantic).
- `render.py` — render Jinja2 to Markdown and HTML.
- `export_docx.py` — Markdown/HTML → DOCX with custom styles.
- `export_pdf.py` — HTML → PDF using chosen engine.
- `assets/` — default CSS for HTML/PDF: headings, shaded callouts (`.critical`, `.warning`, `.tip`), wide tables; page breaks before H1.
- `styles/mtl.docx` — base template (Normal, Heading 1/2/3, Table Normal, Code, Callout).

**Requirements** (`requirements.txt`):
```
jinja2
pyyaml
jsonschema
markdown-it-py
python-docx
weasyprint        # or: pdfkit + wkhtmltopdf (document your choice)
```

**CLI Behavior**
- `build`: validate → render → export all three formats → copy screenshots to `dist/.../assets`.
- `validate`: schema check with helpful errors (point to offending path).
- `preview`: render HTML and open in default browser (optional).

---

## LMS Integration Notes (update `LMS-DEV-SPEC.md`)

**MTL Content Ingestion**
- Storage: commit source YAML to repo; artifacts (`.md`, `.docx`, `.pdf`) stored under `dist/<TaskName>/`.
- LMS displays Markdown for web, links DOCX/PDF for download/print.
- Versioning: `meta.version` + `last_updated` control LMS cache busting.
- Sign-off: LMS can attach an e-sign wrapper or PDF form overlay; file naming `MTL-3_signoff_<task_id>_<date>.pdf`.

**File Naming**
- `MTL-1_<task_id>_<version>.{md,docx,pdf}` etc.

**Accessibility**
- All images require alt text (use `Step ID` as fallback).
- Minimum 12pt in DOCX/PDF; high-contrast callouts.

---

## Tests

Add `tests/test_validation.py`, `tests/test_render.py`, `tests/test_exports.py`:
- Reject invalid date formats, missing CRITICAL confirmations, missing screenshot paths.
- Golden-file compare: render example YAML and compare hash of MD outputs.

---

## Sample Content (seed)

Create `examples/GEN5_Firmware_Flash.yaml` implementing your real procedure:
- Tools: USB A‑B cable, Service Laptop, GEN5, Firmware pkg X.Y.Z.
- Environment: JCM Tool versions, Windows driver notes.
- Steps: include at least 10, mark 3 as **critical**, include 3 screenshots and 2 warnings.
- Confirmations: firmware version check, test ticket feed, status LEDs state.
- Teachback: 6 prompts, rubric with 4 criteria (Connection, Versioning, Recovery, Validation).

Build once to produce a **dist pack** for quick review.

---

## Nice‑to‑Haves
- Front‑matter in Markdown with `meta` block for LMS indexing.
- Optional `--theme` flag to switch CSS (GCG brand colors).
- QR code footer (link to latest MTL‑2) on PDFs.

---

## Commit Plan (examples)
1. `chore(mtlgen): scaffold package and CLI`
2. `feat(schema): add strict MTL schema with confirmations/teachback`
3. `feat(templates): add MTL-1/2/3 jinja templates + partials`
4. `feat(export): add docx/pdf exporters with styles`
5. `test: add validation and render tests`
6. `docs: add README.mtlgen and LMS-DEV-SPEC.md updates`
7. `example: add GEN5_Firmware_Flash sample & built artifacts`

---

## Acceptance Checklist
- [ ] `python -m mtlgen validate examples/GEN5_Firmware_Flash.yaml` passes.
- [ ] `python -m mtlgen build examples/GEN5_Firmware_Flash.yaml` creates 9 files (3×{md,docx,pdf}) + assets.
- [ ] MTL‑2 shows CRITICAL callouts, warnings, tips, and inline screenshots with captions.
- [ ] MTL‑3 renders rubric table correctly and includes sign‑off area.
- [ ] `LMS-DEV-SPEC.md` updated with ingestion + versioning.
- [ ] All dates read as **MM-DD-YY**.
