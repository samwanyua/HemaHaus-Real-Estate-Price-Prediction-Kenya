from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import os

app = FastAPI()

# load model
model_path = os.path.join("models", "tuned_random_forest_model.pkl")
model = joblib.load(model_path)

