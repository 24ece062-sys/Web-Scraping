from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_imdb():
    driver = setup_driver()

    print("Opening IMDb...")
    driver.get("https://www.imdb.com/chart/top/")

    time.sleep(150)

    print("Finding movie links...")

    # Find links to IMDb movie pages
    movie_links = driver.find_elements(
        By.CSS_SELECTOR,
        'a[href*="/title/tt"]'
    )

    print("Movie links found:", len(movie_links))

    data = []

    seen = set()

    for link in movie_links:

        try:
            title = link.text.strip()
            href = link.get_attribute("href")

            # Ignore empty links
            if not title:
                continue

            # Avoid duplicate movie links
            if href in seen:
                continue

            seen.add(href)

            # Get parent/container text
            parent = link.find_element(
                By.XPATH,
                "./ancestor::li[1]"
            )

            text = parent.text.strip()

            print("\nMovie:")
            print(text)

            # Find year directly from IMDB data
            year_match = re.search(r'(?<!\d)((?:19|20)\d{2})', text)
            if year_match:
                year = year_match.group()
            else:
                year = "N/A"

            # Find rating
            rating_match = re.search(
                r"\b([0-9]\.[0-9])\b",
                text
            )

            rating = (
                rating_match.group(1)
                if rating_match
                else "N/A"
            )

            data.append({
                "Rank": len(data) + 1,
                "Title": title,
                "Year": year,
                "Rating": rating
            })

            # Test only first 5
            if len(data) == 250:
                break

        except Exception as e:
            print("Error:", e)

    driver.quit()

    print("\nTotal data collected:", len(data))

    return data

def save_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("imdb_top_250.csv", index=False)
    print("CSV file created successfully!")

def save_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("imdb_top_250.xlsx", index=False)
    print("Excel file created successfully!")

if __name__ == "__main__":
    print("Scraping started...")
    movies = scrape_imdb()
    save_csv(movies)
    save_excel(movies)
    print("Done!")