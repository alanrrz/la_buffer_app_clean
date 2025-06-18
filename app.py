import os, math, requests
import pandas as pd
import streamlit as st
import numpy as np

# ─── STEP 1: DOWNLOAD CSVs FROM GOOGLE DRIVE ─────────────────────────────
import os, math, requests
import pandas as pd
import streamlit as st

DATA_URLS = {
    "schools.csv":   "https://lausdbuffer.s3.us-east-2.amazonaws.com/schools.csv",
    "addresses.csv": "https://lausdbuffer.s3.us-east-2.amazonaws.com/addresses.csv"
}

for fname, url in DATA_URLS.items():
    if not os.path.exists(fname):
        with st.spinner(f"Downloading {fname} from S3…"):
            resp = requests.get(url)
            resp.raise_for_status()
            with open(fname, "wb") as f:
                f.write(resp.content)

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
    schools   = pd.read_csv("schools.csv")
    addresses = pd.read_csv("addresses.csv")

    # DEBUG: see what we actually have
    st.write("Addresses columns:", addresses.columns.tolist())
    st.write("Addresses dtypes:", addresses.dtypes.to_dict())

    # --- Normalize schools ---
    # detect non-numeric column as label
    sch_candidates = [c for c in schools.columns if not np.issubdtype(schools[c].dtype, np.number)]
    if "labels" in sch_candidates:
        schools = schools.rename(columns={"labels": "label"})
    elif "label" in sch_candidates:
        pass
    elif len(sch_candidates) == 1:
        schools = schools.rename(columns={sch_candidates[0]: "label"})
    else:
        raise ValueError(f"Cannot detect school name column, saw: {sch_candidates}")

    # detect and rename numeric coords
    num = [c for c in schools.columns if np.issubdtype(schools[c].dtype, np.number)]
    # assume first is lon, second is lat if not named
    if "xcoord" in num and "ycoord" in num:
        schools = schools.rename(columns={"xcoord": "lon", "ycoord": "lat"})
    elif "lon" in num and "lat" in num:
        pass
    elif len(num) >= 2:
        schools = schools.rename(columns={num[0]: "lon", num[1]: "lat"})
    else:
        raise ValueError(f"Cannot detect school coords columns, saw: {num}")

    # --- Normalize addresses ---
    # detect non-numeric col as address
    addr_candidates = [c for c in addresses.columns if not np.issubdtype(addresses[c].dtype, np.number)]
    if "FullAddress_EnerGov" in addr_candidates:
        addresses = addresses.rename(columns={"FullAddress_EnerGov": "address"})
    elif "address" in addr_candidates:
        pass
    elif len(addr_candidates) == 1:
        addresses = addresses.rename(columns={addr_candidates[0]: "address"})
    else:
        # pick first as fallback
        addresses = addresses.rename(columns={addr_candidates[0]: "address"})

    # detect numeric coord columns for addresses
    num2 = [c for c in addresses.columns if np.issubdtype(addresses[c].dtype, np.number)]
    if "xcoord" in num2 and "ycoord" in num2:
        addresses = addresses.rename(columns={"xcoord": "lon", "ycoord": "lat"})
    elif "lon" in num2 and "lat" in num2:
        pass
    elif len(num2) >= 2:
        addresses = addresses.rename(columns={num2[0]: "lon", num2[1]: "lat"})
    else:
        raise ValueError(f"Cannot detect address coords columns, saw: {num2}")

    # now slice exactly
    schools   = schools[["label","lon","lat"]]
    addresses = addresses[["address","lon","lat"]]

    return schools, addresses

schools, addresses = load_data()

# ─── STEP 3: APP UI ───────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Pick a school and buffer radius to generate your mailing list.")

selected = st.selectbox("Select a School", schools["label"].sort_values().unique())
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

row = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]
dist_list = [
    haversine(slon, slat, float(r["lon"]), float(r["lat"]))
    for _, r in addresses.iterrows()
]
addresses["distance"] = dist_list
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & EXPORT ────────────────────────────────────────────
st.markdown(f"**Found {len(within)} addresses** within **{radius_mi} miles** of **{selected}**")
if not within.empty:
    map_df = within.rename(columns={"lat":"latitude","lon":"longitude"})
    st.map(map_df[["latitude","longitude"]])
    out = within.rename(columns={"lon":"longitude","lat":"latitude"})
    csv = out[["address","longitude","latitude","distance"]].to_csv(index=False)
    st.download_button("⬇️ Download Mailing List", data=csv,
                       file_name=f"{selected.replace(' ','_')}_{radius_mi}mi.csv",
                       mime="text/csv")
else:
    st.info("No addresses found in that buffer.")
