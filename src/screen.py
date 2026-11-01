"""Transparent rule-based screening of alloy candidates."""

import re

import pandas as pd

REQUIRED = {
    "formula",
    "bulk_modulus_GPa",
    "shear_modulus_GPa",
    "pugh_ratio",
}


def screen_alloys(df, max_pugh=0.57, min_bulk_modulus=None, elements=None):
    """Filter alloy candidates by Pugh ratio, bulk modulus and elements."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if not isinstance(max_pugh, (int, float)):
        raise TypeError("max_pugh must be a number")

    if min_bulk_modulus is not None and not isinstance(
        min_bulk_modulus, (int, float)
    ):
        raise TypeError("min_bulk_modulus must be a number or None")

    if elements is not None:
        if not isinstance(elements, list):
            raise TypeError("elements must be a list or None")
        for element in elements:
            if not isinstance(element, str) or not re.fullmatch(
                r"[A-Z][a-z]?", element
            ):
                raise ValueError(f"Invalid element symbol: {element}")

    result = df.dropna(subset=list(REQUIRED)).copy()
    result = result[result["pugh_ratio"] <= max_pugh]

    if min_bulk_modulus is not None:
        result = result[result["bulk_modulus_GPa"] >= min_bulk_modulus]

    if elements:
        def contains_elements(formula):
            symbols = set(re.findall(r"[A-Z][a-z]?", str(formula)))
            return all(element in symbols for element in elements)

        result = result[result["formula"].apply(contains_elements)]

    return result.sort_values(
        ["pugh_ratio", "bulk_modulus_GPa"],
        ascending=[True, False],
    ).reset_index(drop=True)
