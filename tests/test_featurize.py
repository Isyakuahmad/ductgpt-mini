import pytest
from src.featurize import parse_formula,pugh_ratio,composition_features

def test_parse_formula():
    assert parse_formula("WTa2")["Ta"]==pytest.approx(2/3)
def test_parse_fractional_formula():
    assert parse_formula("W0.5Ta0.5")["W"]==pytest.approx(.5)
def test_invalid_formula():
    with pytest.raises(ValueError): parse_formula("W-Ta")
def test_pugh_ratio():
    assert pugh_ratio(250,125)==pytest.approx(.5)
def test_invalid_moduli():
    with pytest.raises(ValueError): pugh_ratio(0,10)
def test_features():
    assert composition_features("W2Ta")["fraction_W"]==pytest.approx(2/3)
