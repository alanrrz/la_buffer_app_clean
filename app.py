import os, math, requests
import pandas as pd
import streamlit as st

# ─── STEP 1: DOWNLOAD CLEAN CSVs FROM GOOGLE DRIVE ───────────────────────
def download_from_drive(file_id: str, dest: str):
    URL = "https://docs.google.com/uc?export=download"
    sess = requests.Session()
    res = sess.get(URL, params={"id": file_id}, stream=True)
    token = next((v for k,v in res.cookies.items() if k.startswith("download_warning")), None)
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

# ─── STEP 2: LOAD & STANDARDIZE ──────────────────────────────────────────
@st.cache_data
def load_data():
    # Load raw CSVs
    schools   = pd.read_csv("schools.csv")
    addresses = pd.read_csv("addresses.csv")

    # 1) Auto-detect school-name field (anything besides lon/lat)
    sch_cols = [c for c in schools.columns if c not in ("lon","lat")]
    if len(sch_cols) != 1:
        raise ValueError(f"Expected exactly one non-lon/lat column in schools.csv, got {sch_cols}")
    schools = schools.rename(columns={sch_cols[0]: "label"})

    # 2) Auto-detect address-text field in addresses.csv
    addr_cols = [c for c in addresses.columns if c not in ("lon","lat")]
    if len(addr_cols) != 1:
        raise ValueError(f"Expected exactly one non-lon/lat column in addresses.csv, got {addr_cols}")
    addresses = addresses.rename(columns={addr_cols[0]: "address"})

    return schools, addresses

schools, addresses = load_data()

# ─── STEP 3: APP UI ───────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Pick a school and buffer radius to generate your mailing list.")

names    = schools["label"].sort_values().unique()
selected = st.selectbox("Select a School", names)

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

# grab school coords
row       = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]

# compute distances into a plain list
dist_list = [
    haversine(slon, slat, float(r["lon"]), float(r["lat"]))
    for _, r in addresses.iterrows()
]
addresses["distance"] = dist_list

# filter by radius
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & DOWNLOAD ───────────────────────────────────────────
st.markdown(f"**Found {len(within)} addresses** within **{radius_mi} mi** of **{selected}**")

if not within.empty:
    map_df = within.rename(columns={"lat":"latitude","lon":"longitude"})
    st.map(map_df[["latitude","longitude"]])

    out = within[["address","lon","lat","distance"]].rename(
        columns={"lon":"longitude","lat":"latitude"}
    )
    st.download_button(
        "⬇️ Download Mailing List",
        data=out.to_csv(index=False),
        file_name=f"{selected.replace(' ','_')}_{radius_mi}mi.csv",
        mime="text/csv"
    )
else:
    st.info("No addresses found in that buffer.")
