import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Global Earthquake Monitor",
    layout="wide"
)

# Connect to database
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5440",
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM marts_earthquakes", conn)
    return df

# Load data
df = load_data()

# Title
st.title("Global Earthquake Monitor")
st.write("Tracking earthquake frequency and magnitude by region over time")

# Sidebar filters
st.sidebar.header("Filters")

min_mag = st.sidebar.slider("Minimum Magnitude", 0.0, 10.0, 0.0)
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].dropna().unique(),
    default=df["region"].dropna().unique()
)

# Filter data
filtered_df = df[
    (df["magnitude"] >= min_mag) &
    (df["region"].isin(selected_region))
]

# Key metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Earthquakes", len(filtered_df))
col2.metric("Avg Magnitude", round(filtered_df["magnitude"].mean(), 2))
col3.metric("Tsunami Alerts", filtered_df["is_tsunami"].sum())
col4.metric("Countries Affected", filtered_df["country_name"].nunique())

st.divider()

# Map
st.subheader("Earthquake Locations")
map_df = filtered_df[["latitude", "longitude"]].dropna()
map_df.columns = ["lat", "lon"]
st.map(map_df)

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Earthquakes by Region")
    region_counts = filtered_df["region"].value_counts()
    st.bar_chart(region_counts)

with col2:
    st.subheader("Average Temperature at Earthquake Locations")
    temp_by_region = filtered_df.groupby("region")["temperature"].mean().dropna()
    st.bar_chart(temp_by_region)

st.divider()

# Top 10 most significant earthquakes
st.subheader("Top 10 Most Significant Earthquakes")
top10 = filtered_df.nlargest(10, "significance")[
    ["place", "magnitude", "significance", "is_tsunami", "region", "temperature"]
]
st.dataframe(top10, use_container_width=True)