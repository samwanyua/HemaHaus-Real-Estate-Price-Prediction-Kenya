# HemaHaus - Real Estate Price Prediction (Kenya)

**HemaHaus** is a lightweight MLOps project designed to predict land and house prices in various regions across Kenya using machine learning. The system integrates data scraping, preprocessing, training, model deployment with FastAPI, and a user-friendly Streamlit frontend.

- Dashboard: [Hemahaus Listings Dashboard](https://hemahause-real-estate-listings-dashboard.streamlit.app/)
- Try it out: [Predict House Price](https://huggingface.co/spaces/samwanyua/hemahaus-frontend)

---

## Problem Statement

The Kenyan real estate market is growing rapidly, yet price estimation remains inconsistent due to a lack of centralized pricing data and tools. Many buyers, sellers, and investors lack a reliable and data-driven way to assess property values across different regions.

---

## Solution Statement

HemaHaus solves this by scraping real estate data, building machine learning models to predict property prices, and deploying the system using FastAPI (backend) and Streamlit (frontend). This tool enables users to make accurate, real-time predictions based on input features such as location, size, and type of property.

---

## Objectives

- Scrape property listings from multiple Kenyan cities and towns.
- Clean, format, and geo-tag real estate data.
- Train a predictive ML model on price data.
- Serve the model using FastAPI as a REST API.
- Build an interactive frontend using Streamlit for predictions.
- Store data and models locally (initially) and on S3/Azure Blob storage when scaling.
- Lay groundwork for scaling with PostgreSQL and cloud deployment - AWS.

---

## Locations Covered

- Nairobi, Thika, Kisumu, Eldoret, Malindi, Kikuyu, Kajiado, Kwale, Machakos, Nyeri, Mombasa, Nakuru, Ngong, Nanyuki, Athi River, Naivasha, Juja, Lamu, Nyandarua, Isinya, Kitengela, Ruiru, Kilifi, Kiambu, Kiserian, Limuru, Watamu, Narok, Nyahururu, Ongata Rongai

---

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **Storage**: Postgres, Amazon S3 (future)
- **Database**: PostgreSQL 
- **ML Libraries**: Scikit-learn, Pandas, NumPy, XGBoost
- **Data visualization**: Matplotlib, Plotly, Seaborn
- **CI/CD**: Github Actions, Docker

---

## System Flow Diagram

```text
        [Real Estate Sites]
              ↓
       ┌────────────┐
       │ Scraper.py │ ───→ Clean + Format → Geo-tag → Save to postgres db
       └────────────┘
              ↓
       [data.csv locally]
              ↓
     ┌─────────────────┐
     │ train_model.py  │ → Evaluate + Save → model.pkl 
     └─────────────────┘
              ↓
        [model.pkl ]
              ↓
 ┌─────────────────────────┐
 │  FastAPI (main.py)      │
 │  - Loads model          │
 │  - Predict endpoint     │
 └─────────────────────────┘
              ↓
 ┌─────────────────────────────┐
 │ Streamlit (frontend_app.py)│
 │  - User inputs location,   │
 │    house/land size, etc.   │
 │  - Calls FastAPI API       │
 │  - Displays prediction     │
 └────────────────────────────┘
              ↓
       [User Feedback Loop]
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/samwanyua/HemaHaus-Real-Estate-Price-Prediction-Kenya.git
cd HemaHaus-Real-Estate-Price-Prediction-Kenya
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Streamlit frontend
```bash
streamlit run frontend_app.py
```

### 5. Run FastAPI backend
```bash
uvicorn main:app --reload
```

---

##  Folder Structure

```
HemaHaus-Real-Estate-Price-Prediction-Kenya/
│
├── data/                  # Scraped + processed data
├── models/                # Saved ML models
├── notebooks/             # EDA and training experiments
├── scraper/               # Scraping logic
├── api/                   # FastAPI backend
├── app/                   # Streamlit frontend
├── requirements.txt
└── README.md
```

---

##  License

MIT License