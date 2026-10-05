from flask import Blueprint, jsonify, request

from config import MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH
from security.analyzer import analyze_password

analysis_bp = Blueprint("analysis", __name__)


def _extract_password(payload: dict, field: str = "password") -> tuple[str | None, tuple | None]:
    if not isinstance(payload, dict):
        return None, ({"error": "Invalid JSON body."}, 400)
    if field not in payload:
        return None, ({"error": f"Missing field: {field}"}, 400)
    value = payload[field]
    if not isinstance(value, str):
        return None, ({"error": f"{field} must be a string."}, 400)
    if len(value) < MIN_PASSWORD_LENGTH:
        return None, ({"error": "Password must not be empty."}, 400)
    if len(value) > MAX_PASSWORD_LENGTH:
        return None, (
            {"error": f"Password exceeds maximum length of {MAX_PASSWORD_LENGTH} characters."},
            400,
        )
    return value, None


@analysis_bp.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    password, error = _extract_password(payload)
    if error:
        body, status = error
        return jsonify(body), status
    try:
        result = analyze_password(password)
    except FileNotFoundError:
        return jsonify({"error": "Model or dataset files are unavailable."}), 503
    except Exception:
        return jsonify({"error": "Analysis failed. Please try again."}), 500
    finally:
        password = None  # drop local reference promptly
    return jsonify(result)


@analysis_bp.post("/compare")
def compare():
    payload = request.get_json(silent=True) or {}
    a, error_a = _extract_password(payload, "password_a")
    if error_a:
        body, status = error_a
        return jsonify(body), status
    b, error_b = _extract_password(payload, "password_b")
    if error_b:
        body, status = error_b
        return jsonify(body), status
    try:
        left = analyze_password(a)
        right = analyze_password(b)
        summary = {
            "a": {
                "score": left["score"],
                "strength": left["strength"],
                "length": left["composition"]["length"],
                "entropy": left["entropy"],
                "dictionary_risk": left["dictionary"]["risk"],
                "pattern_risk": left["attack_resistance"]["levels"]["pattern"],
                "attack_resistance": left["attack_resistance"]["overall"],
                "ml_prediction": left.get("ml_prediction"),
            },
            "b": {
                "score": right["score"],
                "strength": right["strength"],
                "length": right["composition"]["length"],
                "entropy": right["entropy"],
                "dictionary_risk": right["dictionary"]["risk"],
                "pattern_risk": right["attack_resistance"]["levels"]["pattern"],
                "attack_resistance": right["attack_resistance"]["overall"],
                "ml_prediction": right.get("ml_prediction"),
            },
        }
        return jsonify(summary)
    except Exception:
        return jsonify({"error": "Comparison failed. Please try again."}), 500
    finally:
        a = None
        b = None
