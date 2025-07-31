from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
import os

app = FastAPI()

# load model
model_path = os.path.join("models", "tuned_random_forest_model.pkl")
model = joblib.load(model_path)
scaler_path = os.path.join("models", "scaler.pkl")
scaler = joblib.load(scaler_path)

loc_path = os.path.join("models", "location_columns.pkl")
with open(loc_path, "rb") as f:
    location_columns = joblib.load(f)

# Input schema
class HouseFeatures(BaseModel):
    location: str
    bedrooms: int
    bathrooms: int
    parking: int
    size_sqm: float

@app.get("/")
def read_root():
    return {"message": "HemaHause Real Estate Price Prediction API"}

@app.post("/predict")
def predict_price(features: HouseFeatures):
    # Group rare locations 
    location = features.location
    if location not in location_columns:
        location = "Other"

    # One-hot encode location
    loc_data = {f"loc_{col}": 0 for col in location_columns}
    if f"loc_{location}" in loc_data:
        loc_data[f"loc_{location}"] = 1

    # Numeric features
    numeric = pd.DataFrame([[
        features.bedrooms,
        features.bathrooms,
        features.parking,
        features.size_sqm
    ]], columns=['bedrooms', 'bathrooms', 'parking', 'size_sqm'])

    # Standardize
    numeric_scaled = pd.DataFrame(
        scaler.transform(numeric),
        columns=numeric.columns
    )

    # Combine numeric + location dummy vars
    combined = pd.concat([numeric_scaled, pd.DataFrame([loc_data])], axis=1)

    # Predict
    prediction = model.predict(combined)[0]
    return {"predicted_price": f"KES {prediction:,.0f}"}
