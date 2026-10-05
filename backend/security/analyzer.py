"""Full analysis pipeline. The password argument is never persisted."""

from __future__ import annotations

from typing import Any

from security.attack_analysis import analyze_attacks
from security.dictionary_analysis import analyze_dictionary
from security.entropy import analyze_entropy
from security.feature_extraction import extract_features
from security.improvement import simulate_improvements
from security.pattern_detection import detect_patterns
from security.recommendations import build_recommendations
from security.scoring import compute_score


FEATURE_NAMES = [
    "length",
    "uppercase_count",
    "lowercase_count",
    "digit_count",
    "special_count",
    "unique_character_count",
    "character_diversity",
    "entropy",
    "dictionary_match",
    "dictionary_similarity",
    "repeated_character_score",
    "sequence_score",
    "keyboard_pattern_score",
    "year_pattern",
    "common_word_score",
    "predictability_score",
]


def feature_vector(password: str) -> dict[str, float]:
    features = extract_features(password)
    patterns = detect_patterns(password)
    dictionary = analyze_dictionary(password)
    entropy = analyze_entropy(password)
    scores = patterns["scores"]
    return {
        "length": float(features["length"]),
        "uppercase_count": float(features["uppercase_count"]),
        "lowercase_count": float(features["lowercase_count"]),
        "digit_count": float(features["digit_count"]),
        "special_count": float(features["special_count"]),
        "unique_character_count": float(features["unique_character_count"]),
        "character_diversity": float(features["character_diversity"]),
        "entropy": float(entropy["theoretical_bits"]),
        "dictionary_match": 1.0 if dictionary["dictionary_match"] else 0.0,
        "dictionary_similarity": float(dictionary["similarity_score"]),
        "repeated_character_score": float(scores["repeated_character_score"]),
        "sequence_score": float(scores["sequence_score"]),
        "keyboard_pattern_score": float(scores["keyboard_pattern_score"]),
        "year_pattern": float(scores["year_pattern"]),
        "common_word_score": float(dictionary["common_word_score"]),
        "predictability_score": float(patterns["predictability_score"]),
    }


def analyze_password(password: str, include_ml: bool = True) -> dict[str, Any]:
    features = extract_features(password)
    patterns = detect_patterns(password)
    dictionary = analyze_dictionary(password)
    entropy = analyze_entropy(password)
    attacks = analyze_attacks(password, patterns, dictionary)
    scored = compute_score(password, features, patterns, dictionary, attacks)
    recommendations = build_recommendations(password, features, patterns, dictionary, scored["score"])
    improvements = simulate_improvements(scored["score"], features, patterns, dictionary)

    result: dict[str, Any] = {
        "score": scored["score"],
        "strength": scored["strength"],
        "risk_level": scored["risk_level"],
        "score_note": scored["note"],
        "entropy": entropy["theoretical_bits"],
        "entropy_analysis": entropy,
        "composition": features["composition"],
        "features": feature_vector(password),
        "radar": scored["components"],
        "attack_resistance": {
            "dictionary": attacks["dictionary"],
            "rule_based": attacks["rule_based"],
            "pattern": attacks["pattern"],
            "brute_force": attacks["brute_force"],
            "overall": attacks["overall"],
            "levels": attacks["levels"],
            "details": attacks["details"],
            "disclaimer": attacks["disclaimer"],
        },
        "patterns": patterns["patterns"],
        "pattern_detected": patterns["pattern_detected"],
        "dictionary": {
            "dictionary_match": dictionary["dictionary_match"],
            "similarity_score": dictionary["similarity_score"],
            "risk": dictionary["risk"],
            "common_word_detected": dictionary["common_word_detected"],
        },
        "recommendations": recommendations,
        "improvement_path": improvements,
    }

    if include_ml:
        from ml.predict import predict_strength

        result["ml"] = predict_strength(password, fallback_label=scored["strength"])
        result["ml_prediction"] = result["ml"]["label"]
        result["ml_confidence"] = result["ml"]["confidence"]

    result["zxcvbn_benchmark"] = _zxcvbn_benchmark(password)
    return result


def _zxcvbn_benchmark(password: str) -> dict:
    try:
        from zxcvbn import zxcvbn
    except ImportError:
        return {"available": False}
    raw = zxcvbn(password)
    return {
        "available": True,
        "score": int(raw.get("score", 0)),
        "guesses_log10": float(raw.get("guesses_log10", 0) or 0),
        "note": "zxcvbn is a reference estimator only. PasswordGuard uses its own features and model.",
    }
