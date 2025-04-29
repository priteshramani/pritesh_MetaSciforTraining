import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
import io

def scrape_real_estate_data(file_content):
    soup = BeautifulSoup(file_content, "html.parser")
    fullpanel = soup.find_all("div", class_="addressPanel flex justify-content-between align-items-center")

    data = [panel.text.strip() for panel in fullpanel]
    rows = []

    for item in data:
        beds = re.search(r'(\d+(?:\.\d+)?) Beds', item)
        baths = re.search(r'(\d+(?:\.\d+)?) Baths', item)
        sqft =  re.search(r'([\d,]+) sqft', item)
        address = item.split(' Beds')[0]

        beds_value = int(beds.group(1)[-1]) if beds else 'N/A'
        baths_value = baths.group(1) if baths else 'N/A'
        sqft_value = sqft.group(1) if sqft else 'N/A'
        address_value = address

        rows.append({'Beds': beds_value, 'Baths': baths_value, 'Sqft': sqft_value, 'Address': address_value})

    return pd.DataFrame(rows)

# Streamlit App
st.title("🏠 Real Estate Scraper")

uploaded_file = st.file_uploader("Upload the page_source.txt file", type="txt")

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    
    if st.button("Scrape Data"):
        df = scrape_real_estate_data(file_content)
        st.success("Scraping completed!")
        st.dataframe(df)

        # Convert to CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="meta.csv",
            mime="text/csv"
        )
