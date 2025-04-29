import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to fetch page source from URL
def download_page_source(url="https://propertyonion.com/property_search", delay=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(delay)
    page_source = driver.page_source
    driver.quit()
    return page_source

# Function to scrape the HTML content
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

# Streamlit UI
st.title("🏠 Property Onion Scraper")

# Section to download HTML
if st.button("Download Page Source"):
    html_content = download_page_source()
    st.success("Page source downloaded successfully!")

    st.download_button(
        label="📄 Download HTML File",
        data=html_content,
        file_name="page_source.txt",
        mime="text/plain"
    )

st.markdown("---")

# Upload and scrape
uploaded_file = st.file_uploader("Upload a page_source.txt file", type="txt")

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")

    if st.button("Scrape Data"):
        df = scrape_real_estate_data(file_content)
        st.success("Scraping completed!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="meta.csv",
            mime="text/csv"
        )
