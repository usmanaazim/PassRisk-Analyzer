"""Educational attack-resistance estimates.

These scores are methodology-based indicators, not an operational cracker.
No live authentication systems are targeted.
"""

from __future__ import annotations

from typing import Any

from security.entropy import theoretical_entropy_bits
from security.feature_extraction import extract_features


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _level(score: float) -> str:
    if score >= 80:
        return "HIGH"
    if score >= 55:
        return "MEDIUM"
    if score >= 30:
        return "LOW"
    return "VERY_LOW"


def analyze_attacks(
    password: str,
    patterns: dict[str, Any],
    dictionary: dict[str, Any],
) -> dict[str, Any]:
    features = extract_features(password)
    entropy_bits = theoretical_entropy_bits(password)
    predictability = patterns.get("predictability_score", 0.0)

    dict_score = 100.0
    if dictionary.get("dictionary_match"):
        dict_score = 8.0
    elif dictionary.get("common_word_detected"):
        dict_score = 28.0
    else:
        dict_score = 100.0 - 70.0 * dictionary.get("similarity_score", 0.0)
    dict_score = _clamp(dict_score)

    pattern_score = _clamp(100.0 * (1.0 - 0.92 * predictability))
    if patterns.get("pattern_detected") and pattern_score > 70:
        pattern_score = 62.0

    transform_count = sum(
        1
        for item in patterns.get("patterns", [])
        if item["type"] in {"leet_substitution", "common_suffix", "year"}
    )
    rule_score = 100.0
    rule_score -= 28.0 * transform_count
    rule_score -= 18.0 if dictionary.get("common_word_detected") else 0.0
    rule_score -= 12.0 * features["length"] / max(features["length"], 1) if features["length"] < 10 else 0
    if dictionary.get("dictionary_match"):
        rule_score = min(rule_score, 15.0)
    rule_score = _clamp(rule_score)

    # Brute-force resistance uses theoretical search space, then discounts predictability
    brute = _clamp(min(100.0, entropy_bits * 1.15))
    brute *= 1.0 - 0.55 * predictability
    if dictionary.get("dictionary_match"):
        brute *= 0.15
    elif dictionary.get("common_word_detected"):
        brute *= 0.45
    brute = _clamp(brute)

    overall = round(0.30 * dict_score + 0.22 * rule_score + 0.22 * pattern_score + 0.26 * brute, 1)

    return {
        "dictionary": round(dict_score, 1),
        "rule_based": round(rule_score, 1),
        "pattern": round(pattern_score, 1),
        "brute_force": round(brute, 1),
        "overall": overall,
        "levels": {
            "dictionary": _level(dict_score),
            "rule_based": _level(rule_score),
            "pattern": _level(pattern_score),
            "brute_force": _level(brute),
        },
        "details": {
            "dictionary_match": dictionary.get("dictionary_match"),
            "predictable_patterns": "HIGH" if predictability >= 0.5 else ("MEDIUM" if predictability >= 0.2 else "LOW"),
            "predictable_transformations": transform_count,
            "estimated_search_space_bits": round(entropy_bits, 2),
        },
        "disclaimer": (
            "Resistance scores are educational estimates based on length, character pool, "
            "dictionary similarity, and pattern heuristics. They assume a local offline "
            "guessing model and do not attack any real system."
        ),
    }
