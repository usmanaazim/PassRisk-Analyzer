from __future__ import annotations

import pandas as pd

from security.analyzer import FEATURE_NAMES, feature_vector

__all__ = ["FEATURE_NAMES", "vector_to_array", "dataframe_from_passwords"]


def vector_to_array(vector: dict[str, float]) -> pd.DataFrame:
    return pd.DataFrame([vector], columns=FEATURE_NAMES)


def dataframe_from_passwords(passwords: list[str]) -> pd.DataFrame:
    rows = [feature_vector(item) for item in passwords]
    return pd.DataFrame(rows, columns=FEATURE_NAMES)
