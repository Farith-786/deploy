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
    
