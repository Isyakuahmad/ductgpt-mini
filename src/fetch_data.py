"""Fetch tungsten-containing elasticity records from Materials Project."""
import argparse, os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from mp_api.client import MPRester

def fetch_tungsten_alloys(output="data/mp_tungsten_alloys.csv"):
    load_dotenv(); key=os.getenv("MP_API_KEY")
    if not key: raise RuntimeError("MP_API_KEY missing; copy .env.example to .env")
    with MPRester(key) as mpr:
        docs=mpr.materials.elasticity.search(elements=["W"],fields=["material_id","formula_pretty","bulk_modulus","shear_modulus"])
    rows=[]
    for d in docs:
        k,g=d.bulk_modulus,d.shear_modulus
        if k is None or g is None or k<=0 or g<=0: continue
        rows.append({"material_id":str(d.material_id),"formula":d.formula_pretty,"bulk_modulus_GPa":float(k),"shear_modulus_GPa":float(g),"pugh_ratio":float(g)/float(k),"data_source":"Materials Project"})
    frame=pd.DataFrame(rows)
    if frame.empty: raise RuntimeError("No complete elasticity records returned")
    path=Path(output); path.parent.mkdir(parents=True,exist_ok=True); frame.to_csv(path,index=False)
    return frame
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--output",default="data/mp_tungsten_alloys.csv"); a=p.parse_args()
    print(f"Saved {len(fetch_tungsten_alloys(a.output))} records to {a.output}")
