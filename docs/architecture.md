# Architecture

1. **Data:** `src.fetch_data` downloads tungsten-containing elasticity records from Materials Project (API key required).
2. **Features:** `src.featurize` parses simple formulae and computes G/K from supplied moduli.
3. **Screening:** `src.screen` applies transparent thresholds without imputing missing values.
4. **Baseline ML:** `src.train_model` fits an exploratory Random Forest using elemental fractions.
5. **Interface:** CLI and optional Streamlit UI call the deterministic screening function. The LLM-named CLI currently uses structured flags; natural-language parsing is intentionally deferred until safe tool-call validation exists.

## Scientific limits

Pugh ratio is an empirical heuristic, not a direct ductility measurement. Materials Project data is computational and is not necessarily experimental. Synthetic fixture data is for software tests only. Verify candidates with literature, appropriate calculations and experiments before engineering claims.
