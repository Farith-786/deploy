import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Weather Data Analysis - India",
    page_icon="🌦️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to connect to MySQL database
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="fari",
            database="weather_db"
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Database Connection Error: {e}")
        return None

# Function to execute MySQL queries
def execute_query_mysql(query):
    conn = connect_to_mysql()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        return cursor
    except mysql.connector.Error as e:
        st.error(f"Query Execution Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Function to fetch data from MySQL and return as DataFrame
def get_data(query, params=None):
    conn = connect_to_mysql()
    if conn is None:
        return pd.DataFrame()
    
    try:
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        return df
    except mysql.connector.Error as e:
        st.error(f"Data Fetch Error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Function to create table if not exists (for reference)
def create_weather_table():
    query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        City VARCHAR(100),
        Date DATE,
        Temperature_C FLOAT,
        Humidity_Percentage FLOAT,
        Weather_Condition VARCHAR(100),
        Wind_Speed_kmh FLOAT,
        Precipitation_mm FLOAT
    )
    """
    execute_query_mysql(query)

# Function to insert sample data (optional - for demonstration)
def insert_sample_data():
    sample_data = [
        ("Mumbai", "2026-01-15", 28.5, 75, "Partly Cloudy", 15.0, 0.0),
        ("Delhi", "2026-01-15", 18.0, 60, "Clear", 10.0, 0.0),
        ("Bangalore", "2026-01-15", 24.0, 65, "Clear", 12.0, 0.0),
        ("Chennai", "2026-01-15", 30.0, 80, "Humid", 8.0, 0.0),
        ("Kolkata", "2026-01-15", 22.0, 70, "Foggy", 5.0, 0.0),
        ("Mumbai", "2026-01-16", 29.0, 78, "Partly Cloudy", 18.0, 0.5),
        ("Delhi", "2026-01-16", 19.0, 55, "Clear", 12.0, 0.0),
        ("Bangalore", "2026-01-16", 25.0, 60, "Clear", 14.0, 0.0),
    ]
    
    conn = connect_to_mysql()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        # Check if table has data
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        count = cursor.fetchall()[10]
        
        if count == 0:
            query = """
            INSERT INTO weather_data (City, Date, Temperature_C, Humidity_Percentage, 
                                    Weather_Condition, Wind_Speed_kmh, Precipitation_mm)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(query, sample_data)
            conn.commit()
            st.success("Sample data inserted successfully!")
    except mysql.connector.Error as e:
        st.warning(f"Sample data insertion skipped: {e}")
    finally:
        cursor.close()
        conn.close()

# Main application
def main():
    st.title("🌦️ Weather Data Analysis - India")
    st.markdown("---")
    
    # Sidebar Navigation
    st.sidebar.header("📌 Navigation")
    page = st.sidebar.radio(
        "Go to", 
        [
            "🏠 Project Introduction", 
            "📊 Weather Data Visualization", 
            "📋 SQL Queries", 
            "👩‍💻 Creator Information"
        ]
    )
    
    # Page 1: Project Introduction
    if page == "🏠 Project Introduction":
        st.subheader("📊 A Streamlit App for Exploring Weather Trends in India")
        st.write("""
        ### Welcome to the Weather Data Analysis App! 🌏
        
        This application provides comprehensive analysis of weather data from different cities across India 
        using a MySQL database.
        
        #### 📌 Features:
        - **Filter and explore** weather data by city, date, or month
        - **Dynamic visualizations** for temperature, humidity, and other weather parameters
        - **Predefined SQL queries** to gain insights from the data
        - **Interactive charts** using Plotly for better data exploration
        
        #### 🗄️ Database Information:
        - **Database:** `weather_db`
        - **Table:** `weather_data`
        - **Connection:** MySQL localhost
        
        #### 🔍 Key Metrics Tracked:
        - Temperature (°C)
        - Humidity (%)
        - Weather Conditions
        - Wind Speed (km/h)
        - Precipitation (mm)
        
        #### 🎯 Purpose:
        This project aims to help understand weather patterns across different Indian cities, 
        making it useful for travel planning, agricultural analysis, and climate studies.
        """)
        
        # Display sample statistics
        with st.expander("📊 Database Statistics"):
            try:
                total_query = "SELECT COUNT(*) as total_records FROM weather_data"
                total_df = get_data(total_query)
                if not total_df.empty:
                    st.metric("Total Records", total_df['total_records'].iloc[0])
                
                cities_query = "SELECT COUNT(DISTINCT City) as total_cities FROM weather_data"
                cities_df = get_data(cities_query)
                if not cities_df.empty:
                    st.metric("Total Cities", cities_df['total_cities'].iloc[0])
                
                date_range_query = "SELECT MIN(Date) as start_date, MAX(Date) as end_date FROM weather_data"
                date_df = get_data(date_range_query)
                if not date_df.empty and date_df['start_date'].iloc[0] is not None:
                    st.metric("Data Range", f"{date_df['start_date'].iloc[0]} to {date_df['end_date'].iloc[0]}")
            except Exception as e:
                st.warning("Could not fetch database statistics")
    
    # Page 2: Weather Data Visualization
    elif page == "📊 Weather Data Visualization":
        st.header("📊 Weather Data Visualizer")
        
        # Fetch cities and validate
        cities_query = "SELECT DISTINCT City FROM weather_data ORDER BY City"
        cities_df = get_data(cities_query)
        
        if cities_df.empty:
            st.warning("⚠️ No data available in the database. Please insert sample data or check your database connection.")
            if st.button("📥 Insert Sample Data"):
                create_weather_table()
                insert_sample_data()
                st.rerun()
            return
        
        cities = cities_df["City"].tolist()
        df = get_data("SELECT * FROM weather_data")
        if df.empty:
            st.warning("⚠️ No weather data available. Please check your database.")
            return
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Line Chart", "Bar Chart", "Area Chart", "Scatter Plot",
                "Multi-Line Chart", "Multi-Axis Chart"
            ],
            index=0
        )
        # Filters section
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🔍 Filters")
            selected_city = st.selectbox("🌆 Select City", cities)
            
            date_option = st.radio(
                "📅 Filter By:",
                ["Specific Day", "Entire Month", "Date Range", "All Data"],
            )
            
            if date_option == "Specific Day":
                selected_date = st.date_input("Choose a Date", datetime.now().date())
                query = "SELECT * FROM weather_data WHERE City = %s AND Date = %s"
                df = get_data(query, params=(selected_city, selected_date.strftime("%Y-%m-%d")))
                
            elif date_option == "Entire Month":
                selected_month = st.selectbox("📆 Select Month", range(1, 13), format_func=lambda x: datetime(2026, x, 1).strftime("%B"))
                selected_year = st.number_input("📅 Select Year", min_value=2000, max_value=2030, value=2026)
                query = "SELECT * FROM weather_data WHERE City = %s AND MONTH(Date) = %s AND YEAR(Date) = %s"
                df = get_data(query, params=(selected_city, selected_month, selected_year))
                
            elif date_option == "All Data":
                df = get_data("SELECT * FROM weather_data WHERE City = %s", params=(selected_city,))
            else:  # Date Range
                col1a, col2a = st.columns(2)
                with col1a:
                    start_date = st.date_input("Start Date", datetime.now().date())
                with col2a:
                    end_date = st.date_input("End Date", datetime.now().date())
                
                if start_date > end_date:
                    st.error("⚠️ Start date must be before end date!")
                    return
                
                query = "SELECT * FROM weather_data WHERE City = %s AND Date BETWEEN %s AND %s"
                df = get_data(query, params=(selected_city, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        
        with col2:
            if not df.empty:
                st.subheader("📈 Temperature Trends")
                
                # Create tabs for different visualizations
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Line Chart", "📉 Bar Chart", "🌡️ Humidity", "📊 All Metrics"])
                
                with tab1:
                    fig = px.line(df, x="Date", y="Temperature_C", 
                                 title=f"Temperature Trend - {selected_city}",
                                 labels={"Temperature_C": "Temperature (°C)", "Date": "Date"},
                                 markers=True)
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    fig = px.bar(df, x="Date", y="Temperature_C",
                                title=f"Temperature Distribution - {selected_city}",
                                labels={"Temperature_C": "Temperature (°C)"},
                                color="Temperature_C",
                                color_continuous_scale="Viridis")
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab3:
                    fig = px.line(df, x="Date", y="Humidity_Percentage",
                                 title=f"Humidity Trend - {selected_city}",
                                 labels={"Humidity_Percentage": "Humidity (%)", "Date": "Date"},
                                 markers=True,
                                 color_discrete_sequence=["green"])
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab4:
                    # Multiple metrics in one chart
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df["Date"], y=df["Temperature_C"], 
                                           mode="lines+markers", name="Temperature (°C)"))
                    fig.add_trace(go.Scatter(x=df["Date"], y=df["Humidity_Percentage"], 
                                           mode="lines+markers", name="Humidity (%)", yaxis="y2"))
                    
                    fig.update_layout(
                        title=f"Weather Metrics - {selected_city}",
                        xaxis_title="Date",
                        yaxis_title="Temperature (°C)",
                        yaxis2=dict(title="Humidity (%)", overlaying="y", side="right"),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Display raw data
                with st.expander("📊 View Raw Data"):
                    st.dataframe(df, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("📈 Summary Statistics")
                    col1s, col2s, col3s = st.columns(3)
                    with col1s:
                        st.metric("Avg Temperature", f"{df['Temperature_C'].mean():.1f}°C")
                    with col2s:
                        st.metric("Avg Humidity", f"{df['Humidity_Percentage'].mean():.1f}%")
                    with col3s:
                        st.metric("Avg Wind Speed", f"{df['Wind_Speed_kmh'].mean():.1f} km/h")
                
            else:
                st.warning("⚠️ No data available for the selected filters.")
                st.info("💡 Try selecting different dates or cities.")
    
    # Page 3: SQL Queries
    elif page == "📋 SQL Queries":
        st.header("📋 SQL Query Results")
        
        queries = {
            "1. Average Temperature per City": 
                "SELECT City, AVG(Temperature_C) AS Avg_Temperature FROM weather_data GROUP BY City ORDER BY Avg_Temperature DESC",
            
            "2. Highest Humidity per City": 
                "SELECT City, MAX(Humidity_Percentage) AS Max_Humidity FROM weather_data GROUP BY City ORDER BY Max_Humidity DESC",
            
            "3. Lowest Temperature Recorded": 
                "SELECT City, Date, Temperature_C AS Min_Temperature FROM weather_data ORDER BY Temperature_C ASC LIMIT 5",
            
            "4. Highest Temperature Recorded": 
                "SELECT City, Date, Temperature_C AS Max_Temperature FROM weather_data ORDER BY Temperature_C DESC LIMIT 5",
            
            "5. Average Wind Speed by City": 
                "SELECT City, AVG(Wind_Speed_kmh) AS Avg_Wind_Speed FROM weather_data GROUP BY City ORDER BY Avg_Wind_Speed DESC",
            
            "6. Most Common Weather Condition": 
                "SELECT Weather_Condition, COUNT(*) AS Frequency FROM weather_data GROUP BY Weather_Condition ORDER BY Frequency DESC LIMIT 5",
            
            "7. City with Most Records": 
                "SELECT City, COUNT(*) as Record_Count FROM weather_data GROUP BY City ORDER BY Record_Count DESC",
            
            "8. Monthly Averages per City": 
                "SELECT City, MONTH(Date) as Month, AVG(Temperature_C) as Avg_Temp, AVG(Humidity_Percentage) as Avg_Humidity FROM weather_data GROUP BY City, MONTH(Date) ORDER BY City, Month",
            
            "9. Weather Condition Summary": 
                "SELECT Weather_Condition, COUNT(*) as Total_Records, AVG(Temperature_C) as Avg_Temperature, AVG(Humidity_Percentage) as Avg_Humidity FROM weather_data GROUP BY Weather_Condition ORDER BY Total_Records DESC",
            
            "10. Daily Average Temperature": 
                "SELECT Date, AVG(Temperature_C) as Avg_Daily_Temperature FROM weather_data GROUP BY Date ORDER BY Date DESC LIMIT 10"
        }
        
        selected_query_name = st.selectbox("🔍 Choose a Query to Execute", list(queries.keys()))
        selected_query = queries[selected_query_name]
        
        # Show query
        with st.expander("📝 View SQL Query"):
            st.code(selected_query, language="sql")
        
        if st.button("▶️ Execute Query"):
            with st.spinner("Executing query..."):
                query_result = get_data(selected_query)
                
                if not query_result.empty:
                    st.success("✅ Query executed successfully!")
                    
                    # Show results
                    st.subheader("📊 Query Results")
                    st.dataframe(query_result, use_container_width=True)
                    
                    # Visualization based on query type
                    if "AVG" in selected_query_name and "City" in selected_query_name:
                        fig = px.bar(query_result, x="City", y=query_result.columns[1],
                                    title=selected_query_name,
                                    color=query_result.columns[1],
                                    color_continuous_scale="Viridis")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Query returned no results.")
    
    # Page 4: Creator Information
    else:
        st.header("👩‍💻 Creator Information")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://via.placeholder.com/200x200?text=Developer", use_column_width=True)
            st.background_color = "#f0f6f4"
        
        with col2:
            st.subheader("👋 Hello! I'm Farith Ahamed")
            st.write("""
            ### 📊 Data Analyst & Software Developer
            
            **🌟 Skills:**
            - 🐍 Python Programming
            - 🗄️ SQL Database Management
            - 📊 Data Analysis & Visualization
            - 🚀 Streamlit Web Apps
            - 🐼 Pandas & NumPy
            - 📈 Matplotlib & Seaborn
            
            **🌟 Developer:**
        - **Name:** Farith Ahamed
        - **Role:** Data Analyst & Software Developer
        - **Skills:** Python, SQL, Data Visualization, Streamlit
            
            **📚 Project Overview:**
            This Weather Data Analysis project demonstrates my ability to:
            - Build interactive data applications
            - Connect and query MySQL databases
            - Create meaningful visualizations
            - Handle real-world data scenarios
            
            **📧 Contact:**
            - GitHub: [FarithAhamed](https://github.com/FarithAhamed)
            - LinkedIn: [Farith Ahamed](https://linkedin.com/in/FarithAhamed)
            - Email: farith@Tech.Developer.com
            """)
        
        # Project statistics
        with st.expander("📊 Project Statistics"):
            try:
                stats_query = """
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT City) as total_cities,
                    MIN(Date) as earliest_date,
                    MAX(Date) as latest_date
                FROM weather_data
                """
                stats_df = get_data(stats_query)
                if not stats_df.empty:
                    col1s, col2s, col3s, col4s = st.columns(4)
                    col1s.metric("Total Records", stats_df['total_records'].iloc[0])
                    col2s.metric("Total Cities", stats_df['total_cities'].iloc[0])
                    col3s.metric("Earliest Date", stats_df['earliest_date'].iloc[0])
                    col4s.metric("Latest Date", stats_df['latest_date'].iloc[0])
            except:
                st.info("Connect to database to see statistics")

# Import plotly go for multi-axis charts
import plotly.graph_objects as go

if __name__ == "__main__":
    main()
