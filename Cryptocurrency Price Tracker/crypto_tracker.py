#importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
from datetime import datetime

#starting chrome webdriver
def start_driver(headless=False):
    """Configure and launch Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
def scrape_crypto(driver, limit=10):
    """Open CoinMarketCap and extract data for the top `limit` coins."""

#opening coinmarketcap & waiting for data
    driver.get("https://coinmarketcap.com/")
    # Wait for the table to actually load instead of a fixed sleep
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )
    time.sleep(100)  # small buffer for JS-rendered numbers to settle

#extracting top 10 cryptocurrency data
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    data = []
    for i, row in enumerate(rows[:limit], start=1):
        try:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            name = row.find_element(By.CSS_SELECTOR, "p[class*='coin-item-symbol']").text
            price = cells[3].text
            change = cells[4].text
            market_cap = cells[6].text
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#storing data with timestamp
            data.append({
                "Rank": i,
                "Coin": name,
                "Price": price,
                "24h Change": change,
                "Market Cap": market_cap,
                "Timestamp": timestamp
            })
        except Exception as e:
            print(f"Row {i} error:", e)
    return data
def save_csv(data, filename="crypto_prices.csv"):
    """Append the scraped data to a CSV file (creates it with headers if new)."""
    if not data:
        print("No data to save.")
        return

    #saving data to csv
    df = pd.DataFrame(data)
    file_exists = pd.io.common.file_exists(filename)
    df.to_csv(filename, mode="a", header=not file_exists, index=False)
    # Add 2 blank rows
    with open(filename, "a", newline="", encoding="utf-8") as file:
        file.write("\n")
        file.write("\n")
    print(f"Data saved to {filename}")
def filter_data(data, min_price=None, top_gainers=False):
    """Optional filtering: by minimum price and/or sorted by top gainers."""
    df = pd.DataFrame(data)
    if df.empty:
        print("No data scraped")
        return df

    df.columns = df.columns.str.strip()


#Filtering & Top gainners
    if min_price is not None:
        df["Price_Clean"] = (
            df["Price"].str.replace(r"[$,]", "", regex=True).astype(float)
        )
        df = df[df["Price_Clean"] >= min_price]

    if top_gainers:
        df["Change_Clean"] = (
            df["24h Change"].str.replace("%", "", regex=False).astype(float)
        )
        df = df.sort_values("Change_Clean", ascending=False)

    return df


if __name__ == "__main__":
    print("Scraping started...")
    print("Scraping started...")
    print("Starting Chrome browser...")

    driver = start_driver(headless=False)

    print("Chrome browser started successfully!") # set True to run without opening a window

    try:
        crypto_data = scrape_crypto(driver, limit=10)
        save_csv(crypto_data)
        filtered = filter_data(crypto_data, min_price=100)
        print(filtered[["Rank", "Coin", "Price", "24h Change"]])
    finally:
        driver.quit()
        print("Done!")