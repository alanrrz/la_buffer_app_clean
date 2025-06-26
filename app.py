import streamlit as st
import pandas as pd
import numpy as np
import math
import folium
from streamlit_folium import st_folium

REGION_URLS = {
    "CENTRAL": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b0d5501614753fa530532c2f55a48eea4bed7607/C.csv",
    "EAST": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b0d5501614753fa530532c2f55a48eea4bed7607/E.csv",
    "NORTHEAST": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b0d5501614753fa530532c2f55a48eea4bed7607/NE.csv",
    "NORTHWEST": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b0d5501614753fa530532c2f55a48eea4bed7607/NW.csv",
    "SOUTH": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b0d5501614753fa530532c2f55a48eea4bed7607/S.csv",
    "WEST": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b0d5501614753fa530532c2f55a48eea4bed7607/W.csv"
}
SCHOOLS_URL = "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/b5a97acae47e218f836aba96d0dac1c8e3cacfda/school.csv"

@st.cache_data
def load_schools():
    return pd.read_csv(SCHOOLS_URL)

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

# App title and caption
st.title("School Community Address Finder")
st.caption("Find addresses near your selected school site for stakeholder notification and community engagement.")

# Load schools once at app start
schools = load_schools()
site_list = schools["label"].sort_values().tolist()
site_selected = st.selectbox("Select Campus", site_list)

if site_selected:
    # Find the school row and region
    selected_school_row = schools[schools["label"] == site_selected].iloc[0]
    school_region = selected_school_row["SHORTNAME"]

    # Defensive: handle missing region
    if school_region not in REGION_URLS:
        st.error(f"No addresses file found for region: {school_region}")
    else:
        # Only load the addresses for the selected region now!
        @st.cache_data
        def load_addresses(url):
            return pd.read_csv(url)

        addresses = load_addresses(REGION_URLS[school_region])

        radius_selected = st.select_slider(
            "Select Radius (How far from the school site?)",
            options = [round(x, 2) for x in np.arange(0.1, 3.01, 0.01)],
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
            slon, slat = selected_school_row["lon"], selected_school_row["lat"]
            radius = radius_selected

            addresses["distance"] = addresses.apply(
                lambda r: haversine(slon, slat, r["lon"], r["lat"]), axis=1
            )
            within = addresses[addresses["distance"] <= radius]
            csv = within[["address","lon","lat","distance"]].to_csv(index=False)

            st.download_button(
                label=f"Download Nearby Addresses ({site_selected}_{radius}mi.csv)",
                data=csv,
                file_name=f"{site_selected.replace(' ', '_')}_{radius}mi.csv",
                mime='text/csv'
            )

            fmap = folium.Map(location=[slat, slon], zoom_start=15)
            folium.Marker([slat, slon], tooltip=site_selected, icon=folium.Icon(color="blue")).add_to(fmap)
            folium.Circle([slat, slon], radius=radius*1609.34, color='red', fill=True, fill_opacity=0.1).add_to(fmap)

            st.write(f"**Preview:** The red area shows all addresses included in your download. Adjust your campus or radius as needed before downloading.")
            st_folium(fmap, width=700, height=500)
        else:
            st.info("Select campus and radius, then click 'Preview Map'.")
