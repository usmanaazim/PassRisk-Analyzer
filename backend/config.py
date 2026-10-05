"""Application configuration. No secrets are required for local academic use."""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "5001"))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://127.0.0.1:5173,http://localhost:5173",
    ).split(",")
    if origin.strip()
]

MAX_PASSWORD_LENGTH = int(os.environ.get("MAX_PASSWORD_LENGTH", "256"))
MIN_PASSWORD_LENGTH = 1

MODEL_PATH = MODELS_DIR / "password_strength_model.pkl"
FEATURE_METADATA_PATH = MODELS_DIR / "feature_metadata.json"
EVALUATION_PATH = MODELS_DIR / "evaluation.json"

STRENGTH_LABELS = [
    "VERY_WEAK",
    "WEAK",
    "MODERATE",
    "STRONG",
    "VERY_STRONG",
]

SCORE_BANDS = [
    (20, "VERY_WEAK"),
    (40, "WEAK"),
    (60, "MODERATE"),
    (80, "STRONG"),
    (100, "VERY_STRONG"),
]
