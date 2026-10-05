"""Train Logistic Regression, Decision Tree, and Random Forest on synthetic data."""

from __future__ import annotations

import json
import random
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from config import EVALUATION_PATH, FEATURE_METADATA_PATH, MODELS_DIR, MODEL_PATH, STRENGTH_LABELS
from ml.evaluation import serialize_report
from ml.preprocessing import FEATURE_NAMES, dataframe_from_passwords
from security.analyzer import analyze_password

rng = random.Random(42)
COMMON = [
    "password",
    "123456",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
    "abc123",
    "monkey",
    "dragon",
]


def _weak() -> str:
    choice = rng.choice(["dict", "seq", "key", "short"])
    if choice == "dict":
        return rng.choice(COMMON) + rng.choice(["", "1", "123", "2024", "2026"])
    if choice == "seq":
        return rng.choice(["123456", "abcdef", "654321", "111111", "aaaaaa"])
    if choice == "key":
        return rng.choice(["qwerty", "asdfgh", "zxcvbn", "qwerty123"])
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(3, 6)))


def _moderate() -> str:
    word = rng.choice(["River", "Sunset", "Orbit", "Nimbus", "Cedar"])
    return word + str(rng.randint(10, 99)) + rng.choice(["!", "@", ""])


def _strong() -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    length = rng.randint(12, 16)
    return "".join(rng.choice(alphabet) for _ in range(length))


def _very_strong() -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    length = rng.randint(18, 28)
    return "".join(rng.choice(alphabet) for _ in range(length))


def generate_dataset(n: int = 2000) -> tuple[list[str], list[str]]:
    passwords: list[str] = []
    makers = [
        (_weak, 700),
        (_moderate, 400),
        (_strong, 500),
        (_very_strong, 400),
    ]
    for maker, count in makers:
        for _ in range(count):
            passwords.append(maker())
    leftover = n - len(passwords)
    for _ in range(max(0, leftover)):
        passwords.append(_weak())

    labels = [analyze_password(pwd, include_ml=False)["strength"] for pwd in passwords]
    return passwords, labels


def train() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    passwords, labels = generate_dataset()
    x = dataframe_from_passwords(passwords)
    y = np.array(labels)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y if len(set(y)) > 1 else None
    )

    models = {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(max_iter=400, class_weight="balanced", random_state=42),
                ),
            ]
        ),
        "decision_tree": DecisionTreeClassifier(max_depth=12, random_state=42, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=180,
            max_depth=14,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced_subsample",
            n_jobs=-1,
        ),
    }

    comparison = {}
    best_name = "random_forest"
    best_f1 = -1.0
    best_model = None

    for name, model in models.items():
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        f1 = f1_score(y_test, preds, average="weighted", zero_division=0)
        acc = accuracy_score(y_test, preds)
        comparison[name] = {
            "accuracy": round(float(acc), 4),
            "precision_weighted": round(
                float(precision_score(y_test, preds, average="weighted", zero_division=0)), 4
            ),
            "recall_weighted": round(
                float(recall_score(y_test, preds, average="weighted", zero_division=0)), 4
            ),
            "f1_weighted": round(float(f1), 4),
            "classification_report": classification_report(
                y_test, preds, labels=STRENGTH_LABELS, output_dict=True, zero_division=0
            ),
            "confusion_matrix": confusion_matrix(y_test, preds, labels=STRENGTH_LABELS).tolist(),
        }
        prefer_rf = name == "random_forest" and f1 >= best_f1 - 0.01
        if f1 > best_f1 or prefer_rf:
            best_f1 = f1
            best_name = name
            best_model = model

    assert best_model is not None
    joblib.dump(best_model, MODEL_PATH)

    importances = []
    forest = best_model
    if hasattr(forest, "feature_importances_"):
        importances = [
            {"feature": name, "importance": round(float(value), 4)}
            for name, value in zip(FEATURE_NAMES, forest.feature_importances_)
        ]
        importances.sort(key=lambda row: row["importance"], reverse=True)

    metadata = {
        "model_name": best_name,
        "feature_names": FEATURE_NAMES,
        "labels": STRENGTH_LABELS,
        "feature_importance": importances,
        "training_samples": int(len(y)),
        "notes": (
            "Trained on synthetic passwords labeled by the project's scoring engine. "
            "This is an academic model, not a production credential classifier."
        ),
    }
    FEATURE_METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    evaluation = {
        "selected_model": best_name,
        "labels": STRENGTH_LABELS,
        "comparison": comparison,
        "selected": comparison[best_name],
        "feature_importance": importances,
    }
    EVALUATION_PATH.write_text(json.dumps(evaluation, indent=2), encoding="utf-8")
    serialize_report(evaluation)
    print(f"Saved {best_name} to {MODEL_PATH}")
    print(json.dumps({k: v["f1_weighted"] for k, v in comparison.items()}, indent=2))


if __name__ == "__main__":
    train()
