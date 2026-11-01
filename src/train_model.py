"""Exploratory Random Forest baseline; not a validated materials predictor."""
import argparse
from pathlib import Path
import joblib, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from src.featurize import composition_features

def train(csv_path,model_path="models/pugh_rf.joblib"):
    df=pd.read_csv(csv_path).dropna(subset=["formula","pugh_ratio"])
    if len(df)<5: raise ValueError("At least five complete rows are required")
    vec=DictVectorizer(sparse=False); x=vec.fit_transform([composition_features(f) for f in df.formula]); y=df.pugh_ratio.astype(float)
    xt,xv,yt,yv=train_test_split(x,y,test_size=.2,random_state=42)
    model=make_pipeline(SimpleImputer(),RandomForestRegressor(n_estimators=200,random_state=42))
    model.fit(xt,yt); mae=mean_absolute_error(yv,model.predict(xv))
    path=Path(model_path); path.parent.mkdir(parents=True,exist_ok=True); joblib.dump({"vectorizer":vec,"model":model},path)
    return float(mae)
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--data",default="data/sample_W_alloys.csv"); p.add_argument("--output",default="models/pugh_rf.joblib"); a=p.parse_args()
    print(f"Exploratory holdout MAE: {train(a.data,a.output):.4f}")
