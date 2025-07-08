import streamlit as st
import pandas as pd
import re

st.title("🏠 Address Parser")

st.write("Paste your addresses below (one per line):")

addresses = st.text_area("Addresses", height=200)

if st.button("Parse Addresses"):
    rows = []
    for line in addresses.splitlines():
        # crude regex for US address: number, street, city, zip
        # you can adjust this pattern depending on your data
        m = re.match(r"(\d+)\s+(.*?)\s+([A-Za-z\s]+)\s+(\d{5})$", line.strip())
        if m:
            house_num, street, city, zipcode = m.groups()
            rows.append({
                "House Number": house_num,
                "Street": street,
                "City": city,
                "ZIP": zipcode
            })
        else:
            rows.append({
                "House Number": "",
                "Street": "",
                "City": "",
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
