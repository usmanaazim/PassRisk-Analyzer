from flask import Blueprint, jsonify

from ml.predict import load_evaluation, load_metadata, load_model

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    model = load_model()
    return jsonify(
        {
            "status": "ok",
            "service": "password-security-analyzer",
            "model_loaded": model is not None,
        }
    )


@health_bp.get("/model-info")
def model_info():
    return jsonify(load_metadata())


@health_bp.get("/metrics")
def metrics():
    evaluation = load_evaluation()
    if not evaluation.get("available"):
        return jsonify({"error": "Model evaluation is not available. Train the model first."}), 503
    return jsonify(evaluation)
