# {{ meta.title }} — MTL-3 (Teachback & Sign-off)

## Teachback Prompts

{% for p in teachback.prompts %}- {{ p }}
{% endfor %}

## Rubric (Needs Work → Best)

| Criterion | Needs Work | Good | Better | Best |
|---|---|---|---|---|
{% for r in teachback.rubric %}
| {{ r.criterion }} | {{ r.levels_map['Needs Work'] }} | {{ r.levels_map['Good'] }} | {{ r.levels_map['Better'] }} | {{ r.levels_map['Best'] }} |

{% endfor %}

## Sign-off

- Trainee: {{ signoff.trainee_name | default("________________") }}  
- Trainer: {{ signoff.trainer_name | default("________________") }}  
- Date: {{ signoff.date | default("____-____-____") }}
