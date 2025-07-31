import streamlit as st
import requests

# Streamlit page setup
st.set_page_config(page_title="Hemahaus Price Predictor", layout="centered")
st.title("Hemahaus Real Estate Price Predictor")

# Input fields
location_options = [
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
]
col1, col2 = st.columns(2)

with col1:
    location = st.selectbox("Select Location", sorted(location_options))
    bedrooms = st.number_input("Bedrooms", min_value=0, value=2)
    bathrooms = st.number_input("Bathrooms", min_value=0, value=1)

with col2:
    parking = st.number_input("Parking Spots", min_value=0, value=1)
    size_sqm = st.number_input("Size (sqm)", min_value=0, value=80)

# Submit button
if st.button("Predict Price"):
    payload = {
        "location": location,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "parking": parking,
        "size_sqm": size_sqm
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f" Estimated Price: {result['predicted_price']}")
        else:
            st.error("Error getting prediction. Check backend logs.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI backend. Make sure it's running.")

