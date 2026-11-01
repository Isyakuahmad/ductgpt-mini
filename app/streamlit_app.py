from pathlib import Path
import pandas as pd
import streamlit as st
from src.screen import screen_alloys
st.set_page_config(page_title="DuctGPT-Mini",page_icon="🧪")
st.title("DuctGPT-Mini")
st.caption("Exploratory screening only — not experimental validation.")
upload=st.file_uploader("Optional CSV",type="csv")
data=pd.read_csv(upload) if upload else pd.read_csv(Path("data/sample_W_alloys.csv"))
max_pugh=st.slider("Maximum Pugh ratio (G/K)",.1,1.0,.57,.01)
min_bulk=st.number_input("Minimum bulk modulus (GPa)",min_value=0.0,value=0.0)
st.dataframe(screen_alloys(data,max_pugh=max_pugh,min_bulk_modulus=min_bulk or None),use_container_width=True)
st.info("Pugh ratio is a heuristic, not a direct measurement of ductility.")
