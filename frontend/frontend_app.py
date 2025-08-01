import streamlit as st
import numpy as np
import pandas as pd
import os
import joblib
import gdown

# -- Google Drive File IDs --
MODEL_ID = "1Ji6fV483psbeDW7BrOWEGHEbaiBdSPWV"
SCALER_ID = "1cVmJk8__YsW4ts9gb0uiP4g3r9E3Pe_D"
LOC_ID = "16sMvNl12SrnSl6eVpSjkN0OU5lly84jV"

# -- File Paths --
os.makedirs("models", exist_ok=True)
model_path = "models/tuned_random_forest_model.pkl"
scaler_path = "models/scaler.pkl"
loc_path = "models/location_columns.pkl"

# -- Download if missing --
def download_if_missing(file_id, path):
    if not os.path.exists(path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, path, quiet=False)

download_if_missing(MODEL_ID, model_path)
download_if_missing(SCALER_ID, scaler_path)
download_if_missing(LOC_ID, loc_path)

# -- Load model assets --
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
with open(loc_path, "rb") as f:
    location_columns = joblib.load(f)

# -- Streamlit UI --
st.set_page_config(page_title="Hemahaus Price Predictor", layout="centered")
st.title("Hemahaus Real Estate Price Predictor")

# Location options
location_options = sorted([
    'Athi River', 'Bamburi', 'Bofa Beach', 'Buruburu', 'Dagoretti', 'Diani', 'Donholm', 'Embakasi', 'Garden Estate',
    'Gigiri', 'Highridge', 'Hurlingham', 'Imara Daima', 'Joska', 'Juja', 'Kabete', 'Kahawa West', 'Kahawa sukari',
    'Kajiado', 'Kamakis', 'Karen', 'Kasarani', 'Katani', 'Kerarapon', 'Kiambu', 'Kiambu Road', 'Kiembeni',
    'Kikambala', 'Kikuyu', 'Kileleshwa', 'Kilifi', 'Kilimani', 'Kiserian', 'Kisumu CBD', 'Kitengela', 'Kitisuru',
    'Kizingo', 'Kyuna', 'Langata', 'Lavington', 'Lenana', 'Limuru', 'Loresho', 'Lower Kabete', 'Machakos',
    'Malindi', 'Matasia', 'Membley', 'Mirema', 'Mlolongo', 'Mombasa CBD', 'Mombasa Island', 'Mombasa Rd',
    'Mountain View', 'Mtwapa', 'Muthaiga', 'Muthaiga North', 'Nairobi CBD', 'Nairobi West', 'Naivasha',
    'Nakuru Town', 'Nanyuki', 'Ndeiya', 'Ngong', 'Ngong Rd', 'Ngumo estate', 'Nyali', 'Nyari', 'Nyayo',
    'Ongata Rongai', 'Other', 'Pangani', 'Parklands', 'Peponi', 'Redhill', 'Ridgeways', 'Riruta', 'Riverside',
    'Rosslyn', 'Roysambu', 'Ruai', 'Ruaka', 'Ruaraka', 'Ruiru', 'Runda', 'Shanzu', 'Sigona', 'South B', 'South C',
    'Spring Valley', 'Syokimau', 'Thigiri', 'Thika', 'Thindigua', 'Thogoto', 'Thome', 'Tigoni', 'Upper Hill',
    'Utange', 'Utawala', 'Uthiru', 'Valley Arcade', 'Vipingo', 'Wangige', 'Watamu', 'Westlands'
])

# -- Inputs in columns --
col1, col2 = st.columns(2)
with col1:
    location = st.selectbox("Select Location", location_options)
    bedrooms = st.number_input("Bedrooms", min_value=0, value=2)
    bathrooms = st.number_input("Bathrooms", min_value=0, value=1)
with col2:
    parking = st.number_input("Parking Spots", min_value=0, value=1)
    size_sqm = st.number_input("Size (sqm)", min_value=0, value=80)

# -- Predict Button --
if st.button("Predict Price"):
    # Handle unknown locations
    location = location if location in location_columns else "Other"

    loc_data = {f"loc_{col}": 0 for col in location_columns}
    if f"loc_{location}" in loc_data:
        loc_data[f"loc_{location}"] = 1

    numeric = pd.DataFrame([[bedrooms, bathrooms, parking, size_sqm]],
                           columns=["bedrooms", "bathrooms", "parking", "size_sqm"])
    numeric_scaled = pd.DataFrame(scaler.transform(numeric), columns=numeric.columns)

    input_df = pd.concat([numeric_scaled, pd.DataFrame([loc_data])], axis=1)

    # Predict
    price = model.predict(input_df)[0]
    st.success(f"Estimated Price: KES {price:,.0f}")
