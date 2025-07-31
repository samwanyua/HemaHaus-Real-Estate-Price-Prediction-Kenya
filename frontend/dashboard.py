# frontend/dashboard.py

import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Load processed data
DATA_PATH = os.path.join("data", "processed", "transformed_data.csv")
df = pd.read_csv(DATA_PATH)

st.set_page_config(layout="wide", page_title="Real Estate Dashboard")

st.markdown("<h3 style='text-align: left;'>HemaHaus Real Estate Listings Dashboard</h3>", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns([1.2, 2, 3.3, 3])  

# ────────────────────────────
#  Column 1: Filters
# ────────────────────────────
with col1:
    st.header("Filters")

    # Location filter
    location = st.multiselect("Location", df["location"].dropna().unique())

    # Number of bedrooms
    bedrooms = st.multiselect("Bedrooms", sorted(df["bedrooms"].dropna().unique()))

    # Number of bathrooms
    bathrooms = st.multiselect("Bathrooms", sorted(df["bathrooms"].dropna().unique()))

    # Price range slider
    min_price = int(df["price"].min())
    max_price = int(df["price"].max())
    price_range = st.slider("Price Range (KES)", min_value=min_price, max_value=max_price, value=(min_price, max_price), step=1000000)

    # Apply filters
    filtered_df = df.copy()

    if location:
        filtered_df = filtered_df[filtered_df["location"].isin(location)]
    if bedrooms:
        filtered_df = filtered_df[filtered_df["bedrooms"].isin(bedrooms)]
    if bathrooms:
        filtered_df = filtered_df[filtered_df["bathrooms"].isin(bathrooms)]
    if price_range:
        filtered_df = filtered_df[(filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])]

# ────────────────────────────
# Column 2: KPI Metrics
# ────────────────────────────
with col2:

    total_listings = len(filtered_df)
    avg_price = filtered_df["price"].mean() if not filtered_df.empty else 0

    if "price_per_sqm" in filtered_df.columns:
        avg_price_per_sqm = filtered_df["price_per_sqm"].mean()
    elif "size_sqm" in filtered_df.columns:
        avg_price_per_sqm = (filtered_df["price"] / filtered_df["size_sqm"]).mean()
    else:
        avg_price_per_sqm = 0

    median_bedrooms = filtered_df["bedrooms"].median() if "bedrooms" in filtered_df.columns else None

    # Display KPIs
    st.metric(label="Total Listings", value=f"{total_listings:,}")
    st.metric(label="Average Price", value=f"KES {avg_price:,.0f}")
    st.metric(label="Avg. Price per Sqm", value=f"KES {avg_price_per_sqm:,.0f}/sqm" if avg_price_per_sqm else "N/A")
    st.metric(label="Median Bedrooms", value=f"{int(median_bedrooms)}" if median_bedrooms else "N/A")

    
# ────────────────────────────
#  Column 3: Price Distribution
# ────────────────────────────
with col3:

    if not filtered_df.empty:
        top_locations = (
            filtered_df.groupby("location")
            .agg(avg_price=("price", "mean"), listing_count=("price", "count"))
            .sort_values("avg_price", ascending=False)
            .head(10)
            .reset_index()
        )

        fig_bar = px.bar(
            top_locations,
            x="avg_price",
            y="location",
            orientation="h",
            text="avg_price",
            labels={"avg_price": "Average Price (KES)", "location": "Location"},
            title="Top 10 Locations by Avg. Price"
        )

        fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_bar.update_layout(yaxis=dict(autorange="reversed"))  # highest at top
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data to display for selected filters.")

    


# ────────────────────────────
# Column 4: Listings by Price Range
# ────────────────────────────
with col4:

    if not filtered_df.empty:
        # Define bins and labels
        bins = [0, 5e6, 10e6, 20e6, 50e6, 100e6, 200e6]
        labels = ['<5M', '5–10M', '10–20M', '20–50M', '50–100M', '>100M']

        # Categorize prices
        filtered_df["price_range"] = pd.cut(filtered_df["price"], bins=bins, labels=labels)

        # Count listings per price range
        price_range_counts = filtered_df["price_range"].value_counts().sort_index().reset_index()
        price_range_counts.columns = ["price_range", "count"]

        # Plot with Plotly
        fig_price_range = px.bar(
            price_range_counts,
            x="price_range",
            y="count",
            text="count",
            title="Properties by Price Range (KES)",
            labels={"price_range": "Price Range", "count": "Number of Listings"},
        )

        fig_price_range.update_traces(textposition='outside')
        fig_price_range.update_layout(xaxis_title="Price Range (KES)", yaxis_title="Count")
        st.plotly_chart(fig_price_range, use_container_width=True)
    else:
        st.info("No data to display for selected filters.")

