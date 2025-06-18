import os
import math
import requests
import pandas as pd
import streamlit as st

# ─── STEP 1: DOWNLOAD CSVs FROM S3 VIA PRESIGNED URLs ────────────────────
DATA_URLS = {
    "schools.csv": (https://lausdbuffer.s3.us-east-2.amazonaws.com/schools.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIATTZC2PH6XJJQBH6P%2F20250618%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250618T172553Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCICVnnWlqPYPcNHe40zSzwCXHrXd60C52yIK%2BhIOrqv8tAiEA04PKyrpoLzinusz6J5Gf3d6HVykAf6awCegdb2JqTm8qqwIIk%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwyNDg2NDQyNzA1ODkiDOD9ikrdEIzMQ%2Fgp5Sr%2FARtboWaxm0tnMkhv0vh6IGeV5lXsObtvarWvz9qt6sqQXPZms4Oe9nWBaJAz3z7hEkkfqsfpnhmSGotM7m8c4GcVZ3JYhQSIONPKcjNFab3n74719cI1k2ce0Gb95x1ectgCkxSEdXqDvQPSQRpq7BDHJUIlwnX5nQxKVeH0zGozlT3YfclIuY%2BYKfNwjXk7jJyIuWDAhAJbFf63g3%2BCIuc1Uz1Kzw5Bh9K9Sk9K15ijt3hwG%2Brd6blWOEtXOcrUTAR%2BNjRqZW5okiz3Z7S0hLj5zAVdQZHAUtSw%2BU0Y0FByBQnjamtsmEypy%2FXt09f2qUbWwtoPVDyOaaaekUJC9zDZ5svCBjrfAbUl9YRc2U8n7WUZa4WrAkgB34izy8L%2BYxuq6zQoBYg5daLTdsnuooqV7lHNo7CgXke8ZOqbYVRQjPQl7sLWHg2jqstotyOaJlNL%2BQC0HwDqp18lBQMwv%2BpUMf8Tul0jAVeCwENqGnh8Zo2iSfTLk6qSt25bbwXMlWyoWi59xEmyVXDy6GUqCemA4D51G0PL6Gu149uJd5DBPZhDIm1OQ0kUI6pUV9p0UbOo8BuUDAlxSbbqs%2Fi3Q7onhwS09MIQriO8NZyIE7lojFEi1FPnjTiN2JFePDfRONQY4ZFGtBg%3D&X-Amz-Signature=01da5f4f07ce87443a9e905879a9d370ca8f85ed2fda8eade022867410caaa9e),
    "addresses.csv": (https://lausdbuffer.s3.us-east-2.amazonaws.com/addresses.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIATTZC2PH6XJJQBH6P%2F20250618%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250618T172554Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCICVnnWlqPYPcNHe40zSzwCXHrXd60C52yIK%2BhIOrqv8tAiEA04PKyrpoLzinusz6J5Gf3d6HVykAf6awCegdb2JqTm8qqwIIk%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwyNDg2NDQyNzA1ODkiDOD9ikrdEIzMQ%2Fgp5Sr%2FARtboWaxm0tnMkhv0vh6IGeV5lXsObtvarWvz9qt6sqQXPZms4Oe9nWBaJAz3z7hEkkfqsfpnhmSGotM7m8c4GcVZ3JYhQSIONPKcjNFab3n74719cI1k2ce0Gb95x1ectgCkxSEdXqDvQPSQRpq7BDHJUIlwnX5nQxKVeH0zGozlT3YfclIuY%2BYKfNwjXk7jJyIuWDAhAJbFf63g3%2BCIuc1Uz1Kzw5Bh9K9Sk9K15ijt3hwG%2Brd6blWOEtXOcrUTAR%2BNjRqZW5okiz3Z7S0hLj5zAVdQZHAUtSw%2BU0Y0FByBQnjamtsmEypy%2FXt09f2qUbWwtoPVDyOaaaekUJC9zDZ5svCBjrfAbUl9YRc2U8n7WUZa4WrAkgB34izy8L%2BYxuq6zQoBYg5daLTdsnuooqV7lHNo7CgXke8ZOqbYVRQjPQl7sLWHg2jqstotyOaJlNL%2BQC0HwDqp18lBQMwv%2BpUMf8Tul0jAVeCwENqGnh8Zo2iSfTLk6qSt25bbwXMlWyoWi59xEmyVXDy6GUqCemA4D51G0PL6Gu149uJd5DBPZhDIm1OQ0kUI6pUV9p0UbOo8BuUDAlxSbbqs%2Fi3Q7onhwS09MIQriO8NZyIE7lojFEi1FPnjTiN2JFePDfRONQY4ZFGtBg%3D&X-Amz-Signature=c1650512e4fb351f8fb24bb83ffa9711662f6a7ac5b1c623c58f5f4c35fa6a4b
    ),
}

for fname, url in DATA_URLS.items():
    if not os.path.exists(fname):
        with st.spinner(f"Downloading {fname}…"):
            resp = requests.get(url)
            resp.raise_for_status()
            with open(fname, "wb") as f:
                f.write(resp.content)

# ─── STEP 2: LOAD DATA ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Both CSVs are semicolon-delimited with headers: 
    #   schools.csv → label;lon;lat 
    #   addresses.csv → address;lon;lat
    schools = pd.read_csv("schools.csv", sep=";")
    addresses = pd.read_csv("addresses.csv", sep=";")
    return schools, addresses

schools, addresses = load_data()

# ─── STEP 3: APP UI ───────────────────────────────────────────────────────
st.title("📫 LAUSD Mailer (CSV Edition)")
st.markdown("Pick a school and buffer radius to generate your mailing list.")

selected = st.selectbox(
    "Select a School",
    schools["label"].sort_values().unique()
)
radius_mi = st.slider(
    "Buffer radius (miles)",
    min_value=0.25, max_value=2.0, value=0.5, step=0.25
)

# ─── STEP 4: DISTANCE CALCULATION ────────────────────────────────────────
def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))

# find coords of selected school
row = schools[schools["label"] == selected].iloc[0]
slon, slat = row["lon"], row["lat"]

# compute distances via list comprehension
dist_list = [
    haversine(slon, slat, float(r["lon"]), float(r["lat"]))
    for _, r in addresses.iterrows()
]
addresses["distance"] = dist_list

# filter by radius
within = addresses[addresses["distance"] <= radius_mi]

# ─── STEP 5: DISPLAY & EXPORT ────────────────────────────────────────────
st.markdown(
    f"**Found {len(within)} addresses** within **{radius_mi} miles** of **{selected}**"
)

if not within.empty:
    # Map preview (expects columns: latitude, longitude)
    map_df = within.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(map_df[["latitude", "longitude"]])

    # Prepare CSV download
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
