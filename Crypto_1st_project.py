import streamlit as st
import pandas as pd

#function to connect to pymysql database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="fari",
        database="crypto_db"
    )


#function to execute SQL query and return results as a DataFrame
def get_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit App Title
st.title("Crypto, Oil, and Stock Data Analysis")

#streamlit sidebar for navigation
page = st.sidebar.selectbox("🚀 Select a page", ["Home", "Data Overview", "SQL Queries", "Creator Info"])

# Display selected page content
st.write(f"You selected: {page}")
select_coin = st.sidebar.selectbox("Select a cryptocurrency", ["bitcoin", "ethereum", "solana"])
if select_coin:
    query = f"""
    SELECT date, price_usd
    FROM crypto_prices
    WHERE coin_id = '{select_coin}'
    ORDER BY date DESC
    LIMIT 5;
    """
    df = get_data(query)
    st.subheader(f"Latest 5 Price Records for {select_coin.capitalize()}")
    st.dataframe(df)

select_stock = st.sidebar.selectbox("Select a stock index", ["^GSPC", "^IXIC", "^NSEI"])
if select_stock:
    query = f"""
    SELECT date, close
    FROM stock_prices
    WHERE ticker = '{select_stock}'
    ORDER BY date DESC
    LIMIT 5;
    """
    df = get_data(query)
    st.subheader(f"Latest 5 Closing Price Records for {select_stock}")
    st.dataframe(df)
    
select_oil = st.sidebar.checkbox("Show latest oil price")
if select_oil:
    query = """
    SELECT date, price_usd
    FROM oil_prices
    ORDER BY date DESC
    LIMIT 5;
    """
    df = get_data(query)
    st.subheader("Latest 5 Oil Price Records")
    st.dataframe(df)
    
select_top_coins = st.sidebar.checkbox("Show top 5 cryptocurrencies by market cap")
if select_top_coins:
    query = """
    SELECT name, symbol, market_cap
    FROM cryptocurrencies
    ORDER BY market_cap DESC
    LIMIT 5;
    """
    df = get_data(query)
    st.subheader("Top 5 Cryptocurrencies by Market Cap")
    st.dataframe(df)
        
    
select_overview = st.sidebar.checkbox("Show data overview")
if select_overview:
    st.subheader("Data Overview")
    st.write("Use the sidebar to navigate through datasets and analysis sections. You can also run custom SQL queries in the 'SQL Queries' section.")
    
if st.button("Run Query"):
    with st.spinner("Running query..."):
        df = get_data("SELECT * FROM cryptocurrencies LIMIT 5") # Execute a specific SQL query and return a DataFrame
        st.success("Query executed successfully!")
        st.dataframe(df)
        
st.write("Use the sidebar to navigate through datasets and analysis sections. You can also run custom SQL queries in the 'SQL Queries' section.")
st.dataframe(get_data("SELECT * FROM cryptocurrencies LIMIT 5")) # Example query to show some data on the home page

#predefined SQL Quries for selection
predefined_query = st.sidebar.selectbox("Select a predefined SQL query", [
    "Top 3 Cryptocurrencies by Market Cap",
    "Coins with Circulating Supply > 90% of Total Supply",
    "Coins Within 10% of ATH",
    "Average Market Cap Rank (Volume > $1B)",
    "Most Recently Updated Coin",
    "Highest Bitcoin Price in Last Year",
    "Average Ethereum Price in Last Year",
    "Coin with Highest Average Price in Last Year",
    "Percentage Change in Bitcoin Price Sep2024 to Sep2026",
    "Highest Oil Price in Last 5 Years",
    "Average Oil Price by Year",
    "Oil Prices During COVID-19 Crash",
    "Lowest Oil Price in Last 10 Years",
    "Oil Price Volatility by Year",
    "All S&P500 Stock Prices",
    "Highest Closing Price for NASDAQ",
    "Top 5 Days with Largest S&P500 Price Difference",
    "Average Monthly Closing Price for All Stocks",
    "Average Trading Volume for NSEI in 2024"
])

#dropdown to select predefined SQL query and display results
if predefined_query:
    query_mapping = {
        "Top 3 Cryptocurrencies by Market Cap": """
            SELECT name, symbol, market_cap
            FROM cryptocurrencies
            ORDER BY market_cap DESC
            LIMIT 3;
        """,
        "Coins with Circulating Supply > 90% of Total Supply": """
            SELECT name, symbol, circulating_supply, total_supply
            FROM cryptocurrencies
            WHERE total_supply IS NOT NULL
            AND circulating_supply >= (0.9 * total_supply);
        """,
        "Coins Within 10% of ATH": """
            SELECT name, symbol, current_price, ath
            FROM cryptocurrencies
            WHERE current_price >= (ath * 0.9);
        """,
        "Average Market Cap Rank (Volume > $1B)": """
            SELECT AVG(market_cap_rank) AS avg_rank
            FROM cryptocurrencies
            WHERE total_volume > 1000000000;
        """,
        "Most Recently Updated Coin": """
            SELECT id, name, symbol, date
            FROM cryptocurrencies
            ORDER BY date DESC
            LIMIT 1;
        """,
        "Highest Bitcoin Price in Last Year": """
            SELECT MAX(price_usd) AS highest_price
            FROM crypto_prices
            WHERE coin_id = 'bitcoin'
              AND date >= CURDATE() - INTERVAL 365 DAY;
        """,
        "Average Ethereum Price in Last Year": """
            SELECT ROUND(AVG(price_usd),2) AS avg_price
            FROM crypto_prices
            WHERE coin_id = 'ethereum'
              AND date >= CURDATE() - INTERVAL 365 DAY;
        """,
        "Coin with Highest Average Price in Last Year": """
            SELECT coin_id,
                   ROUND(AVG(price_usd),2) AS avg_price
            FROM crypto_prices
            WHERE date >= CURDATE() - INTERVAL 365 DAY
            GROUP BY coin_id
            ORDER BY avg_price DESC
            LIMIT 1;
        """,
        "Percentage Change in Bitcoin Price Sep2024 to Sep2026": """
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
                         AND YEAR(date)=2026
                         AND MONTH(date)=9)
                    ) / (SELECT AVG(price_usd)
                         FROM crypto_prices
                         WHERE coin_id='bitcoin'
                         AND YEAR(date)=2025
                         AND MONTH(date)=9) * 100 AS percentage_change
                FROM crypto_prices
                WHERE coin_id='bitcoin'
                  AND YEAR(date) IN (2025, 2026)
                  AND MONTH(date) = 9;
        """
    }

#backfround image and color for streamlit app     
st.background_color = "#440fa7"
st.background_image = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y3J5cHRvJTIwY29pbnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60"
  
        
#build SQL query based on input section
st.sidebar.subheader("Run Custom SQL Query")
user_query = st.sidebar.text_area("Enter your SQL query here")
if st.sidebar.button("Run Query"):
    if user_query.strip():
        try:
            result_df = get_data(user_query)
            st.subheader("Query Results")
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.warning("Please enter a valid SQL query.")

elif page == "Creator Info":
    st.title("Creator Information")
    st.markdown("""
    **Name:** Farith Ahamed
    **designation:** Software Engineer  
    **Email:** Farith.Tech.Software Engineer.com
    """)
