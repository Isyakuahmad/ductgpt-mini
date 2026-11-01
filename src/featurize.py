"""Composition parsing and Pugh-ratio helpers. G/K is a heuristic, not a ductility measurement."""
import re
from collections import defaultdict
_TOKEN = re.compile(r"([A-Z][a-z]?)([0-9]*\.?[0-9]*)")
def parse_formula(formula: str) -> dict[str, float]:
    if not isinstance(formula, str) or not formula: raise ValueError("formula must be non-empty")
    pos, amounts = 0, defaultdict(float)
    for m in _TOKEN.finditer(formula):
        if m.start() != pos: raise ValueError(f"Unsupported formula near {formula[pos:]!r}")
        amounts[m.group(1)] += float(m.group(2)) if m.group(2) else 1.0
        pos = m.end()
    if pos != len(formula) or not amounts: raise ValueError(f"Invalid formula: {formula}")
    total=sum(amounts.values())
    return {k:v/total for k,v in amounts.items()}
def pugh_ratio(bulk_modulus: float, shear_modulus: float) -> float:
    if bulk_modulus <= 0 or shear_modulus <= 0: raise ValueError("Moduli must be positive")
    return float(shear_modulus)/float(bulk_modulus)
def composition_features(formula: str) -> dict[str,float]:
    return {f"fraction_{k}":v for k,v in sorted(parse_formula(formula).items())}
