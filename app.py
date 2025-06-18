import os
import math
import requests
import pandas as pd
import streamlit as st

# ─── STEP 1: DOWNLOAD CSVs FROM GOOGLE DRIVE ──────────────────────────────
def download_file_from_google_drive(file_id, dest):
    URL = "https://docs.google.com/uc?export=download"
    sess = requests.Session()
    res = sess.get(URL, params={'id': file_id}, stream=True)
    token = next((v for k, v in res.cookies.items() if k.startswith('download_warning')), None)
    if token:
        res = sess.get(URL, params={'id': file_id, 'confirm': token}, stream=True)
    with open(dest, 'wb') as f:
        for chunk in res.iter_content(32768):
            if chunk:
                f.write(chunk)

DRIVE_FILES = {
    "schools.csv":   "1XtSN-3iP1ruQRjmt9K8OWZuo0hHHOK3l",
    "addresses.csv": "1p4C7wCVfd_e5OvLnOVLUYjpFgulM3pGV"
}

for fname, fid in DRIVE_FILES.items():
    if not os.path.exists(fname):
        with st.spinner(f"Downloading {fname}…"):
            download_file_from_google_drive(fid, fname)

# ─── STEP 2: LOAD + AUTO‐RENAME COLUMNS ───────────────────────────────────
@st.cache_data
def load_data():
    schools   = pd.read_csv("schools.csv")
    addresses = pd.read_csv("addresses.csv")

    # 1) Detect & rename the school‐name column → "label"
    sch_candidates = [c for c in schools.columns if c not in ("lon", "lat")]
    if "label" not in schools.columns:
        if "labels" in schools.columns:
            schools.rename(columns={"labels": "label"}, inplace=True)
        elif len(sch_candidates) == 1:
            schools.rename(columns={sch_candidates[0]: "label"}, inplace=True)
        else:
            raise ValueError(f"Cannot determine school‐name column, saw: {sch_candidates}")

    # 2) Detect & rename the address‐text column → "address"
    addr_candidates = [c for c in addresses.columns if c not in ("lon", "lat")]
    if "address" not in addresses.columns:
        if "FullAddress_EnerGov" in addresses.columns:
            addresses.rename(columns={"FullAddress_EnerGov": "address"}, inplace=True)
        elif len(addr_candidates) == 1:
            addresses.rename(columns={addr_candidates[0]: "address"}, inplace=True)
        else:
            raise ValueError(f"Cannot determine address column, saw: {addr_candidates}")

    # 3) Sanity‐check
    assert set(schools.columns) >= {"label", "lon", "lat"}, \
        f"schools.csv missing one of ['label','lon','lat'], got {schools.columns.tolist()}"
    assert set(addresses.columns) >= {"address", "lon", "lat"}, \
        f"addresses.csv missing one of ['address','lon','lat'], got {addresses.columns.tolist()}"

    return schools, addresses

schools, addresses = load_data()

# ─── STEP 3: APP UI ───────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Choose a school and buffer radius to generate your mailing list.")

# Dropdown of school names
school_names = schools["label"].sort_values().unique()
selected     = st.selectbox("Select a School", school_names)

# Buffer radius slider
radius_mi = st.slider(
    "Buffer radius (miles)",
    min_value=0.25, max_value=2.0, value=0.5, step=0.25
)

# Get the chosen school’s coords
row   = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]

# ─── STEP 4: HAVERSINE DISTANCE & FILTER ────────────────────────────────
def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

addresses["distance"] = addresses.apply(
    lambda r: haversine(slon, slat, r["lon"], r["lat"]), axis=1
)
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & DOWNLOAD ─────────────────────────────────────────
st.markdown(f"**Found {len(within)} addresses** within **{radius_mi} mi** of **{selected}**")

if not within.empty:
    # Map preview
    map_df = within.rename(columns={"lat":"latitude","lon":"longitude"})
    st.map(map_df[["latitude", "longitude"]])

    # Downloadable CSV
    out = within[["address","lon","lat","distance"]].rename(
        columns={"lon":"longitude","lat":"latitude"}
    )
    csv = out.to_csv(index=False)
    st.download_button(
        "⬇️ Download Mailing List",
        data=csv,
        file_name=f"{selected.replace(' ','_')}_{radius_mi}mi.csv",
        mime="text/csv"
    )
else:
    st.info("No addresses found in that buffer.")
