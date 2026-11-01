import pandas as pd
from src.screen import screen_alloys

def fixture():
    return pd.DataFrame([{"formula":"WTa","bulk_modulus_GPa":260,"shear_modulus_GPa":130,"pugh_ratio":.5},{"formula":"WCr","bulk_modulus_GPa":240,"shear_modulus_GPa":150,"pugh_ratio":.625},{"formula":"WRe","bulk_modulus_GPa":300,"shear_modulus_GPa":165,"pugh_ratio":.55}])
def test_thresholds_and_sorting():
    assert screen_alloys(fixture(),max_pugh=.57,min_bulk_modulus=250).formula.tolist()==["WTa","WRe"]
def test_element_filter():
    assert screen_alloys(fixture(),elements=["Ta"]).formula.tolist()==["WTa"]
