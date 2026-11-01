"""CLI entry point. Structured arguments are used until safe LLM parsing is implemented."""
import argparse, pandas as pd
from src.screen import screen_alloys

def main():
    p=argparse.ArgumentParser(description="Screen tungsten alloy records")
    p.add_argument("--data",default="data/sample_W_alloys.csv"); p.add_argument("--max-pugh",type=float,default=.57)
    p.add_argument("--min-bulk",type=float,default=None); p.add_argument("--elements",nargs="*",default=None); a=p.parse_args()
    print(screen_alloys(pd.read_csv(a.data),max_pugh=a.max_pugh,min_bulk_modulus=a.min_bulk,elements=a.elements).to_string(index=False))
if __name__=="__main__": main()
