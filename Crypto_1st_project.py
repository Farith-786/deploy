all_records = []
Records = []
import requests
import time

for page in range(1, 6):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page=250&order=market_cap_desc&page={page}&sparkline=False"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        all_records.extend(data)

        for i in data:
            Records.append({
                "Id": i.get("id"),
                "symbol": i.get("symbol"),
                "Name": i.get("name"),
                "Current_price": i.get("current_price"),
                "Market_cap": i.get("market_cap"),
                "Rank": i.get("market_cap_rank"),
                "Total_volume": i.get("total_volume"),
                "Circulating_supply": i.get("circulating_supply"),
                "Total_supply": i.get("total_supply"),
                "Ath": i.get("ath"),
                "Atl": i.get("atl"),
                "last_updated": (i.get("last_updated") or "")[:10]  # extract date only
            })

import pandas as pd
coins_df=pd.DataFrame(Records)
coins_df           
 
coins_df['last_updated'] = pd.to_datetime(coins_df['last_updated'])
coins_df['last_updated']

coins_df['Date'] = coins_df['last_updated'].dt.date
coins_df['Date']

coins_df.drop(columns=['last_updated'], inplace=True)
coins_df.head()

coins_df = coins_df.drop('Last_updated', axis=1, errors='ignore')
coins_df

coins_df.nsmallest(5, 'Rank')

coins_data=[]
coins_ids=['bitcoin','ethereum','tether','binancecoin','ripple']
for i in coins_ids:
  url=f"https://api.coingecko.com/api/v3/coins/{i}/market_chart?vs_currency=inr&days=365"
  response=requests.get(url)
  if response.status_code ==200:
    time.sleep(5)
    coins=response.json()
    prices = coins['prices']
    for ts, price in prices:
      coins_data.append({"coins_id": i,"date": pd.to_datetime(ts, unit='ms'),"price": price})
coinsPrice_df = pd.DataFrame(coins_data)
coinsPrice_df['date'] = coinsPrice_df['date'].dt.date
coinsPrice_df.head()

coinsPrice_df = coinsPrice_df.drop('date', axis=1, errors='ignore')
coinsPrice_df.head()

cols = coinsPrice_df.columns.tolist()
cols.insert(1, cols.pop(2))
coinsPrice_df = coinsPrice_df[cols]
coinsPrice_df.head()

import pandas as pd
oil_df=pd.read_csv("https://raw.githubusercontent.com/datasets/oil-prices/main/data/wti-daily.csv")
oil_df.head()

oil_df['Date'] = pd.to_datetime(oil_df['Date'])
start_date = pd.to_datetime('2020-01-01')
end_date   = pd.to_datetime('2026-04-29')

oil_df = oil_df[(oil_df['Date'] >= start_date) & (oil_df['Date'] <= end_date)]
oil_df['Date'] = oil_df['Date'].dt.date
oil_df.head()

import yfinance as yf
import pandas as pd
tickers=["^GSPC", "^IXIC", "^NSEI"]
start_date="2020-01-01"
end_date="2026-01-29"

stocks_df=yf.download(tickers,start=start_date,end=end_date,group_by='tickers')
stocks_df.head()

stocks1_df=stocks_df["^GSPC"].reset_index()
stocks1_df['Date'] = pd.to_datetime(stocks1_df['Date'])
stocks1_df = stocks1_df[(stocks1_df['Date'] >= start_date) & (stocks1_df['Date'] <= end_date)]
stocks1_df['Date'] = stocks1_df['Date'].dt.date
stocks1_df.head()

stocks1_df.insert(1, "Ticker", "^GSPC")
stocks1_df.head()
stocks2_df=stocks_df["^IXIC"].reset_index()
stocks2_df['Date'] = pd.to_datetime(stocks2_df['Date'])
stocks2_df = stocks2_df[(stocks2_df['Date'] >= start_date) & (stocks2_df['Date'] <= end_date)]
stocks2_df['Date'] = stocks2_df['Date'].dt.date

stocks1_df.isnull().sum()
stocks2_df.insert(1, "Ticker", "^IXIC")
stocks2_df.head()

stocks1_df=stocks1_df.dropna()
stocks1_df.head()
stocks2_df=stocks2_df.dropna()
stocks2_df.head()

stocks2_df=stocks_df["^IXIC"].reset_index()
stocks2_df.insert(1, "Ticker", "^IXIC")
stocks2_df.head()

stocks3_df=stocks_df["^NSEI"].reset_index()
stocks3_df['Date'] = pd.to_datetime(stocks3_df['Date'])
stocks3_df = stocks3_df[(stocks3_df['Date'] >= start_date) & (stocks3_df['Date'] <= end_date)]
stocks3_df['Date'] = stocks3_df['Date'].dt.date
stocks3_df.insert(1, "Ticker", "^NSEI")
stocks3_df.head()

stocks3_df.isnull().sum()
stocks3_df=stocks3_df.dropna()
stocks3_df.head()

Allstocks_df=pd.concat([stocks1_df,stocks2_df,stocks3_df])
Allstocks_df.isnull().sum()
Allstocks_df.head()

import mysql.connector

conn_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fari"
)
cursor_mysql = conn_mysql.cursor()
print("MySQL connection established!")

cursor_mysql.execute("CREATE DATABASE IF NOT EXISTS crypto_db")
cursor_mysql.execute("USE crypto_db")
print("MySQL database 'crypto_db' created successfully!")

cursor_mysql.execute("""
CREATE TABLE IF NOT EXISTS cryptocurrencies (
    id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(100),
    current_price DECIMAL(18,6),
    market_cap BIGINT,
    market_cap_rank INT,
    total_volume BIGINT,
    circulating_supply DECIMAL(20,6),
    total_supply DECIMAL(20,6),
    ath DECIMAL(18,6),
    atl DECIMAL(18,6),
    date DATE
)
""")
conn_mysql.commit()
print("Table 'cryptocurrencies' created successfully in MySQL!")
cursor_mysql.execute("USE crypto_db")

for _, row in coins_df.iterrows():
    # prepare insert query for cryptocurrencies if not already defined
    insert_query = """
    INSERT INTO cryptocurrencies (id, symbol, name, current_price, market_cap, market_cap_rank,
    total_volume, circulating_supply, total_supply, ath, atl, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor_mysql.execute(insert_query, (
        row['Id'], row['symbol'], row['Name'], row['Current_price'], row['Market_cap'],
        row['Rank'], row['Total_volume'], row['Circulating_supply'], row['Total_supply'],
        row['Ath'], row['Atl'], row['Date']
    ))
conn_mysql.commit()
print("Data inserted into 'cryptocurrencies' table successfully!")

cursor_mysql.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    coin_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    price_usd DECIMAL(18,6) NOT NULL,
    PRIMARY KEY (coin_id, date),
    FOREIGN KEY (coin_id) REFERENCES cryptocurrencies(id)
)
""")
conn_mysql.commit()
print("Table 'crypto_prices' created successfully!")

cursor_mysql.execute("""CREATE TABLE IF NOT EXISTS oil_prices (
    date DATE PRIMARY KEY,
    price_usd REAL NOT NULL
)""")
conn_mysql.commit()
print("Table 'oil_prices' created successfully!")

cursor_mysql.execute("""CREATE TABLE IF NOT EXISTS stock_prices (
    date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume BIGINT,
    ticker VARCHAR(50) NOT NULL,
    PRIMARY KEY (date, ticker)
);
""")
conn_mysql.commit()
print("Table 'stock_prices' created successfully!")

try:
    cursor_mysql.execute("""
    CREATE INDEX idx_stock_date
    ON stock_prices(date)
    """)
    conn_mysql.commit()
    print("Index 'idx_stock_date' created successfully!")
except mysql.connector.Error as err:
    if err.errno == 1061:
        print("Index 'idx_stock_date' already exists.")
    else:
        raise
conn_mysql.commit()

insert_query = """
INSERT INTO cryptocurrencies
(id, symbol, name, current_price, market_cap, market_cap_rank,
 total_volume, circulating_supply, total_supply, ath, atl, date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
symbol = VALUES(symbol),
name = VALUES(name),
current_price = VALUES(current_price),
market_cap = VALUES(market_cap),
market_cap_rank = VALUES(market_cap_rank),
total_volume = VALUES(total_volume),
circulating_supply = VALUES(circulating_supply),
total_supply = VALUES(total_supply),
ath = VALUES(ath),
atl = VALUES(atl),
date = VALUES(date)
"""

if 'cursor_mysql' not in globals() or 'conn_mysql' not in globals():
    import mysql.connector
    conn_mysql = mysql.connector.connect(host="localhost", user="root", password="fari")
    cursor_mysql = conn_mysql.cursor()

cursor_mysql.execute("USE crypto_db")
cursor_mysql.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    coin_id VARCHAR(50),
    date DATE,
    price_usd DECIMAL(18,6),
    PRIMARY KEY (coin_id, date),
    FOREIGN KEY (coin_id) REFERENCES cryptocurrencies(id)
)
""")
conn_mysql.commit()
print("Table 'crypto_prices' created successfully!")

conn_mysql.commit()
print("Table created successfully!")

query = """
INSERT OR REPLACE INTO crypto_prices (coin_id, date, price_usd)
VALUES (?, ?, ?)
"""

data = ("bitcoin", "2026-06-01", 105432.75)

cursor_mysql.execute("""
REPLACE INTO crypto_prices (coin_id, date, price_usd)
VALUES (%s, %s, %s)
""", data)
conn_mysql.commit()

print("Data inserted or replaced successfully!")

data = [
    ("bitcoin", "2026-06-01", 105432.75),
    ("ethereum", "2026-06-01", 3845.50),
    ("solana", "2026-06-01", 215.25)
]

cursor_mysql.executemany("""
REPLACE INTO crypto_prices (coin_id, date, price_usd)
VALUES (%s, %s, %s)
""", data)

conn_mysql.commit()

print("Multiple records inserted or replaced successfully!")

import pandas as pd

df = pd.DataFrame({
    'coin_id': ['bitcoin', 'ethereum', 'solana'],
    'date': ['2026-06-01', '2026-06-01', '2026-06-01'],
    'price_usd': [105432.75, 3845.50, 215.25]
})

records = df[['coin_id', 'date', 'price_usd']].values.tolist()

cursor_mysql.executemany("""
REPLACE INTO crypto_prices (coin_id, date, price_usd)
VALUES (%s, %s, %s)
""", records)

conn_mysql.commit()

print("DataFrame data inserted successfully!")

cursor_mysql.fetchall()
cursor_mysql.execute("SELECT * FROM crypto_prices")
rows = cursor_mysql.fetchall()

for row in rows:
    print(row)
    
if 'cursor_mysql' not in globals() or 'conn_mysql' not in globals():
    import mysql.connector
    conn_mysql = mysql.connector.connect(host="localhost", user="root", password="fari")
    cursor_mysql = conn_mysql.cursor()

cursor_mysql.execute("USE crypto_db")
conn = conn_mysql
cursor = cursor_mysql

# Create oil_prices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS oil_prices (
    date DATE PRIMARY KEY,
    price_usd REAL
)
""")

conn.commit()

print("Table created successfully!")

cursor.execute("""
INSERT INTO oil_prices (date, price_usd)
VALUES (%s, %s)
""", ('2025-05-31', 68.75))

conn.commit()

print("Data inserted successfully!")

oil_data = [
    ('2025-05-28', 67.20),
    ('2025-05-29', 68.10),
    ('2025-05-30', 69.50),
    ('2025-05-31', 68.75)
]

cursor.executemany("""
REPLACE INTO oil_prices (date, price_usd)
VALUES (%s, %s)
""", oil_data)

conn.commit()

print("Multiple records inserted successfully!")

import pandas as pd

df = pd.DataFrame({
    'date': ['2025-05-28', '2025-05-29', '2025-05-30'],
    'price_usd': [67.20, 68.10, 69.50]
})

oil_records = df[['date', 'price_usd']].values.tolist()

cursor.executemany("""
REPLACE INTO oil_prices (date, price_usd)
VALUES (%s, %s)
""", oil_records)

conn.commit()

print("DataFrame data inserted or replaced successfully!")

cursor.execute("SELECT * FROM oil_prices")

rows = cursor.fetchall()

for row in rows:
    print(row)
    
cursor = conn.cursor()

# Create stock_prices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_prices (
    date DATE,
    open DECIMAL(18,6),
    high DECIMAL(18,6),
    low DECIMAL(18,6),
    close DECIMAL(18,6),
    volume BIGINT,
    ticker VARCHAR(20),
    PRIMARY KEY (date, ticker)
)
""")
conn.commit();
print("Table created successfully!")

cursor.execute("USE crypto_db")

for row in Allstocks_df.itertuples(index=False):
    # skip rows with missing key fields
    if pd.isnull(row.Date) or pd.isnull(row.Ticker):
        continue

    cursor.execute("""
        REPLACE INTO stock_prices
        (date, open, high, low, close, volume, ticker)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row.Date.date() if hasattr(row.Date, "date") else row.Date,
        None if pd.isnull(row.Open) else float(row.Open),
        None if pd.isnull(row.High) else float(row.High),
        None if pd.isnull(row.Low) else float(row.Low),
        None if pd.isnull(row.Close) else float(row.Close),
        None if pd.isnull(row.Volume) else int(row.Volume),
        row.Ticker
    ))

conn.commit()

cursor = conn.cursor()

cursor.execute("SELECT * FROM stock_prices LIMIT 10")
rows = cursor.fetchall()

for row in rows:
    print(row)

print(Allstocks_df.head())
print(Allstocks_df.columns)

cursor.execute("USE crypto_db")
cursor.execute("SELECT * FROM stock_prices LIMIT 5")

rows = cursor.fetchall()

for row in rows:
    print(row)

import sys
try:
    from tabulate import tabulate
except ImportError:
    print("The 'tabulate' library is not installed. Please install it using 'pip install tabulate' and try again.")
    sys.exit(1)
query = """
SELECT name, symbol, market_cap
FROM cryptocurrencies
ORDER BY market_cap DESC
LIMIT 3;
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nTop 3 Cryptocurrencies by Market Cap")
print(tabulate(result,
               headers=["Name", "Symbol", "Market Cap"],
               tablefmt="grid"))

query = """
SELECT name, symbol, circulating_supply, total_supply
FROM cryptocurrencies
WHERE total_supply IS NOT NULL
AND circulating_supply >= (0.9 * total_supply);
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nCoins with Circulating Supply > 90% of Total Supply")
print(tabulate(result,
               headers=["Name", "Symbol", "Circulating Supply", "Total Supply"],
               tablefmt="grid"))

query = """
SELECT name, symbol, current_price, ath
FROM cryptocurrencies
WHERE current_price >= (ath * 0.9);
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nCoins Within 10% of ATH")
print(tabulate(result,
               headers=["Name", "Symbol", "Current Price", "ATH"],
               tablefmt="grid"))

query = """
SELECT AVG(market_cap_rank) AS avg_rank
FROM cryptocurrencies
WHERE total_volume > 1000000000;
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nAverage Market Cap Rank (Volume > $1B)")
print(tabulate(result,
               headers=["Average Rank"],
               tablefmt="grid"))

query = """
SELECT id, name, symbol, date
FROM cryptocurrencies
ORDER BY date DESC
LIMIT 1;
"""

cursor.execute(query)
result = cursor.fetchall()

print("\nMost Recently Updated Coin")
print(tabulate(result,
               headers=["ID", "Name", "Symbol", "Date"],
               tablefmt="grid"))

query = """
SELECT MAX(price_usd) AS highest_price
FROM crypto_prices
WHERE coin_id = 'bitcoin'
AND date >= CURDATE() - INTERVAL 365 DAY;
"""

cursor.execute(query)

result = cursor.fetchall()

print(tabulate(result,
               headers=["Highest Bitcoin Price"],
               tablefmt="grid"))

query = """
SELECT ROUND(AVG(price_usd),2) AS avg_price
FROM crypto_prices
WHERE coin_id = 'ethereum'
AND date >= CURDATE() - INTERVAL 365 DAY;
"""

cursor.execute(query)

result = cursor.fetchall()

print(tabulate(result,
               headers=["Average Ethereum Price"],
               tablefmt="grid"))

query = """
SELECT coin_id,
       ROUND(AVG(price_usd),2) AS avg_price
FROM crypto_prices
WHERE date >= CURDATE() - INTERVAL 365 DAY
GROUP BY coin_id
ORDER BY avg_price DESC
LIMIT 1;
"""

cursor.execute(query)

result = cursor.fetchall()

print(tabulate(result,
               headers=["Coin", "Average Price"],
               tablefmt="grid"))

query = """
SELECT
(
    (
        (SELECT AVG(price_usd)
         FROM crypto_prices
         WHERE coin_id='bitcoin'
         AND YEAR(date)=2025
         AND MONTH(date)=9)

        -

        (SELECT AVG(price_usd)
         FROM crypto_prices
         WHERE coin_id='bitcoin'
         AND YEAR(date)=2024
         AND MONTH(date)=9)
    )

    /

    (SELECT AVG(price_usd)
     FROM crypto_prices
     WHERE coin_id='bitcoin'
     AND YEAR(date)=2024
     AND MONTH(date)=9)

) * 100 AS percentage_change;
"""

cursor.execute(query)

result = cursor.fetchall()

print(tabulate(result,
               headers=["% Change Sep2024 to Sep2026"],
               tablefmt="grid"))

from tabulate import tabulate

query = """
SELECT MAX(price_usd) AS highest_oil_price
FROM oil_prices
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
"""

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(result,
               headers=["Highest Oil Price"],
               tablefmt="grid"))


query = """
SELECT
    YEAR(date) AS year,
    ROUND(AVG(price_usd), 2) AS average_price
FROM oil_prices
GROUP BY YEAR(date)
ORDER BY year;
"""

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(result,
               headers=["Year", "Average Oil Price"],
               tablefmt="grid"))


from tabulate import tabulate

query = """
SELECT
    date,
    price_usd
FROM oil_prices
WHERE date BETWEEN '2020-03-01' AND '2020-04-30'
ORDER BY date;
"""

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(result,
               headers=["Date", "Oil Price"],
               tablefmt="grid"))


from tabulate import tabulate

query = """
SELECT MIN(price_usd) AS lowest_oil_price
FROM oil_prices
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 10 YEAR);
"""

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(result,
               headers=["Lowest Oil Price"],
               tablefmt="grid"))


from tabulate import tabulate

query = """
SELECT
    YEAR(date) AS year,
    ROUND(MAX(price_usd) - MIN(price_usd), 2) AS volatility
FROM oil_prices
GROUP BY YEAR(date)
ORDER BY year;
"""

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(result,
               headers=["Year", "Volatility"],
               tablefmt="grid"))

query = """
SELECT *
FROM stock_prices
WHERE ticker = '^GSPC';
"""

cursor.execute(query)

rows = cursor.fetchall()

print(tabulate(rows, headers=[i[0] for i in cursor.description], tablefmt="grid"))

query = """
SELECT MAX(close) AS highest_closing_price
FROM stock_prices
WHERE ticker = '^IXIC';
"""

cursor.execute(query)

rows = cursor.fetchall()

print(tabulate(rows,
               headers=[i[0] for i in cursor.description],
               tablefmt="grid"))

query = """
SELECT
    date,
    high,
    low,
    (high - low) AS price_difference
FROM stock_prices
WHERE ticker = '^GSPC'
ORDER BY price_difference DESC
LIMIT 5;
"""

cursor.execute(query)

rows = cursor.fetchall()

print(tabulate(rows,
               headers=[i[0] for i in cursor.description],
   
               tablefmt="grid"))

query = """
SELECT
    ticker,
    YEAR(date) AS year,
    MONTH(date) AS month,
    ROUND(AVG(close), 2) AS avg_close_price
FROM stock_prices
GROUP BY ticker, YEAR(date), MONTH(date)
ORDER BY ticker, year, month;
"""

cursor.execute(query)

rows = cursor.fetchall()

print(tabulate(rows,
               headers=[i[0] for i in cursor.description],
               tablefmt="grid"))

query = """
SELECT
    ticker,
    ROUND(AVG(volume), 2) AS avg_trading_volume
FROM stock_prices
WHERE ticker = '^NSEI'
  AND YEAR(date) = 2024
GROUP BY ticker;
"""

cursor.execute(query)

rows = cursor.fetchall()

print(tabulate(rows,
               headers=[i[0] for i in cursor.description],
               tablefmt="grid"))

query = """
    SELECT
        sp.date,
        sp.close AS sp500_close,
        op.price_usd AS oil_price
    FROM stock_prices sp
    JOIN oil_prices op
        ON sp.date = op.date
    WHERE sp.ticker = '^GSPC'
    ORDER BY sp.date;
    """

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(
        result,
        headers=["Date", "S&P500 Close", "Oil Price"],
        tablefmt="grid"
    ))


query = """
SELECT
    sp.date,
    sp.close AS sp500_close,
    op.price_usd AS oil_price
FROM stock_prices sp
JOIN oil_prices op
    ON sp.date = op.date
WHERE sp.ticker = '^GSPC'
ORDER BY sp.date;
"""

cursor.execute(query)
result = cursor.fetchall()

print(tabulate(
    result,
    headers=["Date","S&P500","Oil Price"],
    tablefmt="grid"
))


import mysql.connector

conn_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fari"
)
cursor_mysql = conn_mysql.cursor()
print("MySQL connection established!")

cursor_mysql.execute("CREATE DATABASE IF NOT EXISTS crypto_db;")
print("MySQL database 'crypto_db' created successfully!")

cursor_mysql.execute("CREATE DATABASE IF NOT EXISTS crypto_db")
cursor_mysql.execute("USE crypto_db")

cursor_mysql.execute("""
CREATE TABLE IF NOT EXISTS cryptocurrencies (
    id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(100),
    current_price DECIMAL(18,6),
    market_cap BIGINT,
    market_cap_rank INT,
    total_volume BIGINT,
    circulating_supply DECIMAL(20,6),
    total_supply DECIMAL(20,6),
    ath DECIMAL(18,6),
    atl DECIMAL(18,6),
    date DATE
)
""")
conn_mysql.commit()
print("Table 'cryptocurrencies' created successfully in MySQL!")

cursor_mysql.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    coin_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    price_usd DECIMAL(18,6) NOT NULL,
    PRIMARY KEY (coin_id, date),
    FOREIGN KEY (coin_id) REFERENCES cryptocurrencies(id)
)
""")
conn_mysql.commit()
print("Table 'crypto_prices' created successfully!")

cursor_mysql.execute("""CREATE TABLE IF NOT EXISTS oil_prices (
    date DATE PRIMARY KEY,
    price_usd REAL NOT NULL
)""")
conn_mysql.commit()
print("Table 'oil_prices' created successfully!")

cursor_mysql.execute("""CREATE TABLE IF NOT EXISTS stock_prices (
    date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume BIGINT,
    ticker VARCHAR(50) NOT NULL,
    PRIMARY KEY (date, ticker)
);
""")
conn_mysql.commit()
print("Table 'stock_prices' created successfully!")

import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to MySQL database
def get_data(query, params=None):
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="fari",
        database="crypto_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Streamlit App Title
st.set_page_config(page_title="Crypto Data Analysis", layout="wide")


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "Crypto Data Visualization", "SQL Queries", "Creator Info"])
# Project Introduction Page
if page == "Project Introduction":
    st.header("Welcome to the Cryptocurrency Data Analysis Project!")
    st.markdown("""
    In this project, we will analyze cryptocurrency data using MySQL and Streamlit.
    We will explore various aspects of the data, including price trends, trading volumes, and correlations between different cryptocurrencies.
    """)
    st.title("Cryptocurrency Data Analysis Project")
    st.markdown("""
    This project aims to analyze cryptocurrency data using MySQL and Streamlit. 
    We will explore various aspects of the data, including price trends, trading volumes, and correlations between different cryptocurrencies.
    """)
    st.image("https://www.example.com/crypto_image.jpg", caption="Cryptocurrency Analysis")
# Crypto Data Visualization Page
elif page == "Crypto Data Visualization":
    st.title("Cryptocurrency Data Visualization")
    query = "SELECT date, price FROM crypto_prices WHERE crypto_name = 'Bitcoin' ORDER BY date"
    df = get_data(query)
    st.line_chart(df.set_index('date')['price'])
    st.subheader("Price Distribution")
    sns.histplot(df['price'], bins=30, kde=True)
    st.pyplot(plt)
# SQL Queries Page
elif page == "SQL Queries":
    st.title("SQL Queries")
    st.markdown("Here are some SQL queries used in this project:")
    st.code("""
    -- Query to get Bitcoin price data
    SELECT date, price 
    FROM crypto_prices 
    WHERE crypto_name = 'Bitcoin' 
    ORDER BY date;
    
    -- Query to get average trading volume for Ethereum
    SELECT AVG(trading_volume) 
    FROM crypto_prices 
    WHERE crypto_name = 'Ethereum';
    
    -- Query to get the top 5 cryptocurrencies by market cap
    SELECT crypto_name, market_cap 
    FROM crypto_prices 
    ORDER BY market_cap DESC 
    LIMIT 5;
    """, language='sql')
    
# Creator Info Page
elif page == "Creator Info":
    st.title("Creator Information")
    st.markdown("""
    **Name:** Farith Ahamed
    **designation:** Software Engineer  
    **Email:** Farith.Tech.Software Engineer.com
    """)
