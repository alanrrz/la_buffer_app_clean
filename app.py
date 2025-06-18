import os
import math
import requests
import pandas as pd
import streamlit as st

# ─── STEP 1: DOWNLOAD CSVs VIA PRESIGNED S3 URLs ─────────────────────────
for fname, url in DATA_URLS.items():
    if not os.path.exists(fname):
        st.write("🔗 Trying URL:", url)
        resp = requests.get(url)
        st.write("⏱️ Status code:", resp.status_code)
        # show the first 200 chars of any error body
        if resp.status_code != 200:
            st.write("⚠️ Response body snippet:", resp.text[:200])
        resp.raise_for_status()
        with open(fname, "wb") as f:
            f.write(resp.content)


# ─── STEP 2: LOAD DATA ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Both CSVs are semicolon-delimited:
    #  - schools.csv → label;lon;lat
    #  - addresses.csv → address;lon;lat
    schools   = pd.read_csv("schools.csv",   sep=";")
    addresses = pd.read_csv("addresses.csv", sep=";")
    return schools, addresses

schools, addresses = load_data()

# ─── STEP 3: APP UI ───────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Pick a school and buffer radius to generate your mailing list.")

selected  = st.selectbox("Select a School", schools["label"].sort_values().unique())
radius_mi = st.slider("Buffer radius (miles)", 0.25, 2.0, 0.5, 0.25)

# ─── STEP 4: DISTANCE CALCULATION ────────────────────────────────────────
def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat/2)**2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon/2)**2
    )
    return 2 * R * math.asin(math.sqrt(a))

row = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]

distances = [
    haversine(slon, slat, float(r["lon"]), float(r["lat"]))
    for _, r in addresses.iterrows()
]
addresses["distance"] = distances
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & EXPORT ────────────────────────────────────────────
st.markdown(f"**Found {len(within)} addresses** within **{radius_mi} miles** of **{selected}**")

if not within.empty:
    map_df = within.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(map_df[["latitude", "longitude"]])

    out_csv = within.rename(
        columns={"lon": "longitude", "lat": "latitude"}
    )[["address", "longitude", "latitude", "distance"]].to_csv(index=False)

    st.download_button(
        "⬇️ Download Mailing List",
        data=out_csv,
        file_name=f"{selected.replace(' ','_')}_{radius_mi}mi.csv",
        mime="text/csv"
    )
else:
    st.info("No addresses found in that buffer.")
