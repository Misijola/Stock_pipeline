-- =============================================
-- STOCK MARKET ANALYTICS - SQL QUERIES
-- Stock Pipeline Project | EMIMO Portfolio
-- =============================================


-- -----------------------------------------------
-- QUERY 1: Latest closing price for each stock
-- -----------------------------------------------
SELECT 
    symbol,
    MAX(date) AS latest_date,
    close
FROM stocks
WHERE date = (SELECT MAX(date) FROM stocks WHERE symbol = symbol)
GROUP BY symbol, close
ORDER BY close DESC;


-- -----------------------------------------------
-- QUERY 2: 7-day and 30-day moving averages
-- (most recent values per stock)
-- -----------------------------------------------
SELECT
    symbol,
    date,
    close,
    ROUND(ma_7::numeric, 2) AS moving_avg_7day,
    ROUND(ma_30::numeric, 2) AS moving_avg_30day
FROM stocks
WHERE date = (SELECT MAX(date) FROM stocks WHERE symbol = symbol)
ORDER BY symbol;


-- -----------------------------------------------
-- QUERY 3: Top 5 gainers and losers
-- based on most recent daily return
-- -----------------------------------------------
SELECT
    symbol,
    ROUND(daily_return::numeric, 4) AS daily_return_pct,
    close,
    CASE 
        WHEN daily_return > 0 THEN 'GAINER'
        WHEN daily_return < 0 THEN 'LOSER'
        ELSE 'FLAT'
    END AS status
FROM stocks
WHERE date = (SELECT MAX(date) FROM stocks)
ORDER BY daily_return DESC;


-- -----------------------------------------------
-- QUERY 4: Portfolio total value
-- (JOIN between stocks and portfolio tables)
-- -----------------------------------------------
SELECT
    p.symbol,
    p.shares_owned,
    p.close AS current_price,
    p.position_value,
    ROUND(p.daily_return::numeric, 4) AS daily_return_pct
FROM portfolio p
ORDER BY position_value DESC;


-- -----------------------------------------------
-- QUERY 5: Window function - RANK stocks by 
-- best average closing price over all time
-- -----------------------------------------------
SELECT
    symbol,
    ROUND(AVG(close)::numeric, 2) AS avg_close,
    ROUND(MAX(close)::numeric, 2) AS all_time_high,
    ROUND(MIN(close)::numeric, 2) AS all_time_low,
    RANK() OVER (ORDER BY AVG(close) DESC) AS price_rank
FROM stocks
GROUP BY symbol
ORDER BY price_rank;


-- -----------------------------------------------
-- QUERY 6: Daily return volatility per stock
-- (standard deviation = how risky the stock is)
-- -----------------------------------------------
SELECT
    symbol,
    ROUND(STDDEV(daily_return)::numeric, 4) AS volatility,
    ROUND(AVG(daily_return)::numeric, 4) AS avg_daily_return,
    COUNT(*) AS trading_days
FROM stocks
WHERE daily_return IS NOT NULL
GROUP BY symbol
ORDER BY volatility DESC;


-- -----------------------------------------------
-- QUERY 7: Monthly average closing price
-- (aggregation by month)
-- -----------------------------------------------
SELECT
    symbol,
    DATE_TRUNC('month', date) AS month,
    ROUND(AVG(close)::numeric, 2) AS avg_monthly_close,
    ROUND(MAX(close)::numeric, 2) AS monthly_high,
    ROUND(MIN(close)::numeric, 2) AS monthly_low
FROM stocks
GROUP BY symbol, DATE_TRUNC('month', date)
ORDER BY symbol, month;