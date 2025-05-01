import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import WebDriverException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_page_source(url="https://propertyonion.com/property_search"):
    """
    Download the page source from the given URL using Selenium.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: The page source HTML content
        
    Raises:
        WebDriverException: If there's an error with the web driver
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        with st.spinner("Initializing web driver..."):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
        with st.spinner("Loading page..."):
            driver.get(url)
            time.sleep(5)  # Wait for the page to load
            page_source = driver.page_source
            
        driver.quit()
        return page_source
    except WebDriverException as e:
        logger.error(f"Error downloading page source: {str(e)}")
        st.error("Failed to download page source. Please check the URL and try again.")
        return None

def validate_scraped_data(row):
    """
    Validate the scraped data for each property.
    
    Args:
        row (dict): Dictionary containing property data
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    required_fields = ['Beds', 'Baths', 'Sqft', 'Address', 'Status', 'Listing Type', 'Date']
    return all(field in row and row[field] != 'N/A' for field in required_fields)

def scrape_real_estate_data(file_content):
    """
    Scrape real estate data from the HTML content.
    
    Args:
        file_content (str): HTML content to scrape
        
    Returns:
        pd.DataFrame: DataFrame containing the scraped data
    """
    if not file_content:
        return pd.DataFrame()
        
    soup = BeautifulSoup(file_content, "html.parser")
    addressbar = soup.find_all("div", class_="addressPanel flex justify-content-between align-items-center")
    datebar = soup.find_all("div", class_="infoBar flex justify-content-between px-1 pt-2 pb-2")

    rows = []
    total_properties = len(datebar)
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(total_properties):
        try:
            data = addressbar[i].text.strip()
            beds = re.search(r'(\d+(?:\.\d+)?) Beds', data)
            baths = re.search(r'(\d+(?:\.\d+)?) Baths', data)
            sqft = re.search(r'([\d,]+) sqft', data)
            address = data.split(' Beds')[0]

            beds_value = int(beds.group(1)[-1]) if beds else 'N/A'
            baths_value = baths.group(1) if baths else 'N/A'
            sqft_value = sqft.group(1) if sqft else 'N/A'
            address_value = address

            text = datebar[i].text.strip()
            match = re.match(r'^(\w+)\s+(.*?)(\d{2}/\d{2}/\d{4})$', text)
            if match:
                status = match.group(1).strip()
                listing = match.group(2).strip()
                date = match.group(3)
            else:
                status = 'N/A'
                listing = 'N/A'
                date = 'N/A'

            row = {
                'Beds': beds_value,
                'Baths': baths_value,
                'Sqft': sqft_value,
                'Address': address_value,
                'Status': status,
                'Listing Type': listing,
                'Date': date
            }

            if validate_scraped_data(row):
                rows.append(row)
            
            # Update progress
            progress = (i + 1) / total_properties
            progress_bar.progress(progress)
            status_text.text(f"Scraping property {i + 1} of {total_properties}")
            
        except Exception as e:
            logger.error(f"Error processing property {i + 1}: {str(e)}")
            continue

    progress_bar.empty()
    status_text.empty()
    return pd.DataFrame(rows)

# Streamlit UI
st.set_page_config(page_title="Property Onion Scraper", page_icon="🏠", layout="wide")
st.title("🏠 Property Onion Scraper")

# Add some helpful information
st.markdown("""
This tool helps you scrape real estate data from PropertyOnion.com. 
Enter a valid URL below to start scraping.
""")

# URL input with validation
url = st.text_input(
    "Enter PropertyOnion URL",
    placeholder="https://propertyonion.com/property_search",
    help="Enter a valid PropertyOnion URL to scrape data from"
)

if url:
    if not url.startswith("https://propertyonion.com/"):
        st.warning("Please enter a valid PropertyOnion URL")
    else:
        if st.button("Scrape Data", help="Click to start scraping data"):
            with st.spinner("Downloading page source..."):
                file_content = download_page_source(url)
                
            if file_content:
                with st.spinner("Scraping data..."):
                    df = scrape_real_estate_data(file_content)
                
                if not df.empty:
                    st.success(f"Successfully scraped {len(df)} properties!")
                    
                    # Display data
                    st.dataframe(df)
                    
                    # Download button
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="property_data.csv",
                        mime="text/csv",
                        help="Download the scraped data as a CSV file"
                    )
                else:
                    st.warning("No valid property data found on the page.")
    
