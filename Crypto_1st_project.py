import streamlit as st
import pandas as pd



# Streamlit App Title
st.title("Crypto, Oil, and Stock Data Analysis")

#streamlit sidebar for navigation
page = st.sidebar.selectbox("🚀 Select a page", ["Home", "Data Overview", "SQL Queries", "Creator Info"])
# Display selected page content
st.write(f"You selected: {page}")
select_coin = st.sidebar.selectbox("Select a cryptocurrency", ["bitcoin", "ethereum", "solana"])

select_stock = st.sidebar.selectbox("Select a stock index", ["^GSPC", "^IXIC", "^NSEI"])

    
select_oil = st.sidebar.checkbox("Show latest oil price")

select_top_coins = st.sidebar.checkbox("Show top 5 cryptocurrencies by market cap")

        
    
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
