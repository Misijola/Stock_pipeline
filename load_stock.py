import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load database credentials from .env file
load_dotenv()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

# --- CREATE TABLES ---
# This is our PostgreSQL schema

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10),
        date DATE,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        volume BIGINT,
        ma_7 NUMERIC,
        ma_30 NUMERIC,
        daily_return NUMERIC
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10),
        close NUMERIC,
        shares_owned INTEGER,
        position_value NUMERIC,
        daily_return NUMERIC
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id SERIAL PRIMARY KEY,
        metric_name VARCHAR(50),
        metric_value NUMERIC,
        recorded_at TIMESTAMP DEFAULT NOW()
    );
""")

conn.commit()
print("Tables created successfully")

# --- LOAD STOCK DATA ---
df = pd.read_csv("stock_data_transformed.csv")
df["date"] = pd.to_datetime(df["date"])

# Clear old data before inserting fresh data
cursor.execute("DELETE FROM stocks;")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO stocks (symbol, date, open, high, low, close, volume, ma_7, ma_30, daily_return)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["symbol"],
        row["date"],
        row["open"],
        row["high"],
        row["low"],
        row["close"],
        row["volume"],
        None if pd.isna(row["ma_7"]) else row["ma_7"],
        None if pd.isna(row["ma_30"]) else row["ma_30"],
        None if pd.isna(row["daily_return"]) else row["daily_return"]
    ))

conn.commit()
print(f"Loaded {len(df)} rows into stocks table")

# --- LOAD PORTFOLIO DATA ---
portfolio = pd.read_csv("portfolio_summary.csv")

cursor.execute("DELETE FROM portfolio;")

for _, row in portfolio.iterrows():
    cursor.execute("""
        INSERT INTO portfolio (symbol, close, shares_owned, position_value, daily_return)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row["symbol"],
        row["close"],
        row["shares_owned"],
        row["position_value"],
        row["daily_return"]
    ))

conn.commit()
print("Loaded portfolio data")

# --- LOAD KEY METRICS ---
total_value = float(portfolio["position_value"].sum())

cursor.execute("DELETE FROM metrics;")
cursor.execute("""
    INSERT INTO metrics (metric_name, metric_value)
    VALUES (%s, %s)
""", ("total_portfolio_value", total_value))

conn.commit()
print("Loaded metrics")

cursor.close()
conn.close()
print("\nAll data loaded into PostgreSQL successfully")