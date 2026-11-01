"""Fetch tungsten-containing elasticity records from Materials Project."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from mp_api.client import MPRester

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "mp_tungsten_alloys.csv"
FIELDS = [
    "material_id",
    "formula_pretty",
    "bulk_modulus",
    "shear_modulus",
]


def fetch_tungsten_alloys(output: str | Path = DEFAULT_OUTPUT) -> pd.DataFrame:
    """Fetch W-containing materials with complete, positive elastic moduli."""
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("MP_API_KEY")
    if not api_key:
        raise RuntimeError(
            "MP_API_KEY is not set. Copy .env.example to .env and add your "
            "Materials Project API key."
        )

    with MPRester(api_key) as mpr:
        documents = mpr.materials.elasticity.search(
            elements=["W"],
            fields=FIELDS,
        )

    rows = []
    for doc in documents:
        bulk = getattr(doc, "bulk_modulus", None)
        shear = getattr(doc, "shear_modulus", None)
        formula = getattr(doc, "formula_pretty", None)
        material_id = getattr(doc, "material_id", None)

        if (
            bulk is None
            or shear is None
            or formula is None
            or material_id is None
            or bulk <= 0
            or shear <= 0
        ):
            continue

        bulk = float(bulk)
        shear = float(shear)
        rows.append(
            {
                "material_id": str(material_id),
                "formula": str(formula),
                "bulk_modulus_GPa": bulk,
                "shear_modulus_GPa": shear,
                "pugh_ratio": shear / bulk,
                "data_source": "Materials Project",
            }
        )

    frame = pd.DataFrame(rows)
    if frame.empty:
        raise RuntimeError(
            "Materials Project returned no records with complete positive "
            "bulk and shear moduli for tungsten-containing materials."
        )

    frame = (
        frame.drop_duplicates(subset=["material_id"])
        .sort_values(["pugh_ratio", "bulk_modulus_GPa"])
        .reset_index(drop=True)
    )

    output_path = Path(output).expanduser()
    if not output_path.is_absolute():
        output_path = (ROOT / output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download tungsten-alloy elasticity data from Materials Project."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Destination CSV path (default: data/mp_tungsten_alloys.csv)",
    )
    args = parser.parse_args()

    try:
        frame = fetch_tungsten_alloys(args.output)
    except Exception as exc:
        parser.exit(1, f"Error fetching Materials Project data: {exc}\n")

    print(f"Saved {len(frame)} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
