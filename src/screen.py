"""Transparent rule-based screening; no missing properties are imputed."""
import pandas as pd
REQUIRED={"formula","bulk_modulus_GPa","shear_modulus_GPa","pugh_ratio"}
def screen_alloys(data: pd.DataFrame, *, max_pugh: float=0.57, min_bulk_modulus: float|None=None, elements: list[str]|None=None) -> pd.DataFrame:
    missing=REQUIRED-set(data.columns)
    if missing: raise ValueError(f"Missing required columns: {sorted(missing)}")
    out=data.dropna(subset=list(REQUIRED)).copy()
    out=out[out.pugh_ratio<=max_pugh]
    if min_bulk_modulus is not None: out=out[out.bulk_modulus_GPa>=min_bulk_modulus]
    if elements: out=out[out.formula.apply(lambda f: all(e in f for e in elements))]
    return out.sort_values(["pugh_ratio","bulk_modulus_GPa"],ascending=[True,False]).reset_index(drop=True)
