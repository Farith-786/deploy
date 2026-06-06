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
