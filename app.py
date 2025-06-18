import os, math, requests
import pandas as pd
import streamlit as st

# ─── STEP 1: DOWNLOAD CSVs ─────────────────────────────────────────────────
def download_from_drive(file_id: str, dest: str):
    URL = "https://docs.google.com/uc?export=download"
    sess = requests.Session()
    res = sess.get(URL, params={"id": file_id}, stream=True)
    token = next((v for k, v in res.cookies.items() if k.startswith("download_warning")), None)
    if token:
        res = sess.get(URL, params={"id": file_id, "confirm": token}, stream=True)
    with open(dest, "wb") as f:
        for chunk in res.iter_content(32768):
            if chunk:
                f.write(chunk)

DRIVE_FILES = {
    "addresses.csv": "1W0oqnxK26-EAsrSOBCt32wOonsA3LL8o",
    "schools.csv":   "1koPoihMbfQZWxBdfUMnkenUnMrruHie-"
}

for fname, fid in DRIVE_FILES.items():
    if not os.path.exists(fname):
        with st.spinner(f"Downloading {fname}..."):
            download_from_drive(fid, fname)

# ─── STEP 2: LOAD & STANDARDIZE ───────────────────────────────────────────
@st.cache_data
def load_data():
    # Read raw CSVs
    schools   = pd.read_csv("schools.csv")
    addresses = pd.read_csv("addresses.csv")

    # --- Normalize schools ---
    # find all non-coordinate columns
    sch_candidates = [c for c in schools.columns if c not in ("lon", "lat")]
    # prefer existing label/labels
    if "label" in schools.columns:
        schools.rename(columns={"label": "label"}, inplace=True)
    elif "labels" in schools.columns:
        schools.rename(columns={"labels": "label"}, inplace=True)
    elif len(sch_candidates) == 1:
        schools.rename(columns={sch_candidates[0]: "label"}, inplace=True)
    else:
        raise ValueError(f"Cannot find a single school name column, saw: {sch_candidates}")

    # --- Normalize addresses ---
    addr_candidates = [c for c in addresses.columns if c not in ("lon", "lat")]
    if "address" in addresses.columns:
        addresses.rename(columns={"address": "address"}, inplace=True)
    else:
        # look for any column containing 'FullAddress'
        fulls = [c for c in addr_candidates if "FullAddress" in c]
        if fulls:
            addresses.rename(columns={fulls[0]: "address"}, inplace=True)
        elif len(addr_candidates) == 1:
            addresses.rename(columns={addr_candidates[0]: "address"}, inplace=True)
        else:
            # fallback: pick first candidate
            addresses.rename(columns={addr_candidates[0]: "address"}, inplace=True)
    # drop any extra fields so we have exactly these three
    addresses = addresses[["address", "lon", "lat"]]

    return schools, addresses

# Load Data
schools, addresses = load_data()

# ─── STEP 3: UI ──────────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Pick a school and buffer radius to generate your mailing list.")

selected = st.selectbox(
    "Select a School",
    schools["label"].sort_values().unique()
)
radius_mi = st.slider("Radius (miles)", 0.25, 2.0, 0.5, 0.25)

# ─── STEP 4: DISTANCE CALCULATION ────────────────────────────────────────
def haversine(lon1, lat1, lon2, lat2):
    R = 3959
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return 2 * R * math.asin(math.sqrt(a))

# find coords of the chosen school
row = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]

# compute distances as a plain list
dist_list = [
    haversine(slon, slat, float(r["lon"]), float(r["lat"]))
    for _, r in addresses.iterrows()
]
addresses["distance"] = dist_list

# filter to within radius
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & EXPORT ────────────────────────────────────────────
st.markdown(f"**Found {len(within)} addresses** within **{radius_mi} mi** of **{selected}**")

if not within.empty:
    # map preview
    map_df = within.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(map_df[["latitude", "longitude"]])

    # prepare download
    out = within.rename(columns={"lon": "longitude", "lat": "latitude"})
    csv = out[["address", "longitude", "latitude", "distance"]].to_csv(index=False)

    st.download_button(
        "⬇️ Download Mailing List",
        data=csv,
        file_name=f"{selected.replace(' ','_')}_{radius_mi}mi.csv",
        mime="text/csv"
    )
else:
    st.info("No addresses found in that buffer.")
