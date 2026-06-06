all_records=[]
import requests
import time
import streamlit as st
for page in range (1,6):
  url=f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page=250&order=market_cap_desc&page={page}&sparkline=False"
  response = requests.get(url)
  if response.status_code == 200:
    data=response.json()
    all_records.extend(data)
len(all_records)
Records = []

for i in all_records:
    Records.append({
        "Id": i["id"],
        "symbol": i["symbol"],
        "Name": i["name"],
        "Current_price": i["current_price"],
        "Market_cap": i["market_cap"],
        "Rank": i["market_cap_rank"],
        "Total_volume": i["total_volume"],
        "Circulating_supply": i["circulating_supply"],
        "Total_supply": i["total_supply"],
        "Ath": i["ath"],
        "Atl": i["atl"],
        "last_updated": i["last_updated"].split("T")[0]   # 👈 extract date only
    })
import pandas as pd
coins_df=pd.DataFrame(Records)
coins_df
coins_df['last_updated'] = pd.to_datetime(coins_df['last_updated'])
coins_df['last_updated']
coins_df['Date'] = coins_df['last_updated'].dt.date
coins_df['Date']
coins_df
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
coinsPrice_df

coinsPrice_df = coinsPrice_df.drop('date', axis=1, errors='ignore')
coinsPrice_df

cols = coinsPrice_df.columns.tolist()
coinsPrice_df = coinsPrice_df[cols]
coinsPrice_df

import pandas as pd
oil_df=pd.read_csv("https://raw.githubusercontent.com/datasets/oil-prices/main/data/wti-daily.csv")
oil_df

oil_df

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
stocks1_df

cols = coinsPrice_df.columns.tolist()
coinsPrice_df = coinsPrice_df[cols]
coinsPrice_df

import pandas as pd
oil_df=pd.read_csv("https://raw.githubusercontent.com/datasets/oil-prices/main/data/wti-daily.csv")
oil_df

oil_df['Date'] = pd.to_datetime(oil_df['Date'])
start_date = pd.to_datetime('2020-01-01')
end_date   = pd.to_datetime('2026-04-29')

oil_df = oil_df[(oil_df['Date'] >= start_date) & (oil_df['Date'] <= end_date)]
oil_df

Allstocks_df=pd.concat([stocks1_df,stocks2_df,stocks3_df]) # pyright: ignore[reportUndefinedVariable]
Allstocks_df

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
    
