"""Local dictionary analysis using a small educational word list.

This module does not load leaked credential dumps. The bundled list is a
synthetic subset of well-known trivial passwords used in textbooks.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sample" / "common_passwords.txt"

_CACHE: set[str] | None = None


def _load_dictionary() -> set[str]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    words: set[str] = set()
    if DATA_FILE.exists():
        for line in DATA_FILE.read_text(encoding="utf-8").splitlines():
            item = line.strip().lower()
            if item and not item.startswith("#"):
                words.add(item)
    _CACHE = words
    return words


def _normalize(password: str) -> str:
    return password.lower()


def _deleet(password: str) -> str:
    table = str.maketrans({"@": "a", "4": "a", "0": "o", "1": "i", "$": "s", "5": "s", "3": "e", "7": "t"})
    return password.lower().translate(table)


def _ngram_similarity(a: str, b: str, n: int = 3) -> float:
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if len(a) < n or len(b) < n:
        return 1.0 if a in b or b in a else 0.0

    def grams(text: str) -> set[str]:
        return {text[i : i + n] for i in range(len(text) - n + 1)}

    ga, gb = grams(a), grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def analyze_dictionary(password: str) -> dict[str, Any]:
    dictionary = _load_dictionary()
    lower = _normalize(password)
    deleet = _deleet(password)

    exact = lower in dictionary or deleet in dictionary
    contained_word = None
    tokens = re.split(r"[^a-z0-9]+", lower) + re.split(r"[^a-z0-9]+", deleet)
    alnum = re.sub(r"[^a-z0-9]", "", lower)
    for word in dictionary:
        if len(word) < 4:
            continue
        in_tokens = word in tokens
        if not in_tokens:
            continue
        coverage = len(word) / max(len(alnum), 1)
        if exact or coverage >= 0.5 or (in_tokens and len(alnum) <= 14 and coverage >= 0.35):
            contained_word = word
            break

    best = 1.0 if exact else 0.0
    if not exact:
        sample = list(dictionary)[:120]
        for word in sample:
            best = max(best, _ngram_similarity(lower, word), _ngram_similarity(deleet, word))
            if best >= 0.85:
                break

    if contained_word and not exact:
        best = max(best, 0.72)

    if exact:
        risk = "HIGH"
    elif best >= 0.55 or contained_word:
        risk = "MEDIUM"
    elif best >= 0.25:
        risk = "LOW"
    else:
        risk = "VERY_LOW"

    return {
        "dictionary_match": bool(exact),
        "common_word_detected": bool(contained_word),
        "matched_token": None if not contained_word else "common-word",
        "similarity_score": round(min(1.0, best), 4),
        "risk": risk,
        "common_word_score": 1.0 if exact else (0.7 if contained_word else round(best, 4)),
    }


def entropy_adjusted_for_dictionary(theoretical_bits: float, dictionary: dict[str, Any]) -> float:
    """Reduce theoretical entropy when the password is dictionary-like."""
    penalty = 0.0
    if dictionary["dictionary_match"]:
        penalty = 0.75
    elif dictionary["common_word_detected"]:
        penalty = 0.45
    else:
        penalty = 0.25 * dictionary["similarity_score"]
    return max(0.0, theoretical_bits * (1.0 - penalty))


def log2_safe(value: float) -> float:
    if value <= 0:
        return 0.0
    return math.log2(value)
