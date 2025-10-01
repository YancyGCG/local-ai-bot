"""Quiz generation utilities derived from MTL task data."""

from __future__ import annotations

from typing import Any, Dict, List


def build_quiz_payload(task_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Derive quiz prompts from teachback and confirmation data."""

    quiz_items: List[Dict[str, Any]] = []
    teachback = task_data.get("teachback", {})

    for idx, prompt in enumerate(teachback.get("prompts", []), start=1):
        quiz_items.append(
            {
                "id": f"teachback-{idx}",
                "type": "open",
                "question": prompt,
            }
        )

    for step in task_data.get("steps", [])[:5]:
        confirmation = step.get("confirm")
        if confirmation:
            quiz_items.append(
                {
                    "id": f"confirm-{step.get('id', len(quiz_items))}",
                    "type": "short-answer",
                    "question": f"What confirms completion of step '{step.get('id', 'Step')}?'",
                    "answer": confirmation,
                }
            )

    confirmations = task_data.get("confirmations", [])[:3]
    for idx, item in enumerate(confirmations, start=1):
        quiz_items.append(
            {
                "id": f"final-{idx}",
                "type": "short-answer",
                "question": f"List acceptable outcomes for {item.get('item', 'this task')}.",
                "answer": "; ".join(item.get("accept", [])),
            }
        )

    return quiz_items
