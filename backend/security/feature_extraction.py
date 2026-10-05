"""Character-level feature extraction. Passwords stay in memory only."""

from __future__ import annotations

import math
import string
from typing import Any


LOWER = set(string.ascii_lowercase)
UPPER = set(string.ascii_uppercase)
DIGITS = set(string.digits)
# Common printable specials used in password policies
SPECIALS = set("!@#$%^&*()_+-=[]{}|;:',.<>/?`~\"\\")


def _counts(password: str) -> dict[str, int]:
    lower = upper = digits = special = other = 0
    for ch in password:
        if ch in LOWER:
            lower += 1
        elif ch in UPPER:
            upper += 1
        elif ch in DIGITS:
            digits += 1
        elif ch in SPECIALS or (not ch.isalnum() and not ch.isspace()):
            special += 1
        else:
            other += 1
    return {
        "lowercase": lower,
        "uppercase": upper,
        "digits": digits,
        "special": special,
        "other": other,
    }


def character_pool_size(password: str) -> int:
    """Estimate the character alphabet actually used (R in H = L * log2(R))."""
    pool = 0
    counts = _counts(password)
    if counts["lowercase"]:
        pool += 26
    if counts["uppercase"]:
        pool += 26
    if counts["digits"]:
        pool += 10
    if counts["special"]:
        pool += 33
    if counts["other"]:
        # Unicode / space / uncommon symbols expand the theoretical pool
        unique_other = len({ch for ch in password if ch not in LOWER | UPPER | DIGITS | SPECIALS})
        pool += max(unique_other, 50)
    return max(pool, 1)


def shannon_entropy(password: str) -> float:
    if not password:
        return 0.0
    freq: dict[str, int] = {}
    for ch in password:
        freq[ch] = freq.get(ch, 0) + 1
    length = len(password)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy * length


def extract_features(password: str) -> dict[str, Any]:
    counts = _counts(password)
    length = len(password)
    unique = len(set(password))
    diversity = (unique / length) if length else 0.0
    classes = sum(
        1
        for key in ("lowercase", "uppercase", "digits", "special")
        if counts[key] > 0
    )
    return {
        "length": length,
        "uppercase_count": counts["uppercase"],
        "lowercase_count": counts["lowercase"],
        "digit_count": counts["digits"],
        "special_count": counts["special"],
        "other_count": counts["other"],
        "unique_character_count": unique,
        "character_diversity": round(diversity, 4),
        "character_classes": classes,
        "character_pool": character_pool_size(password),
        "composition": {
            "length": length,
            "uppercase": counts["uppercase"],
            "lowercase": counts["lowercase"],
            "digits": counts["digits"],
            "special": counts["special"],
            "unique": unique,
        },
    }
