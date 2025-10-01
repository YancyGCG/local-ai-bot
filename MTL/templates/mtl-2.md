# {{ meta.title }} — MTL-2 (Detailed Walkthrough)

> **CRITICAL steps are flagged.** Complete confirmations after each major action.

## Environment

- Models: {{ environment.models | default([]) | join(", ") }}
- Software Versions: {{ environment.sw_versions | default([]) | join(", ") }}
- Connections: {{ environment.connections | default([]) | join(", ") }}

## Tools Required

{% for t in tools_required %}- **{{ t.name }}**{% if t.qty %} ({{ t.qty }}){% endif %}{% if t.notes %} — {{ t.notes }}{% endif %}
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
