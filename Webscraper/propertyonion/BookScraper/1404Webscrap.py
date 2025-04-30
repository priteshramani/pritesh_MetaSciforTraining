import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Utility: Check if a URL is internal
def is_internal(link, base_url):
    return urlparse(link).netloc == urlparse(base_url).netloc or urlparse(link).netloc == ''

# Main scraping function (recursive)
def scrape_website(url, visited=None):
    if visited is None:
        visited = set()

    if url in visited:
        return ""

    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return f"\n[Error accessing {url}]: {str(e)}\n"

    content = f"\n\n--- Content from: {url} ---\n\n"
    content += soup.get_text(separator="\n", strip=True)

    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link['href'])
        if is_internal(full_url, url):
            content += scrape_website(full_url, visited)

    return content

# Save content to text file
def save_report(content, filename="report.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# Streamlit UI
st.set_page_config(page_title="Web Scraper", layout="centered")
st.title("Web Scraper with Report Generator")

st.write("Enter a website URL. This scraper will crawl the site and generate a downloadable text report from all internal pages.")

url = st.text_input("Enter Website URL", placeholder="https://books.toscrape.com")

if st.button("Start Scraping"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Scraping in progress..."):
            scraped_data = scrape_website(url)
            save_report(scraped_data)
            st.success("Scraping complete!")
            st.download_button(
                label="Download Report",
                data=scraped_data,
                file_name="website_report.txt",
                mime="text/plain"
            )
