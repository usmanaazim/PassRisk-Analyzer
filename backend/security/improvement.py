"""Estimate how score could improve without generating a real password."""

from __future__ import annotations

from typing import Any


def simulate_improvements(current_score: int, features: dict[str, Any], patterns: dict[str, Any], dictionary: dict[str, Any]) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = [{"label": "Current score", "score": current_score, "change": None}]
    score = current_score
    types = {p["type"] for p in patterns.get("patterns", [])}

    def add(label: str, delta: int) -> None:
        nonlocal score
        score = min(100, score + delta)
        steps.append({"label": label, "score": score, "change": delta})

    if features["length"] < 12:
        add("Increase length to 12+", max(8, 12 - features["length"]) * 2)
    if features["character_classes"] < 3:
        add("Add missing character classes", 10)
    if "year" in types:
        add("Remove predictable year", 8)
    if "keyboard" in types or "sequential" in types:
        add("Remove sequential / keyboard patterns", 12)
    if dictionary.get("dictionary_match") or dictionary.get("common_word_detected"):
        add("Replace common dictionary words", 14)
    if features["character_diversity"] < 0.7:
        add("Increase uniqueness", 7)
    if "leet_substitution" in types or "common_suffix" in types:
        add("Avoid suffixes and leetspeak", 6)
    if len(steps) == 1:
        add("Maintain unique per-account secrets", 2)
    return steps
