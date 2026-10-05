"""Dynamic recommendations based on detected weaknesses."""

from __future__ import annotations

from typing import Any


def build_recommendations(
    password: str,
    features: dict[str, Any],
    patterns: dict[str, Any],
    dictionary: dict[str, Any],
    score: int,
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    types = {p["type"] for p in patterns.get("patterns", [])}

    if features["length"] < 12:
        items.append(
            {
                "severity": "high",
                "title": "Increase password length",
                "detail": "Use at least 12–16 characters. Longer secrets expand the search space.",
            }
        )
    elif features["length"] < 16:
        items.append(
            {
                "severity": "medium",
                "title": "Consider a longer passphrase",
                "detail": "Passphrases of 16+ characters generally resist brute-force estimates better.",
            }
        )
    else:
        items.append(
            {
                "severity": "ok",
                "title": "Good password length",
                "detail": "Length is in a healthier range for search-space resistance.",
            }
        )

    if features["character_classes"] < 3:
        items.append(
            {
                "severity": "high",
                "title": "Increase character diversity",
                "detail": "Mix lowercase, uppercase, digits, and special characters.",
            }
        )
    else:
        items.append(
            {
                "severity": "ok",
                "title": "Good character diversity",
                "detail": "Multiple character classes were detected.",
            }
        )

    if dictionary.get("dictionary_match") or dictionary.get("common_word_detected"):
        items.append(
            {
                "severity": "high",
                "title": "Avoid common dictionary words",
                "detail": "Standalone common words and famous trivial passwords are guessed first.",
            }
        )

    if "year" in types:
        items.append(
            {
                "severity": "medium",
                "title": "Avoid predictable years",
                "detail": "Birth years and the current year are common rule-based suffixes.",
            }
        )
    if "keyboard" in types:
        items.append(
            {
                "severity": "high",
                "title": "Avoid keyboard sequences",
                "detail": "Sequences such as qwerty or asdfgh are included in most wordlists.",
            }
        )
    if "sequential" in types:
        items.append(
            {
                "severity": "high",
                "title": "Avoid sequential characters",
                "detail": "Patterns like 123456 or abcdef are extremely predictable.",
            }
        )
    if "repeated_characters" in types or "repeated_substring" in types:
        items.append(
            {
                "severity": "medium",
                "title": "Avoid repeated-character patterns",
                "detail": "Runs such as aaaa or repeated blocks reduce uniqueness.",
            }
        )
    if "leet_substitution" in types:
        items.append(
            {
                "severity": "low",
                "title": "Do not rely on leetspeak",
                "detail": "Substitutions such as a→@ or o→0 are applied automatically in rule attacks.",
            }
        )
    if "common_suffix" in types:
        items.append(
            {
                "severity": "medium",
                "title": "Avoid common numeric suffixes",
                "detail": "Appending 123 or a year is a well-known mangling rule.",
            }
        )

    if score >= 81 and not any(i["severity"] in {"high", "medium"} for i in items):
        items.append(
            {
                "severity": "ok",
                "title": "No major weaknesses detected",
                "detail": "Continue using unique passwords for each account and a reputable password manager.",
            }
        )

    if features["character_diversity"] < 0.55 and features["length"] >= 8:
        items.append(
            {
                "severity": "medium",
                "title": "Increase uniqueness",
                "detail": "Reuse of the same characters shrinks the effective alphabet.",
            }
        )

    return items
