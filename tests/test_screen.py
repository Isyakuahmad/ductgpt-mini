from pathlib import Path

import pandas as pd

from src.screen import screen_alloys


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "sample_W_alloys.csv"


def load_sample():
    """Load the committed local fixture; tests never require an API key."""
    return pd.read_csv(DATA_FILE)


def test_sample_dataset_is_available():
    df = load_sample()
    assert not df.empty
    assert {"formula", "bulk_modulus_GPa", "shear_modulus_GPa", "pugh_ratio"} <= set(df.columns)


def test_thresholds_and_sorting():
    result = screen_alloys(
        load_sample(),
        max_pugh=0.57,
        min_bulk_modulus=250,
    )
    assert result["formula"].tolist() == ["WTi", "WTa", "W2Ta", "WMo", "WTa2", "WRe"]


def test_element_filter():
    result = screen_alloys(load_sample(), elements=["Ta"])
    assert result["formula"].tolist() == ["WTa", "W2Ta", "WTa2"]


def test_combined_filters():
    result = screen_alloys(
        load_sample(),
        max_pugh=0.53,
        min_bulk_modulus=255,
        elements=["Ta"],
    )
    assert result["formula"].tolist() == ["WTa", "W2Ta", "WTa2"]
