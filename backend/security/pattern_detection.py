"""Educational pattern detection for common human password habits."""

from __future__ import annotations

import re
from typing import Any

KEYBOARD_ROWS = [
    "1234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "!@#$%^&*()",
]

COMMON_SUFFIXES = (
    "123",
    "1234",
    "12345",
    "1",
    "12",
    "!",
    "!!",
    "@123",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024",
    "2025",
    "2026",
)

LEET_MAP = str.maketrans(
    {
        "@": "a",
        "4": "a",
        "0": "o",
        "1": "i",
        "!": "i",
        "$": "s",
        "5": "s",
        "3": "e",
        "7": "t",
        "+": "t",
    }
)


def _normalize(password: str) -> str:
    return password.lower()


def _has_sequence(text: str, alphabet: str, min_len: int = 4) -> bool:
    if len(text) < min_len:
        return False
    forward = alphabet
    backward = alphabet[::-1]
    for source in (forward, backward):
        for i in range(len(source) - min_len + 1):
            chunk = source[i : i + min_len]
            if chunk in text:
                return True
    return False


def detect_sequential(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lower = _normalize(password)
    if _has_sequence(lower, "abcdefghijklmnopqrstuvwxyz") or _has_sequence(lower, "0123456789"):
        findings.append(
            {
                "type": "sequential",
                "severity": "high",
                "description": "Contains sequential characters (letters or digits).",
            }
        )
    return findings


def detect_repeated_characters(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if re.search(r"(.)\1{2,}", password):
        findings.append(
            {
                "type": "repeated_characters",
                "severity": "medium",
                "description": "Contains three or more repeated characters in a row.",
            }
        )
    return findings


def detect_repeated_substrings(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lower = _normalize(password)
    if re.search(r"(.{3,})\1", lower):
        findings.append(
            {
                "type": "repeated_substring",
                "severity": "medium",
                "description": "Contains a repeated substring (for example abcabc).",
            }
        )
    return findings


def detect_keyboard_patterns(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lower = _normalize(password)
    for row in KEYBOARD_ROWS:
        if _has_sequence(lower, row, min_len=4) or _has_sequence(lower, row, min_len=5):
            findings.append(
                {
                    "type": "keyboard",
                    "severity": "high",
                    "description": "Contains a keyboard-walk sequence such as qwerty or asdf.",
                }
            )
            break
    return findings


def detect_years(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if re.search(r"(19[5-9]\d|20[0-3]\d)", password):
        findings.append(
            {
                "type": "year",
                "severity": "medium",
                "description": "Contains a four-digit year, which is a common predictable suffix.",
            }
        )
    return findings


def detect_common_suffixes(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lower = _normalize(password)
    for suffix in COMMON_SUFFIXES:
        if lower.endswith(suffix) and len(lower) > len(suffix):
            findings.append(
                {
                    "type": "common_suffix",
                    "severity": "medium",
                    "description": f"Ends with a common suffix pattern ({suffix}).",
                }
            )
            break
    return findings


def detect_leet_substitutions(password: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if any(ch in password for ch in "@0$!"):
        findings.append(
            {
                "type": "leet_substitution",
                "severity": "low",
                "description": (
                    "Contains common substitutions (a→@, o→0, i→1, s→$). "
                    "Attackers routinely try these transformations."
                ),
            }
        )
    return findings


def pattern_scores(password: str, findings: list[dict[str, Any]]) -> dict[str, float]:
    types = {item["type"] for item in findings}
    repeated_run = 0.0
    if password:
        longest = 1
        current = 1
        for i in range(1, len(password)):
            if password[i] == password[i - 1]:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        repeated_run = min(1.0, (longest - 1) / 4.0)

    return {
        "repeated_character_score": round(repeated_run, 4),
        "sequence_score": 1.0 if "sequential" in types else 0.0,
        "keyboard_pattern_score": 1.0 if "keyboard" in types else 0.0,
        "year_pattern": 1.0 if "year" in types else 0.0,
        "common_suffix_score": 1.0 if "common_suffix" in types else 0.0,
        "leet_score": 1.0 if "leet_substitution" in types else 0.0,
        "repeated_substring_score": 1.0 if "repeated_substring" in types else 0.0,
    }


def detect_patterns(password: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    findings.extend(detect_sequential(password))
    findings.extend(detect_repeated_characters(password))
    findings.extend(detect_repeated_substrings(password))
    findings.extend(detect_keyboard_patterns(password))
    findings.extend(detect_years(password))
    findings.extend(detect_common_suffixes(password))
    findings.extend(detect_leet_substitutions(password))
    scores = pattern_scores(password, findings)
    return {
        "pattern_detected": bool(findings),
        "patterns": findings,
        "scores": scores,
        "predictability_score": round(
            min(
                1.0,
                0.25 * scores["sequence_score"]
                + 0.25 * scores["keyboard_pattern_score"]
                + 0.15 * scores["year_pattern"]
                + 0.15 * scores["repeated_character_score"]
                + 0.10 * scores["common_suffix_score"]
                + 0.10 * scores["repeated_substring_score"],
            ),
            4,
        ),
    }
