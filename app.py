import streamlit as st
import pandas as pd
import usaddress

st.title("🏠 US Address Parser")

st.write("Paste your addresses below (one per line):")

addresses = st.text_area("Addresses", height=200)

if st.button("Parse Addresses"):
    rows = []
    for line in addresses.splitlines():
        line = line.strip()
        try:
            parsed, _ = usaddress.tag(line)
            rows.append({
                "House Number": parsed.get("AddressNumber", ""),
                "Street": " ".join([
                    parsed.get("StreetNamePreDirectional", ""),
                    parsed.get("StreetName", ""),
                    parsed.get("StreetNamePostType", ""),
                    parsed.get("StreetNamePostDirectional", ""),
                ]).strip(),
                "City": parsed.get("PlaceName", ""),
                "State": parsed.get("StateName", ""),
                "ZIP": parsed.get("ZipCode", ""),
                "Original": line
            })
        except usaddress.RepeatedLabelError as e:
            rows.append({
                "House Number": "",
                "Street": "",
                "City": "",
                "State": "",
                "ZIP": "",
                "Original": line
            })

    df = pd.DataFrame(rows)
    st.write("### 📝 Parsed Addresses")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="parsed_addresses.csv",
        mime="text/csv"
    )
