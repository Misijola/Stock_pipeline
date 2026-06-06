import pandas as pd

# Load the data we already fetched
df = pd.read_csv("stock_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["symbol", "date"])

# --- MOVING AVERAGES ---
# A moving average smooths out price fluctuations
# 7-day MA = average of last 7 days closing price
# 30-day MA = average of last 30 days closing price

df["ma_7"] = df.groupby("symbol")["close"].transform(
    lambda x: x.rolling(window=7).mean()
)

df["ma_30"] = df.groupby("symbol")["close"].transform(
    lambda x: x.rolling(window=30).mean()
)

# --- DAILY RETURN ---
# How much did the stock gain or lose each day in %
df["daily_return"] = df.groupby("symbol")["close"].pct_change() * 100

# --- TOP GAINERS AND LOSERS ---
# Get the most recent closing price for each stock
latest = df.groupby("symbol").last().reset_index()
latest = latest[["symbol", "close", "daily_return"]]
latest = latest.sort_values("daily_return", ascending=False)

print("=== TOP GAINERS / LOSERS (Most Recent Day) ===")
print(latest.to_string(index=False))

# --- PORTFOLIO PERFORMANCE ---
# Simulate owning 10 shares of each stock
latest["shares_owned"] = 10
latest["position_value"] = latest["close"] * latest["shares_owned"]
total_portfolio_value = latest["position_value"].sum()

print(f"\n=== PORTFOLIO VALUE ===")
print(latest[["symbol", "close", "shares_owned", "position_value"]].to_string(index=False))
print(f"\nTotal Portfolio Value: ${total_portfolio_value:,.2f}")

# Save transformed data
df.to_csv("stock_data_transformed.csv", index=False)
latest.to_csv("portfolio_summary.csv", index=False)
print("\nSaved transformed data to stock_data_transformed.csv")
print("Saved portfolio summary to portfolio_summary.csv")