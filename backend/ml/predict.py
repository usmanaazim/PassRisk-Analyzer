from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

import joblib
import numpy as np

from config import EVALUATION_PATH, FEATURE_METADATA_PATH, MODEL_PATH, STRENGTH_LABELS
from ml.preprocessing import FEATURE_NAMES, vector_to_array
from security.analyzer import feature_vector


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_metadata() -> dict[str, Any]:
    if not FEATURE_METADATA_PATH.exists():
        return {
            "model_name": "untrained",
            "feature_names": FEATURE_NAMES,
            "labels": STRENGTH_LABELS,
            "feature_importance": [],
        }
    return json.loads(FEATURE_METADATA_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_evaluation() -> dict[str, Any]:
    if not EVALUATION_PATH.exists():
        return {"available": False}
    data = json.loads(EVALUATION_PATH.read_text(encoding="utf-8"))
    data["available"] = True
    return data


def predict_strength(password: str, fallback_label: str) -> dict[str, Any]:
    model = load_model()
    metadata = load_metadata()
    labels = metadata.get("labels", STRENGTH_LABELS)
    vector = feature_vector(password)
    array = vector_to_array(vector)

    if model is None:
        probabilities = {label: 0.0 for label in labels}
        probabilities[fallback_label] = 1.0
        return {
            "label": fallback_label,
            "confidence": 1.0,
            "probabilities": probabilities,
            "model_name": "heuristic_fallback",
            "available": False,
            "feature_importance": metadata.get("feature_importance", []),
        }

    proba = None
    if hasattr(model, "predict_proba"):
        raw = model.predict_proba(array)[0]
        class_labels = list(model.classes_)
        probabilities = {label: 0.0 for label in labels}
        for cls, value in zip(class_labels, raw):
            probabilities[str(cls)] = round(float(value), 4)
        label = str(class_labels[int(np.argmax(raw))])
        confidence = round(float(np.max(raw)), 4)
    else:
        label = str(model.predict(array)[0])
        probabilities = {item: 0.0 for item in labels}
        probabilities[label] = 1.0
        confidence = 1.0

    return {
        "label": label,
        "confidence": confidence,
        "probabilities": probabilities,
        "model_name": metadata.get("model_name", "random_forest"),
        "available": True,
        "feature_importance": metadata.get("feature_importance", []),
    }
