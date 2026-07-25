# WEATHER_PROJECT.py
import streamlit as st
import pandas as pd
import mysql.connector import connect
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import warnings
import os
import sqlite3
warnings.filterwarnings('ignore')

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2c8cce;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection functions
@st.cache_resource
def connect_to_mysql():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="fari",
            database="weather_db"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None

# Database setup - Using SQLite for cloud deployment
@st.cache_resource
def init_database():
    """Initialize SQLite database and create table if not exists"""
    db_path = "weather_data.db"
    
    # Check if database exists, if not create and populate with sample data
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                City TEXT,
                Date TEXT,
                Temperature_C REAL,
                Humidity_Percentage REAL,
                Wind_Speed_kmh REAL,
                Weather_Condition TEXT
            )
        ''')
        
        # Insert sample data
        sample_data = [
            ('Madurai', '2024-01-15', 22.5, 65.0, 15.2, 'Sunny'),
            ('Chennai', '2024-01-16', 20.0, 70.0, 18.5, 'Cloudy'),
            ('Nellore', '2024-01-17', 18.5, 75.0, 20.0, 'Rainy'),
            ('Kanchipuram', '2024-01-18', 21.0, 68.0, 16.0, 'Partly Cloudy'),
            ('Tamil Nadu', '2024-01-19', 23.0, 62.0, 14.0, 'Sunny'),
            ('Bhopal', '2024-01-20', 19.5, 72.0, 19.0, 'Cloudy'),
            ('Anantapur', '2024-01-15', 18.0, 75.0, 20.5, 'Cloudy'),
            ('Mumbai', '2024-01-16', 16.5, 80.0, 22.0, 'Rainy'),
            ('Hyderabad', '2024-01-17', 19.0, 70.0, 18.0, 'Partly Cloudy'),
            ('Trichy', '2024-01-18', 17.0, 78.0, 21.0, 'Cloudy'),
            ('Panta', '2024-01-19', 20.0, 68.0, 17.5, 'Sunny'),
            ('Kochin', '2024-01-20', 18.5, 72.0, 19.5, 'Partly Cloudy'),
            ('Madurai', '2024-01-15', 25.0, 60.0, 12.0, 'Clear'),
            ('Trichy', '2024-01-16', 23.5, 65.0, 14.0, 'Sunny'),
            ('Hyderabad', '2024-01-17', 24.0, 62.0, 11.5, 'Clear'),
            ('Madurai', '2024-01-18', 26.0, 58.0, 10.0, 'Sunny'),
            ('Chennai', '2024-01-19', 22.0, 68.0, 13.5, 'Cloudy'),
            ('Nellore', '2024-01-20', 24.5, 60.0, 12.5, 'Clear'),
            ('Kanchipuram', '2024-01-15', 20.0, 70.0, 18.0, 'Partly Cloudy'),
            ('Tamil Nadu', '2024-01-16', 19.0, 72.0, 19.5, 'Cloudy'),
            ('Bhopal', '2024-01-17', 21.0, 68.0, 17.0, 'Sunny'),
            ('Anantapur', '2024-01-18', 18.0, 75.0, 20.0, 'Rainy'),
            ('Mumbai', '2024-01-19', 22.0, 65.0, 16.5, 'Sunny'),
            ('Hyderabad', '2024-01-20', 20.5, 68.0, 18.5, 'Partly Cloudy'),
            ('Trichy', '2024-01-15', 30.0, 55.0, 10.0, 'Sunny'),
            ('Chennai', '2024-01-16', 28.5, 58.0, 12.0, 'Clear'),
            ('Mumbai', '2024-01-17', 29.0, 56.0, 11.0, 'Sunny'),
            ('Patna', '2024-01-18', 31.0, 52.0, 9.0, 'Sunny'),
            ('Tamil Nadu', '2024-01-19', 27.0, 62.0, 13.0, 'Partly Cloudy'),
            ('Kerala', '2024-01-20', 29.5, 55.0, 11.5, 'Clear')
        ]
        
        cursor.executemany('''
            INSERT INTO weather_data (City, Date, Temperature_C, Humidity_Percentage, Wind_Speed_kmh, Weather_Condition)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()
    
    return db_path

def execute_query(query, params=None):
    """Execute a query and return results as DataFrame"""
    db_path = init_database()
    conn = sqlite3.connect(db_path)
    
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ Error executing query: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_cities():
    """Get list of unique cities"""
    query = "SELECT DISTINCT City FROM weather_data ORDER BY City"
    df = execute_query(query)
    return df["City"].tolist() if not df.empty else []

def get_weather_data(city=None, date_start=None, date_end=None, month=None):
    """Fetch weather data with filters"""
    query = "SELECT * FROM weather_data WHERE 1=1"
    params = []
    
    if city:
        query += " AND City = ?"
        params.append(city)
    
    if date_start and date_end:
        query += " AND Date BETWEEN ? AND ?"
        params.extend([date_start, date_end])
    
    if month:
        query += " AND CAST(strftime('%m', Date) AS INTEGER) = ?"
        params.append(month)
    
    return execute_query(query, params=tuple(params) if params else None)

# Main Application
def main():
    # Sidebar Navigation
    st.sidebar.markdown("# 🌦️ Weather Explorer")
    st.sidebar.markdown("---")
    
    # Initialize database
    init_database()
    
    # Get cities for filters
    cities = get_cities()
    
    if not cities:
        st.warning("⚠️ No cities found in database. Please check your data.")
        return
    
    page = st.sidebar.radio(
        "📋 Navigate",
        ["🏠 Home", "📊 Visualizations", "📈 Analytics", "💾 SQL Queries", "ℹ️ About"],
        index=0
    )
    
    if page == "🏠 Home":
        home_page(cities)
    elif page == "📊 Visualizations":
        visualization_page(cities)
    elif page == "📈 Analytics":
        analytics_page(cities)
    elif page == "💾 SQL Queries":
        sql_queries_page()
    elif page == "ℹ️ About":
        about_page()

def home_page(cities):
    """Home page with overview"""
    st.markdown("<h1 class='main-header'>🌦️ Weather Data Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Get summary statistics
    try:
        df_stats = execute_query("SELECT COUNT(*) as total_records, COUNT(DISTINCT City) as total_cities FROM weather_data")
        
        if not df_stats.empty:
            total_records = df_stats['total_records'].iloc[0]
            total_cities = df_stats['total_cities'].iloc[0]
            
            avg_temp = execute_query("SELECT AVG(Temperature_C) as avg_temp FROM weather_data")
            max_temp = execute_query("SELECT MAX(Temperature_C) as max_temp FROM weather_data")
            min_temp = execute_query("SELECT MIN(Temperature_C) as min_temp FROM weather_data")
            
            with col1:
                st.metric("📊 Total Records", f"{total_records:,}")
            with col2:
                st.metric("🏙️ Cities Covered", total_cities)
            with col3:
                avg_val = avg_temp['avg_temp'].iloc[0] if not avg_temp.empty else 0
                st.metric("🌡️ Average Temperature", f"{avg_val:.1f}°C")
            with col4:
                min_val = min_temp['min_temp'].iloc[0] if not min_temp.empty else 0
                max_val = max_temp['max_temp'].iloc[0] if not max_temp.empty else 0
                st.metric("📈 Temperature Range", f"{min_val:.1f}°C - {max_val:.1f}°C")
    except Exception as e:
        st.warning(f"Could not fetch statistics: {e}")
    
    st.markdown("---")
    
    # Show sample data
    st.subheader("📋 Sample Weather Data")
    sample_df = execute_query("SELECT * FROM weather_data LIMIT 5")
    if not sample_df.empty:
        st.dataframe(sample_df, use_container_width=True)
    
    # Quick filters
    st.subheader("🔍 Quick Search")
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Select City", ["All"] + cities)
    with col2:
        date_range = st.date_input("Date Range", [])
    
    if st.button("🔍 Search Data"):
        if selected_city != "All" and date_range:
            df = get_weather_data(
                city=selected_city if selected_city != "All" else None,
                date_start=date_range[0] if date_range else None,
                date_end=date_range[1] if len(date_range) > 1 else None
            )
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No data found for selected criteria")

def visualization_page(cities):
    """Visualization page"""
    st.subheader("📊 Weather Visualizations")
    
    if not cities:
        st.warning("No cities found in database.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_city = st.selectbox("🌆 Select City", cities, key="vis_city")
    with col2:
        date_start = st.date_input("📅 Start Date", datetime.now().date(), key="vis_start")
    with col3:
        date_end = st.date_input("📅 End Date", datetime.now().date(), key="vis_end")
    
    # Ensure date range is valid
    if date_start > date_end:
        st.error("Start date cannot be after end date!")
        return
    
    # Fetch data
    df = get_weather_data(
        city=selected_city,
        date_start=date_start.strftime("%Y-%m-%d"),
        date_end=date_end.strftime("%Y-%m-%d")
    )
    
    if df.empty:
        st.warning("No data available for selected filters. Please try different dates.")
        return
    
    st.success(f"✅ Found {len(df)} records for {selected_city}")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "💧 Humidity", "💨 Wind", "🌧️ Conditions"])
    
    with tab1:
        st.subheader("Temperature Trends")
        
        # Convert Date to datetime if it's not already
        df['Date'] = pd.to_datetime(df['Date'])
        
        fig1 = px.line(df, x="Date", y="Temperature_C", 
                       title=f"Temperature Trend in {selected_city}",
                       labels={"Temperature_C": "Temperature (°C)", "Date": ""})
        fig1.update_traces(marker=dict(size=8))
        st.plotly_chart(fig1, use_container_width=True)
        
        # Temperature statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Temperature", f"{df['Temperature_C'].mean():.1f}°C")
        with col2:
            st.metric("Max Temperature", f"{df['Temperature_C'].max():.1f}°C")
        with col3:
            st.metric("Min Temperature", f"{df['Temperature_C'].min():.1f}°C")
    
    with tab2:
        st.subheader("Humidity Analysis")
        
        fig2 = px.bar(df, x="Date", y="Humidity_Percentage",
                      title=f"Humidity Levels in {selected_city}",
                      labels={"Humidity_Percentage": "Humidity (%)", "Date": ""},
                      color="Humidity_Percentage",
                      color_continuous_scale="Blues")
        st.plotly_chart(fig2, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Humidity", f"{df['Humidity_Percentage'].mean():.1f}%")
        with col2:
            st.metric("Max Humidity", f"{df['Humidity_Percentage'].max():.1f}%")
    
    with tab3:
        st.subheader("Wind Speed Analysis")
        
        fig3 = px.scatter(df, x="Date", y="Wind_Speed_kmh",
                          title=f"Wind Speed in {selected_city}",
                          labels={"Wind_Speed_kmh": "Wind Speed (km/h)", "Date": ""},
                          size="Wind_Speed_kmh",
                          color="Wind_Speed_kmh",
                          color_continuous_scale="Viridis")
        st.plotly_chart(fig3, use_container_width=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Average Wind Speed", f"{df['Wind_Speed_kmh'].mean():.1f} km/h")
        with col2:
            st.metric("Max Wind Speed", f"{df['Wind_Speed_kmh'].max():.1f} km/h")
        with col3:
            st.metric("Min Wind Speed", f"{df['Wind_Speed_kmh'].min():.1f} km/h")
        with col4:
            st.metric("Wind Speed Std Dev", f"{df['Wind_Speed_kmh'].std():.1f} km/h")
        with col5:
            st.metric("Records Count", f"{len(df)}")
                
    
    with tab4:
        st.subheader("Weather Conditions Distribution")
        
        # Weather condition distribution
        weather_counts = df['Weather_Condition'].value_counts()
        if not weather_counts.empty:
            fig4 = px.pie(values=weather_counts.values, 
                          names=weather_counts.index,
                          title=f"Weather Conditions in {selected_city}")
            st.plotly_chart(fig4, use_container_width=True)
            
            # Show condition counts
            st.dataframe(weather_counts.reset_index().rename(columns={'index': 'Weather Condition', 0: 'Count'}))

def analytics_page(cities):
    """Advanced Analytics page"""
    st.subheader("📈 Advanced Weather Analytics")
    
    if not cities:
        st.warning("No cities found in database.")
        return
    
    # Multi-city comparison
    st.subheader("🏙️ Multi-City Comparison")
    selected_cities = st.multiselect("Select cities to compare", cities, default=cities[:2] if len(cities) >= 2 else cities)
    
    if selected_cities:
        df = get_weather_data()
        if not df.empty:
            df_filtered = df[df['City'].isin(selected_cities)]
            
            if not df_filtered.empty:
                # Temperature comparison
                fig1 = px.box(df_filtered, x="City", y="Temperature_C",
                              title="Temperature Distribution by City",
                              labels={"Temperature_C": "Temperature (°C)"},
                              color="City")
                st.plotly_chart(fig1, use_container_width=True)
                
                # Average metrics table
                st.subheader("📊 City Comparison Statistics")
                stats_df = df_filtered.groupby('City').agg({
                    'Temperature_C': ['mean', 'max', 'min', 'std'],
                    'Humidity_Percentage': ['mean', 'max', 'min'],
                    'Wind_Speed_kmh': ['mean', 'max']
                }).round(2)
                
                # Flatten column names
                stats_df.columns = [f'{col[0]}_{col[1]}' for col in stats_df.columns]
                stats_df = stats_df.reset_index()
                
                # Rename columns for better readability
                stats_df.columns = ['City', 'Avg Temp', 'Max Temp', 'Min Temp', 'Temp Std', 
                                   'Avg Humidity', 'Max Humidity', 'Min Humidity', 'Avg Wind', 'Max Wind']
                st.dataframe(stats_df, use_container_width=True)
            else:
                st.warning("No data available for selected cities")
    
    # Correlation Analysis
    st.subheader("🔗 Weather Parameter Correlations")
    df = get_weather_data()
    if not df.empty:
        # Calculate correlations
        numeric_cols = ['Temperature_C', 'Humidity_Percentage', 'Wind_Speed_kmh']
        corr_df = df[numeric_cols].corr()
        
        # Heatmap
        fig2 = px.imshow(corr_df, 
                        text_auto=True,
                        title="Correlation Matrix of Weather Parameters",
                        color_continuous_scale="RdBu_r")
        st.plotly_chart(fig2, use_container_width=True)

def sql_queries_page():
    """SQL Queries page"""
    st.subheader("💾 SQL Query Runner")
    
    # Predefined queries
    st.write("### 📋 Predefined Queries")
    predefined_queries = {
        "Average Temperature per City": "SELECT City, AVG(Temperature_C) AS Avg_Temperature, COUNT(*) as Records FROM weather_data GROUP BY City ORDER BY Avg_Temperature DESC",
        "Highest Humidity per City": "SELECT City, MAX(Humidity_Percentage) AS Max_Humidity FROM weather_data GROUP BY City ORDER BY Max_Humidity DESC",
        "Temperature Extremes": "SELECT City, MIN(Temperature_C) AS Min_Temp, MAX(Temperature_C) AS Max_Temp, (MAX(Temperature_C) - MIN(Temperature_C)) AS Temp_Range FROM weather_data GROUP BY City ORDER BY Temp_Range DESC",
        "Most Common Weather Conditions": "SELECT Weather_Condition, COUNT(*) AS Frequency FROM weather_data GROUP BY Weather_Condition ORDER BY Frequency DESC",
        "Wind Speed Analysis": "SELECT City, AVG(Wind_Speed_kmh) AS Avg_Wind, MAX(Wind_Speed_kmh) AS Max_Wind, MIN(Wind_Speed_kmh) AS Min_Wind FROM weather_data GROUP BY City ORDER BY Avg_Wind DESC"
    }
    
    selected_query_name = st.selectbox("Select a predefined query", list(predefined_queries.keys()))
    query = predefined_queries[selected_query_name]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.code(query, language="sql")
    with col2:
        if st.button("▶️ Run Query", use_container_width=True):
            result = execute_query(query)
            if not result.empty:
                st.success(f"✅ Query executed successfully! {len(result)} rows returned.")
                st.dataframe(result, use_container_width=True)
                
                # Download button
                csv = result.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No results returned from query")
    
    # Custom Query Runner
    st.write("### ✏️ Custom SQL Query")
    custom_query = st.text_area("Enter your SQL query:", height=100)
    
    if custom_query:
        if st.button("▶️ Run Custom Query", key="custom_query_btn"):
            try:
                result = execute_query(custom_query)
                if not result.empty:
                    st.success("✅ Query executed successfully!")
                    st.dataframe(result, use_container_width=True)
                    
                    # Download button
                    csv = result.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"custom_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("Query executed successfully but returned no results.")
            except Exception as e:
                st.error(f"❌ Error executing custom query: {e}")

def about_page():
    """About page"""
    st.markdown("<h1 class='main-header'>ℹ️ About This Project</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ## 🌦️ Weather Data Analysis Dashboard
    
    ### Project Overview
    This Streamlit application provides comprehensive weather data analysis and visualization capabilities.
    
    ### Features
    - **📊 Interactive Visualizations**: Dynamic charts for temperature, humidity, wind speed, and weather conditions
    - **🔍 Data Filtering**: Filter weather data by city, date range, and month
    - **📈 Advanced Analytics**: Multi-city comparison, correlation analysis, and statistical insights
    - **💾 SQL Query Runner**: Predefined and custom SQL queries for data exploration
    - **📥 Data Export**: Download query results as CSV files
    
    ### Technologies Used
    - **Python** - Core programming language
    - **Streamlit** - Web application framework
    - **SQLite** - Lightweight database
    - **Pandas** - Data manipulation and analysis
    - **Plotly** - Interactive visualizations
    - **Seaborn/Matplotlib** - Statistical visualizations
    
    ### Developer
    **Farith Ahamed**
    - **Skills**: Python, SQL, Data Analysis, Streamlit, Pandas
    """)

if __name__ == "__main__":
    main()
