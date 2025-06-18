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

# ─── STEP 2: LOAD DATA ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    schools   = pd.read_csv("schools.csv")     # must have label,lon,lat
    addresses = pd.read_csv("addresses.csv")  # must have address,lon,lat
    return schools, addresses

schools, addresses = load_data()
st.write("Sample schools coords:", schools[["label","lon","lat"]].head(5))
st.write("Sample addresses coords:", addresses[["address","lon","lat"]].head(5))

# ─── STEP 3: APP UI ───────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Pick a school and buffer radius to generate your mailing list.")

# School selector
names    = schools["label"].sort_values().unique()
selected = st.selectbox("Select a School", names)

# Radius slider
radius_mi = st.slider("Radius (miles)", 0.25, 2.0, 0.5, 0.25)

# ─── STEP 4: DISTANCE CALCULATION ────────────────────────────────────────
# find selected school coords
row       = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]

# build a plain Python list of distances
dist_list = [
    haversine(slon, slat, float(r["lon"]), float(r["lat"]))
    for _, r in addresses.iterrows()
]

# assign the list and filter
addresses["distance"] = dist_list
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & EXPORT ────────────────────────────────────────────
st.markdown(f"**Found {len(within)} addresses** within **{radius_mi} mi** of **{selected}**")

if not within.empty:
    # map preview
    map_df = within.rename(columns={"lat":"latitude","lon":"longitude"})
    st.map(map_df[["latitude","longitude"]])

    # download list
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
