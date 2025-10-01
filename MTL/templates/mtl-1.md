# {{ meta.title }} — MTL-1 (At-a-Glance)

**Task ID:** {{ meta.task_id }}  
**Version:** {{ meta.version }} • **Owner:** {{ meta.owner }} • **Updated:** {{ meta.last_updated }}  
**Difficulty:** {{ meta.difficulty }} • **Est. Time:** {{ meta.estimated_time_min }} min  
**Tags:** {{ meta.tags | join(", ") }}

## Purpose
Brief: why this matters and when to run it.

## Tools Required
{% for t in tools_required %}- **{{ t.name }}**{% if t.qty %} ({{ t.qty }}){% endif %}{% if t.notes %} — {{ t.notes }}{% endif %}
{% endfor %}

## Prerequisites
{% for p in prerequisites %}- {{ p }}
{% endfor %}

## Success Criteria (Confirmations)
{% for c in confirmations %}- **{{ c.item }}** → Accept: {{ c.accept | join("; ") }}
{% endfor %}
