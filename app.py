import os
import math
import requests
import pandas as pd
import streamlit as st
import traceback

st.set_page_config(page_title="LAUSD Mailer (CSV Edition)")

try:
    # ─── STEP 1: DROPBOX LINKS ─────────────────────────────────────────────
    DATA_URLS = {
        "schools.csv": (
            "https://www.dropbox.com/scl/fi/qt5wmh9raabpjjykuvslt/schools.csv"
            "?rlkey=m7xtw0790sfv9djxz62h2ypzk&st=bt8qzi45&dl=1"
        ),
        "addresses.csv": (
            "https://www.dropbox.com/scl/fi/ika7darb79t1zbuzjpj90/addresses.csv"
            "?rlkey=h8anuof8jc4n70ynsrwd9svue&st=lafa9xe6&dl=1"
        ),
    }

    # download if missing
    for fname, url in DATA_URLS.items():
        if not os.path.exists(fname):
            with st.spinner(f"Downloading {fname}…"):
                resp = requests.get(url)
                resp.raise_for_status()
                with open(fname, "wb") as f:
                    f.write(resp.content)

    # ─── STEP 2: LOAD DATA ─────────────────────────────────────────────────
    @st.cache_data
    def load_data():
        # schools.csv is comma-delimited; addresses.csv is semicolon-delimited
        schools = pd.read_csv("schools.csv", sep=",")
        addresses = pd.read_csv("addresses.csv", sep=";")

        # normalize to lowercase
        schools.columns   = [c.strip().lower() for c in schools.columns]
        addresses.columns = [c.strip().lower() for c in addresses.columns]

        # ensure required columns exist
        for f, req in [("schools.csv", {"label","lon","lat"}),
                       ("addresses.csv", {"address","lon","lat"})]:
            missing = req - set((schools if f=="schools.csv" else addresses).columns)
            if missing:
                raise ValueError(f"{f} missing columns: {missing}")

        return schools, addresses

    schools, addresses = load_data()

    # ─── STEP 3: UI ────────────────────────────────────────────────────────
    st.title("📫 LAUSD Mailer (CSV Edition)")
    st.markdown("Pick a school and buffer radius to generate your mailing list.")

    selected  = st.selectbox("Select a School", schools["label"].sort_values().unique())
    radius_mi = st.slider("Buffer radius (miles)", 0.25, 2.0, 0.5, 0.25)

    # ─── STEP 4: DISTANCE ─────────────────────────────────────────────────
    def haversine(lon1, lat1, lon2, lat2):
        R = 3959
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

    addresses["distance"] = addresses.apply(
        lambda r: haversine(slon, slat, r["lon"], r["lat"]), axis=1
    )
    within = addresses[addresses["distance"] <= radius_mi]

    # ─── STEP 5: DISPLAY & EXPORT ─────────────────────────────────────────
    st.markdown(
        f"**Found {len(within)} addresses** within **{radius_mi} mile(s)** of **{selected}**"
    )

    if not within.empty:
        map_df = within.rename(columns={"lat": "latitude", "lon": "longitude"})
        st.map(map_df[["latitude", "longitude"]])

        out_csv = (
            within
            .rename(columns={"lon":"longitude","lat":"latitude"})
            [["address","longitude","latitude","distance"]]
            .to_csv(index=False)
        )
        st.download_button(
            "⬇️ Download Mailing List",
            data=out_csv,
            file_name=f"{selected.replace(' ', '_')}_{radius_mi}mi.csv",
            mime="text/csv",
        )
    else:
        st.info("No addresses found in that buffer.")

except Exception:
    st.error("❌ An error occurred:")
    st.text(traceback.format_exc())
    st.stop()
