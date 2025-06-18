import os
import math
import requests
import pandas as pd
import streamlit as st

# ─── DOWNLOAD CSVs FROM GOOGLE DRIVE ────────────────────────────────────
def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    # 1. Initial request
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    # 2. Confirm token if present
    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    # 3. Save to disk
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# Map filenames to Google Drive file IDs
DRIVE_FILES = {
    "schools.csv":   "1XtSN-3iP1ruQRjmt9K8OWZuo0hHHOK3l",
    "addresses.csv": "1p4C7wCVfd_e5OvLnOVLUYjpFgulM3pGV"
}

for fname, file_id in DRIVE_FILES.items():
    if not os.path.exists(fname):
        with st.spinner(f"Downloading {fname}…"):
            download_file_from_google_drive(file_id, fname)

# ─── LOAD DATA ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Both CSVs now live in the working directory
    schools   = pd.read_csv("schools.csv")     # expects columns: label, lon, lat
    addresses = pd.read_csv("addresses.csv")  # expects columns: address, lon, lat
    return schools, addresses

schools, addresses = load_data()

# ─── APP HEADER & CONTROLS ─────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Choose a school and buffer radius to generate your mailing list.")

selected = st.selectbox(
    "Select a School", 
    schools["label"].sort_values().unique()
)
radius_mi = st.slider(
    "Buffer radius (miles)", 
    min_value=0.25, max_value=2.0, value=0.5, step=0.25
)

# ─── FIND SELECTED SCHOOL COORDS ───────────────────────────────────────
school_row = schools[schools["label"] == selected].iloc[0]
slon, slat = school_row["lon"], school_row["lat"]

# ─── HAVERSINE DISTANCE FUNCTION ────────────────────────────────────────
def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))

# ─── COMPUTE DISTANCES & FILTER ADDRESSES ───────────────────────────────
addresses["distance"] = addresses.apply(
    lambda r: haversine(slon, slat, r["lon"], r["lat"]), axis=1
)
within = addresses[addresses["distance"] <= radius_mi]

# ─── DISPLAY RESULTS & DOWNLOAD ─────────────────────────────────────────
st.markdown(
    f"**Found {len(within)} addresses** within **{radius_mi} miles** of **{selected}**"
)

if not within.empty:
    # Map preview (expects columns latitude, longitude)
    map_df = within.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(map_df[["latitude", "longitude"]])

    # Prepare CSV for download
    out = within[["address", "lon", "lat", "distance"]].rename(
        columns={"lon": "longitude", "lat": "latitude"}
    )
    csv = out.to_csv(index=False)

    st.download_button(
        "⬇️ Download Mailing List",
        data=csv,
        file_name=f"{selected.replace(' ', '_')}_{radius_mi}mi.csv",
        mime="text/csv"
    )
else:
    st.info("No addresses found in that buffer.")
