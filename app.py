# app.py

import os
import pandas as pd
import math
import folium
import requests
from streamlit_folium import st_folium
import streamlit as st

# ─── Dropbox URLs ───────────────────────────────────────────────────────
DROPBOX_LINKS = {
    "addresses.csv": "https://www.dropbox.com/scl/fi/ika7darb79t1zbuzjpj90/addresses.csv?rlkey=h8anuof8jc4n70ynsrwd9svue&dl=1",
    "schools.csv":   "https://www.dropbox.com/scl/fi/qt5wmh9raabpjjykuvslt/schools.csv?rlkey=m7xtw0790sfv9djxz62h2ypzk&dl=1"
}

# ─── Download files if not present ──────────────────────────────────────
for fname, url in DROPBOX_LINKS.items():
    if not os.path.exists(fname):
        st.info(f"Downloading {fname}...")
        r = requests.get(url)
        with open(fname, "wb") as f:
            f.write(r.content)

# ─── Load data ──────────────────────────────────────────────────────────
schools = pd.read_csv("schools.csv", sep=",")
addresses = pd.read_csv("addresses.csv", sep=";")

# ─── Distance calculation ───────────────────────────────────────────────
def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2)**2
    )
    return 2 * R * math.asin(math.sqrt(a))

# ─── Streamlit UI ────────────────────────────────────────────────────────
st.title("Nearby Address Finder")

school_name = st.selectbox("Select a school:", sorted(schools["label"].unique()))
radius = st.select_slider(
    "Select radius (miles):",
    options=[round(x/10,1) for x in range(1,7)] + list(range(1,6)),
    value=0.5
)

if st.button("Run Buffer"):
    row = schools[schools["label"] == school_name].iloc[0]
    slon, slat = row["lon"], row["lat"]

    addresses["distance"] = addresses.apply(
        lambda r: haversine(slon, slat, r["lon"], r["lat"]), axis=1
    )
    within = addresses[addresses["distance"] <= radius]

    st.write(f"📍 Found {len(within)} addresses within {radius} miles of {school_name}.")

    # ─── Create Map ──────────────────────────────────────────────────────
    m = folium.Map(location=[slat, slon], zoom_start=14, tiles="OpenStreetMap")
    folium.Circle(
        [slat, slon],
        radius=radius * 1609,
        color="blue", fill=False,
        popup=f"{school_name} Buffer"
    ).add_to(m)

    for _, r in within.iterrows():
        folium.Marker(
            [r["lat"], r["lon"]],
            icon=folium.Icon(color="red", icon="envelope"),
            popup=r["address"]
        ).add_to(m)

    st_folium(m, width=700, height=500)

    # ─── Download CSV ────────────────────────────────────────────────────
    csv = within[["address", "lon", "lat", "distance"]].to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{school_name.replace(' ', '_')}_{radius}mi.csv",
        mime="text/csv"
    )
