import os, math, requests
import pandas as pd
import streamlit as st
import numpy as np

# ─── STEP 1: DOWNLOAD CSVs FROM GOOGLE DRIVE ─────────────────────────────
import os, math, requests
import pandas as pd
import streamlit as st

# ─── STEP 1: DOWNLOAD CSVs FROM S3 VIA PRESIGNED URLs ───────────────────
DATA_URLS = {
    "schools.csv":   "https://lausdbuffer.s3.us-east-2.amazonaws.com/schools.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIATTZC2PH6XJJQBH6P%2F20250618%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250618T172553Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCICVnnWlqPYPcNHe40zSzwCXHrXd60C52yIK%2BhIOrqv8tAiEA04PKyrpoLzinusz6J5Gf3d6HVykAf6awCegdb2JqTm8qqwIIk%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwyNDg2NDQyNzA1ODkiDOD9ikrdEIzMQ%2Fgp5Sr%2FARtboWaxm0tnMkhv0vh6IGeV5lXsObtvarWvz9qt6sqQXPZms4Oe9nWBaJAz3z7hEkkfqsfpnhmSGotM7m8c4GcVZ3JYhQSIONPKcjNFab3n74719cI1k2ce0Gb95x1ectgCkxSEdXqDvQPSQRpq7BDHJUIlwnX5nQxKVeH0zGozlT3YfclIuY%2BYKfNwjXk7jJyIuWDAhAJbFf63g3%2BCIuc1Uz1Kzw5Bh9K9Sk9K15ijt3hwG%2Brd6blWOEtXOcrUTAR%2BNjRqZW5okiz3Z7S0hLj5zAVdQZHAUtSw%2BU0Y0FByBQnjamtsmEypy%2FXt09f2qUbWwtoPVDyOaaaekUJC9zDZ5svCBjrfAbUl9YRc2U8n7WUZa4WrAkgB34izy8L%2BYxuq6zQoBYg5daLTdsnuooqV7lHNo7CgXke8ZOqbYVRQjPQl7sLWHg2jqstotyOaJlNL%2BQC0HwDqp18lBQMwv%2BpUMf8Tul0jAVeCwENqGnh8Zo2iSfTLk6qSt25bbwXMlWyoWi59xEmyVXDy6GUqCemA4D51G0PL6Gu149uJd5DBPZhDIm1OQ0kUI6pUV9p0UbOo8BuUDAlxSbbqs%2Fi3Q7onhwS09MIQriO8NZyIE7lojFEi1FPnjTiN2JFePDfRONQY4ZFGtBg%3D&X-Amz-Signature=01da5f4f07ce87443a9e905879a9d370ca8f85ed2fda8eade022867410caaa9e",
    "addresses.csv": "https://lausdbuffer.s3.us-east-2.amazonaws.com/addresses.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIATTZC2PH6XJJQBH6P%2F20250618%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250618T172554Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCICVnnWlqPYPcNHe40zSzwCXHrXd60C52yIK%2BhIOrqv8tAiEA04PKyrpoLzinusz6J5Gf3d6HVykAf6awCegdb2JqTm8qqwIIk%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwyNDg2NDQyNzA1ODkiDOD9ikrdEIzMQ%2Fgp5Sr%2FARtboWaxm0tnMkhv0vh6IGeV5lXsObtvarWvz9qt6sqQXPZms4Oe9nWBaJAz3z7hEkkfqsfpnhmSGotM7m8c4GcVZ3JYhQSIONPKcjNFab3n74719cI1k2ce0Gb95x1ectgCkxSEdXqDvQPSQRpq7BDHJUIlwnX5nQxKVeH0zGozlT3YfclIuY%2BYKfNwjXk7jJyIuWDAhAJbFf63g3%2BCIuc1Uz1Kzw5Bh9K9Sk9K15ijt3hwG%2Brd6blWOEtXOcrUTAR%2BNjRqZW5okiz3Z7S0hLj5zAVdQZHAUtSw%2BU0Y0FByBQnjamtsmEypy%2FXt09f2qUbWwtoPVDyOaaaekUJC9zDZ5svCBjrfAbUl9YRc2U8n7WUZa4WrAkgB34izy8L%2BYxuq6zQoBYg5daLTdsnuooqV7lHNo7CgXke8ZOqbYVRQjPQl7sLWHg2jqstotyOaJlNL%2BQC0HwDqp18lBQMwv%2BpUMf8Tul0jAVeCwENqGnh8Zo2iSfTLk6qSt25bbwXMlWyoWi59xEmyVXDy6GUqCemA4D51G0PL6Gu149uJd5DBPZhDIm1OQ0kUI6pUV9p0UbOo8BuUDAlxSbbqs%2Fi3Q7onhwS09MIQriO8NZyIE7lojFEi1FPnjTiN2JFePDfRONQY4ZFGtBg%3D&X-Amz-Signature=c1650512e4fb351f8fb24bb83ffa9711662f6a7ac5b1c623c58f5f4c35fa6a4b"
}

for fname, url in DATA_URLS.items():
    if not os.path.exists(fname):
        with st.spinner(f"Downloading {fname}…"):
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
    # Read semicolon-delimited CSVs
    schools   = pd.read_csv("schools.csv",   sep=";")  # now gives columns ['label','lon','lat']
    addresses = pd.read_csv("addresses.csv", sep=";")  # now gives ['address','lon','lat']


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
