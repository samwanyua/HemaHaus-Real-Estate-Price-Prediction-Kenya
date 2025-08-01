from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
import os
import gdown

os.environ["GDOWN_CACHE_DIR"] = "/tmp"

app = FastAPI()

# --- Helper function to download from Google Drive ---
def download_from_gdrive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False, use_cookies=False)

# --- File IDs and paths ---
model_id = "1Ji6fV483psbeDW7BrOWEGHEbaiBdSPWV"
scaler_id = "1cVmJk8__YsW4ts9gb0uiP4g3r9E3Pe_D"
loc_id = "16sMvNl12SrnSl6eVpSjkN0OU5lly84jV"

os.makedirs("/tmp/models", exist_ok=True)
model_path = "/tmp/models/tuned_random_forest_model.pkl"
scaler_path = "/tmp/models/scaler.pkl"
loc_path = "/tmp/models/location_columns.pkl"


# --- Download files if missing ---
if not os.path.exists(model_path):
    download_from_gdrive(model_id, model_path)
if not os.path.exists(scaler_path):
    download_from_gdrive(scaler_id, scaler_path)
if not os.path.exists(loc_path):
    download_from_gdrive(loc_id, loc_path)

# --- Load models ---
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
with open(loc_path, "rb") as f:
    location_columns = joblib.load(f)

# --- Input schema ---
class HouseFeatures(BaseModel):
    location: str
    bedrooms: int
    bathrooms: int
    parking: int
    size_sqm: float

@app.get("/")
def read_root():
    return {"message": "HemaHaus Real Estate Price Prediction API"}

@app.post("/predict")
def predict_price(features: HouseFeatures):
    location = features.location
    if location not in location_columns:
        location = "Other"

    # One-hot encode location
    loc_data = {f"loc_{col}": 0 for col in location_columns}
    if f"loc_{location}" in loc_data:
        loc_data[f"loc_{location}"] = 1

    numeric = pd.DataFrame([[
        features.bedrooms,
        features.bathrooms,
        features.parking,
        features.size_sqm
    ]], columns=['bedrooms', 'bathrooms', 'parking', 'size_sqm'])

    numeric_scaled = pd.DataFrame(scaler.transform(numeric), columns=numeric.columns)
    combined = pd.concat([numeric_scaled, pd.DataFrame([loc_data])], axis=1)

    prediction = model.predict(combined)[0]
    return {"predicted_price": f"KES {prediction:,.0f}"}
