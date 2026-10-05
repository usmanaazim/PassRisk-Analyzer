# Machine learning

## Features

length, uppercase_count, lowercase_count, digit_count, special_count, unique_character_count, character_diversity, entropy, dictionary_match, dictionary_similarity, repeated_character_score, sequence_score, keyboard_pattern_score, year_pattern, common_word_score, predictability_score.

## Target

VERY_WEAK, WEAK, MODERATE, STRONG, VERY_STRONG — assigned by the same scoring engine used in the API. This yields an explainable academic classifier; it is not an independent human-labeled corpus.

## Models

1. Logistic Regression (scaled features, balanced classes)
2. Decision Tree (`max_depth=12`)
3. Random Forest (`n_estimators=180`)

A 75/25 stratified split is used. Accuracy, precision, recall, weighted F1, classification report, and confusion matrix are stored in `backend/models/evaluation.json`.

The Random Forest F1 is typically very high because labels are produced from the same feature family the model sees. That is expected for a policy-learning academic model, not evidence of an independently labeled human study.

## Inference

`ml/predict.py` loads the joblib artifact once. If the file is missing, the API falls back to the heuristic label and reports `available: false`.

## Ethics

Do not train on leaked personal credentials. Retrain with `PYTHONPATH=. python ml/train_model.py` from `backend/`.
