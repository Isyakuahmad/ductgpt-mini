# DuctGPT-Mini 🧪⚛️

> An open research prototype for reproducible screening of tungsten-based alloy candidates.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

## What it does

DuctGPT-Mini provides an inspectable workflow to fetch tungsten-containing elasticity records, calculate the Pugh ratio (G/K), screen candidates using explicit thresholds, and experiment with a baseline Random Forest model. Screening works locally using the included illustrative fixture and does not require API keys.

This is an independent community prototype inspired by natural-language materials-discovery concepts. It is not affiliated with or endorsed by Ames National Laboratory and does not reproduce a proprietary system.

## Workflow

![Workflow](docs/images/workflow.svg)

## Quick start

```bash
git clone https://github.com/Isyakuahmad/ductgpt-mini.git
cd ductgpt-mini
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
pytest -q
python -m src.llm_agent --data data/sample_W_alloys.csv --max-pugh 0.57
```

Optional interface: `streamlit run app/streamlit_app.py`.

## Materials Project data (optional)

Copy `.env.example` to `.env`, add your Materials Project API key, then run:

```bash
python -m src.fetch_data
```

Downloaded records are saved under `data/`; generated datasets are ignored by Git by default.

## Exploratory baseline

```bash
python -m src.train_model --data data/sample_W_alloys.csv
```

The included fixture is synthetic and deliberately small. A model trained on it is only a software demonstration, not a scientifically useful predictor. Use a sufficiently large, curated dataset and appropriate validation before drawing conclusions.

## Scientific caveats

- Pugh ratio is an empirical heuristic, not a direct measurement or guarantee of ductility.
- Materials Project values are computational data, not necessarily experimental measurements.
- The sample CSV contains illustrative software-test values, not real alloy results.
- Predictions and rankings require independent verification, literature review, and, where appropriate, DFT and experimental validation.

See [architecture](docs/architecture.md), [data notes](data/README.md), and [MIT License](LICENSE).
