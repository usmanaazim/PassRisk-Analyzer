"""Composite security score. This is an analytical estimate, not a proof of safety."""

from __future__ import annotations

from typing import Any

from config import SCORE_BANDS
from security.entropy import theoretical_entropy_bits


def strength_from_score(score: int) -> str:
    for upper, label in SCORE_BANDS:
        if score <= upper:
            return label
    return "VERY_STRONG"


def risk_from_score(score: int) -> str:
    if score <= 20:
        return "CRITICAL"
    if score <= 40:
        return "HIGH"
    if score <= 60:
        return "MEDIUM"
    if score <= 80:
        return "LOW"
    return "VERY_LOW"


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def component_scores(
    password: str,
    features: dict[str, Any],
    patterns: dict[str, Any],
    dictionary: dict[str, Any],
    attacks: dict[str, Any],
) -> dict[str, float]:
    length = features["length"]
    if length >= 20:
        length_score = 100.0
    elif length >= 16:
        length_score = 90.0
    elif length >= 12:
        length_score = 75.0
    elif length >= 10:
        length_score = 58.0
    elif length >= 8:
        length_score = 40.0
    else:
        length_score = max(8.0, length * 5.0)

    complexity = min(
        100.0,
        features["character_classes"] * 22.0 + 12.0 * min(features["special_count"], 3),
    )
    if length >= 20:
        complexity = max(complexity, 78.0)
    if length >= 24:
        complexity = max(complexity, 88.0)

    uniqueness = min(
        100.0,
        features["character_diversity"] * 85.0 + min(features["unique_character_count"], 16) * 1.2,
    )

    if dictionary.get("dictionary_match"):
        dictionary_resistance = 6.0
    elif dictionary.get("common_word_detected"):
        dictionary_resistance = 32.0
    else:
        dictionary_resistance = 100.0 - 80.0 * dictionary.get("similarity_score", 0.0)

    pattern_resistance = 100.0 * (1.0 - patterns.get("predictability_score", 0.0))
    predictability = 100.0 * (1.0 - patterns.get("predictability_score", 0.0) * 0.85)
    attack_resistance = attacks.get("overall", 50.0)

    entropy_bits = theoretical_entropy_bits(password)
    entropy_score = min(100.0, entropy_bits * 1.25)
    if dictionary.get("dictionary_match"):
        entropy_score *= 0.25
    elif dictionary.get("common_word_detected"):
        entropy_score *= 0.55
    entropy_score *= 1.0 - 0.35 * patterns.get("predictability_score", 0.0)

    return {
        "length": round(_clamp(length_score), 1),
        "complexity": round(_clamp(complexity), 1),
        "entropy": round(_clamp(entropy_score), 1),
        "uniqueness": round(_clamp(uniqueness), 1),
        "dictionary_resistance": round(_clamp(dictionary_resistance), 1),
        "pattern_resistance": round(_clamp(pattern_resistance), 1),
        "predictability": round(_clamp(predictability), 1),
        "attack_resistance": round(_clamp(attack_resistance), 1),
    }


def compute_score(
    password: str,
    features: dict[str, Any],
    patterns: dict[str, Any],
    dictionary: dict[str, Any],
    attacks: dict[str, Any],
) -> dict[str, Any]:
    components = component_scores(password, features, patterns, dictionary, attacks)
    weighted = (
        0.16 * components["length"]
        + 0.12 * components["complexity"]
        + 0.16 * components["entropy"]
        + 0.10 * components["uniqueness"]
        + 0.16 * components["dictionary_resistance"]
        + 0.12 * components["pattern_resistance"]
        + 0.08 * components["predictability"]
        + 0.10 * components["attack_resistance"]
    )
    if features["length"] < 6:
        weighted = min(weighted, 18 + features["length"] * 3)
    if dictionary.get("dictionary_match"):
        weighted = min(weighted, 28)
    if features["length"] < 8 and patterns.get("predictability_score", 0) >= 0.2:
        weighted = min(weighted, 32)
    score = int(round(_clamp(weighted)))
    return {
        "score": score,
        "strength": strength_from_score(score),
        "risk_level": risk_from_score(score),
        "components": components,
        "note": (
            "Security score is an analytical estimate based on multiple password "
            "characteristics and attack-resistance indicators."
        ),
    }
