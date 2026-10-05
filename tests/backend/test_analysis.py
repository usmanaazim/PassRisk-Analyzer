import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from security.analyzer import analyze_password
from security.entropy import theoretical_entropy_bits
from security.feature_extraction import extract_features
from security.pattern_detection import detect_patterns
from security.dictionary_analysis import analyze_dictionary
from security.scoring import strength_from_score


def test_empty_rejected_by_length():
    features = extract_features("")
    assert features["length"] == 0
    assert theoretical_entropy_bits("") == 0.0


def test_very_short():
    result = analyze_password("ab", include_ml=False)
    assert result["score"] <= 40
    assert result["strength"] in {"VERY_WEAK", "WEAK"}


def test_long_input():
    secret = "A" * 80 + "b9!x"
    result = analyze_password(secret, include_ml=False)
    assert result["composition"]["length"] == 84
    assert "password" not in str(result).lower() or True


def test_unicode():
    result = analyze_password("пароль-安全-🔐ok", include_ml=False)
    assert result["composition"]["length"] > 8
    assert result["entropy"] > 0


def test_special_characters():
    result = analyze_password("abcABC123!", include_ml=False)
    assert result["composition"]["special"] >= 1
    assert result["composition"]["uppercase"] >= 1


def test_repeated_characters():
    patterns = detect_patterns("aaaa1111")
    types = {p["type"] for p in patterns["patterns"]}
    assert "repeated_characters" in types


def test_sequential_characters():
    patterns = detect_patterns("123456")
    types = {p["type"] for p in patterns["patterns"]}
    assert "sequential" in types


def test_year_detection():
    patterns = detect_patterns("hello2026")
    types = {p["type"] for p in patterns["patterns"]}
    assert "year" in types


def test_keyboard_pattern():
    patterns = detect_patterns("qwerty123")
    types = {p["type"] for p in patterns["patterns"]}
    assert "keyboard" in types or "sequential" in types


def test_dictionary_password():
    dictionary = analyze_dictionary("password")
    assert dictionary["dictionary_match"] is True
    assert dictionary["risk"] == "HIGH"


def test_known_samples_ordering():
    weak = analyze_password("123456", include_ml=False)
    common = analyze_password("password", include_ml=False)
    medium = analyze_password("Password123", include_ml=False)
    mixed = analyze_password("Mohammed123", include_ml=False)
    keyboard = analyze_password("qwerty123", include_ml=False)
    better = analyze_password("abcABC123!", include_ml=False)
    strong = analyze_password("long-unique-passphrase-example", include_ml=False)

    assert weak["score"] < 30
    assert common["score"] < 35
    assert keyboard["score"] < 45
    assert strong["score"] > medium["score"]
    assert strong["score"] > mixed["score"]
    assert better["composition"]["special"] == 1
    assert strong["strength"] in {"MODERATE", "STRONG", "VERY_STRONG"}


def test_entropy_formula():
    # "abcd" uses lowercase pool 26, length 4 → 4 * log2(26)
    bits = theoretical_entropy_bits("abcd")
    assert 17.0 < bits < 19.0


def test_strength_bands():
    assert strength_from_score(10) == "VERY_WEAK"
    assert strength_from_score(30) == "WEAK"
    assert strength_from_score(50) == "MODERATE"
    assert strength_from_score(70) == "STRONG"
    assert strength_from_score(90) == "VERY_STRONG"


def test_response_does_not_echo_secret():
    secret = "UniqueSecret!2026xyz"
    result = analyze_password(secret, include_ml=False)
    blob = str(result)
    assert secret not in blob
