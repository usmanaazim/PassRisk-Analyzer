from __future__ import annotations

import json
from pathlib import Path


def serialize_report(evaluation: dict) -> None:
    """Keep a human-readable copy beside the JSON metrics."""
    path = Path(__file__).resolve().parent.parent / "models" / "evaluation_summary.txt"
    selected = evaluation["selected"]
    lines = [
        f"Selected model: {evaluation['selected_model']}",
        f"Accuracy: {selected['accuracy']}",
        f"Precision (weighted): {selected['precision_weighted']}",
        f"Recall (weighted): {selected['recall_weighted']}",
        f"F1 (weighted): {selected['f1_weighted']}",
        "",
        "Confusion matrix rows/cols follow STRENGTH_LABELS.",
        str(selected["confusion_matrix"]),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
