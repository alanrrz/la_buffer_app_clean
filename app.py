import streamlit as st
import pandas as pd
import numpy as np
import math
import folium
from streamlit_folium import st_folium

# 📄 Your schools file
SCHOOLS_URL = "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/ab73deb13c0a02107f43001161ab70891630a9c7/schools.csv"

# 🔷 ZipCode → CSV URL mapping
ZIPCODE_URLS = {
    90001: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90001.0.csv,
    90002: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90002.0.csv,
    90003: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90003.0.csv,
    90004: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90004.0.csv,
    90005: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90005.0.csv,
    90006: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90006.0.csv,
    90007: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90007.0.csv,
    90008: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90008.0.csv,
    90010: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90010.0.csv,
    90011: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90011.0.csv,
    90012: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90012.0.csv,
    90013: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90013.0.csv,
    90014: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90014.0.csv,
    90015: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90015.0.csv,
    90016: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90016.0.csv,
    90017: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90017.0.csv,
    90018: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90018.0.csv,
    90019: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90019.0.csv,
    90020: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90020.0.csv,
    90021: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90021.0.csv,
    90022: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90022.0.csv,
    90023: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90023.0.csv,
    90024: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90024.0.csv,
    90025: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90025.0.csv,
    90026: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90026.0.csv,
    90027: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90027.0.csv,
    90028: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90028.0.csv,
    90029: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90029.0.csv,
    90031: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90031.0.csv,
    90032: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90032.0.csv,
    90033: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90033.0.csv,
    90034: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90034.0.csv,
    90035: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90035.0.csv,
    90036: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90036.0.csv,
    90037: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90037.0.csv,
    90038: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90038.0.csv,
    90039: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90039.0.csv,
    90040: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90040.0.csv,
    90041: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90041.0.csv,
    90042: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90042.0.csv,
    90043: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90043.0.csv,
    90044: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90044.0.csv,
    90045: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90045.0.csv,
    90046: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90046.0.csv,
    90047: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90047.0.csv,
    90048: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90048.0.csv,
    90049: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90049.0.csv,
    90056: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90056.0.csv,
    90057: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90057.0.csv,
    90058: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90058.0.csv,
    90059: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90059.0.csv,
    90061: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90061.0.csv,
    90062: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90062.0.csv,
    90063: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90063.0.csv,
    90064: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90064.0.csv,
    90065: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90065.0.csv,
    90066: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90066.0.csv,
    90067: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90067.0.csv,
    90068: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90068.0.csv,
    90069: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90069.0.csv,
    90071: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90071.0.csv,
    90073: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90073.0.csv,
    90077: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90077.0.csv,
    90089: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90089.0.csv,
    90094: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90094.0.csv,
    90108: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90108.0.csv,
    90201: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90201.0.csv,
    90210: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90210.0.csv,
    90211: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90211.0.csv,
    90212: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90212.0.csv,
    90220: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90220.0.csv,
    90221: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90221.0.csv,
    90230: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90230.0.csv,
    90232: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90232.0.csv,
    90245: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90245.0.csv,
    90247: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90247.0.csv,
    90248: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90248.0.csv,
    90249: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90249.0.csv,
    90250: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90250.0.csv,
    90255: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90255.0.csv,
    90262: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90262.0.csv,
    90270: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90270.0.csv,
    90272: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90272.0.csv,
    90275: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90275.0.csv,
    90280: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90280.0.csv,
    90290: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90290.0.csv,
    90291: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90291.0.csv,
    90292: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90292.0.csv,
    90293: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90293.0.csv,
    90302: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90302.0.csv,
    90303: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90303.0.csv,
    90402: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90402.0.csv,
    90403: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90403.0.csv,
    90404: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90404.0.csv,
    90405: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90405.0.csv,
    90501: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90501.0.csv,
    90502: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90502.0.csv,
    90505: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90505.0.csv,
    90640: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90640.0.csv,
    90710: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90710.0.csv,
    90717: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90717.0.csv,
    90731: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90731.0.csv,
    90732: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90732.0.csv,
    90744: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90744.0.csv,
    90745: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90745.0.csv,
    90746: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90746.0.csv,
    90810: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90810.0.csv,
    91030: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91030.0.csv,
    91040: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91040.0.csv,
    91042: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91042.0.csv,
    91205: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91205.0.csv,
    91214: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91214.0.csv,
    91302: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91302.0.csv,
    91303: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91303.0.csv,
    91304: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91304.0.csv,
    91306: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91306.0.csv,
    91307: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91307.0.csv,
    91311: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91311.0.csv,
    91316: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91316.0.csv,
    91321: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91321.0.csv,
    91324: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91324.0.csv,
    91325: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91325.0.csv,
    91326: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91326.0.csv,
    91330: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91330.0.csv,
    91331: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91331.0.csv,
    91335: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91335.0.csv,
    91340: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91340.0.csv,
    91342: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91342.0.csv,
    91343: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91343.0.csv,
    91344: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91344.0.csv,
    91345: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91345.0.csv,
    91352: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91352.0.csv,
    91356: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91356.0.csv,
    91364: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91364.0.csv,
    91367: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91367.0.csv,
    91387: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91387.0.csv,
    91401: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91401.0.csv,
    91402: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91402.0.csv,
    91403: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91403.0.csv,
    91405: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91405.0.csv,
    91406: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91406.0.csv,
    91411: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91411.0.csv,
    91423: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91423.0.csv,
    91436: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91436.0.csv,
    91504: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91504.0.csv,
    91505: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91505.0.csv,
    91506: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91506.0.csv,
    91510: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91510.0.csv,
    91601: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91601.0.csv,
    91602: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91602.0.csv,
    91604: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91604.0.csv,
    91605: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91605.0.csv,
    91606: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91606.0.csv,
    91607: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91607.0.csv,
    91608: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91608.0.csv,
    91754: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91754.0.csv,
    91801: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91801.0.csv,
    91803: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91803.0.csv,
    92008: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/92008.0.csv,
    93063: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/93063.0.csv,
    97439: https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/97439.0.csv,

}

# 📄 Load schools
@st.cache_data
def load_schools():
    df = pd.read_csv(SCHOOLS_URL)
    df.columns = df.columns.str.strip()
    df["ZIPCODE"] = (
        df["ZIPCODE"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(5)
    )
    return df

# 📄 Load addresses file for a given URL
@st.cache_data
def load_addresses(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    return df

# 📄 Distance calculation
def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat/2)**2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon/2)**2
    )
    return 2 * R * math.asin(math.sqrt(a))


# 🌟 App title
st.title("📍 School Community Address Finder (by ZipCode)")
st.caption("Find addresses near your selected school site based on its ZipCode.")

schools = load_schools()
site_list = schools["LABEL"].sort_values().tolist()
site_selected = st.selectbox("Select Campus", site_list)

if site_selected:
    selected_school_row = schools[schools["LABEL"] == site_selected].iloc[0]
    school_zip = selected_school_row["ZIPCODE"]
    slon, slat = selected_school_row["LON"], selected_school_row["LAT"]

    st.write(f"📌 Selected School: **{site_selected}** (ZipCode: `{school_zip}`)")

    if school_zip not in ZIPCODE_URLS:
        st.error(f"No addresses file found for ZipCode: {school_zip}")
    else:
        addresses = load_addresses(ZIPCODE_URLS[school_zip])

        radius_selected = st.select_slider(
            "Select Radius (miles)",
            options=[round(x, 2) for x in np.arange(0.1, 3.01, 0.01)],
            value=0.5
        )

        if "show_map" not in st.session_state:
            st.session_state["show_map"] = False

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Preview Map"):
                st.session_state["show_map"] = True
        with col2:
            if st.button("Reset"):
                st.session_state["show_map"] = False

        if st.session_state["show_map"]:
            addresses["distance"] = addresses.apply(
                lambda r: haversine(slon, slat, r["LON"], r["LAT"]), axis=1
            )
            within = addresses[addresses["distance"] <= radius_selected]

            csv = within[["FullAddress"]].rename(columns={"FullAddress": "Address"}).to_csv(index=False)

            st.download_button(
                label=f"📥 Download Nearby Addresses ({site_selected}_{radius_selected}mi.csv)",
                data=csv,
                file_name=f"{site_selected.replace(' ', '_')}_{radius_selected}mi.csv",
                mime='text/csv'
            )

            fmap = folium.Map(location=[slat, slon], zoom_start=15)
            folium.Marker([slat, slon], tooltip=site_selected, icon=folium.Icon(color="blue")).add_to(fmap)
            folium.Circle([slat, slon], radius=radius_selected * 1609.34, color='red', fill=True, fill_opacity=0.1).add_to(fmap)

            st.write("### 📍 Map Preview")
            st.write("The red circle shows all addresses included in your download. Adjust your campus or radius as needed before downloading.")
            st_folium(fmap, width=700, height=500)
        else:
            st.info("Select campus and radius, then click 'Preview Map' to see results.")
