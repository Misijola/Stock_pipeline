import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Load our secret API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# The 5 companies we're tracking
STOCKS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

def fetch_stock_data(symbol):
    """Fetch daily stock data for a given company symbol"""
    url = f"https://www.alphavantage.co/query"
    
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",  # last 100 days
        "apikey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract the daily price data
    time_series = data.get("Time Series (Daily)", {})
    
    rows = []
    for date, values in time_series.items():
        rows.append({
            "symbol": symbol,
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        })
    
    return rows

def fetch_all_stocks():
    """Loop through all 5 companies and collect their data"""
    all_data = []
    
    for symbol in STOCKS:
        print(f"Fetching data for {symbol}...")
        stock_data = fetch_stock_data(symbol)
        all_data.extend(stock_data)
    
    # Convert to a DataFrame (like an Excel table in Python)
    df = pd.DataFrame(all_data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["symbol", "date"])
    
    return df

# Run it
if __name__ == "__main__":
    df = fetch_all_stocks()
    print(df.head(20))
    print(f"\nTotal rows fetched: {len(df)}")
    
    # Save to CSV so we can inspect it
    df.to_csv("stock_data.csv", index=False)
    print("Saved to stock_data.csv")