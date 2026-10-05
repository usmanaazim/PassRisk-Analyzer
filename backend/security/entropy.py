"""Theoretical entropy and search-space estimates.

H = L * log2(R) is an upper-bound model of a uniformly random password.
Human-chosen passwords are far more predictable, so this value is a
reference — not a guarantee of real-world strength.
"""

from __future__ import annotations

import math

from security.feature_extraction import character_pool_size, shannon_entropy


# Conservative educational assumption for offline guessing illustrations.
GUESSES_PER_SECOND = 1_000_000_000  # 1e9, GPU-class offline hash guessing (illustrative)


def theoretical_entropy_bits(password: str) -> float:
    length = len(password)
    pool = character_pool_size(password)
    if length == 0:
        return 0.0
    return length * math.log2(pool)


def search_space(password: str) -> float:
    length = len(password)
    pool = character_pool_size(password)
    return float(pool ** length) if length else 0.0


def estimated_crack_seconds(password: str, guesses_per_second: int = GUESSES_PER_SECOND) -> float:
    space = search_space(password)
    if space <= 0 or guesses_per_second <= 0:
        return 0.0
    # Average-case: half the search space
    return (space / 2.0) / guesses_per_second


def humanize_duration(seconds: float) -> str:
    if seconds < 1:
        return "less than 1 second"
    units = [
        (60, "seconds"),
        (60, "minutes"),
        (24, "hours"),
        (365, "days"),
        (100, "years"),
        (10, "centuries"),
    ]
    value = seconds
    label = "seconds"
    for divisor, next_label in units:
        if value < divisor:
            break
        value /= divisor
        label = next_label
    if value >= 1e6:
        return "astronomically long (theoretical)"
    if value >= 1000:
        return f"about {value:,.0f} {label}"
    return f"about {value:.1f} {label}"


def analyze_entropy(password: str) -> dict:
    bits = theoretical_entropy_bits(password)
    shannon = shannon_entropy(password)
    space = search_space(password)
    seconds = estimated_crack_seconds(password)
    return {
        "theoretical_bits": round(bits, 2),
        "shannon_bits": round(shannon, 2),
        "character_pool": character_pool_size(password),
        "search_space_log10": round(math.log10(space), 2) if space > 0 else 0.0,
        "estimated_offline_crack_time": humanize_duration(seconds),
        "assumption_guesses_per_second": GUESSES_PER_SECOND,
        "caveat": (
            "Theoretical entropy assumes uniformly random characters from the "
            "detected pool. Human-chosen passwords are typically much weaker."
        ),
    }
