import streamlit as st
import pandas as pd
from mysql.connector import connect
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import mysql.connector

# Page configuration
st.set_page_config(
    page_title="Growth Population Analysis",
    page_icon="📊",
    layout="wide"
)

# Function to connect to MySQL database
def connect_to_mysql():
    try:
        return connect(
            host="localhost",
            user="root",
            password="fari",
            database="global_literacy"
        )
    except mysql.connector.Error as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

# Function to execute query and return results as DataFrame
def get_data(query, params=None):
    conn = connect_to_mysql()
    if conn is None:
        return pd.DataFrame()
    try:
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Error executing query: {e}")
        conn.close()
        return pd.DataFrame()

# Function to execute query without returning data
def execute_query(query):
    conn = connect_to_mysql()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Error executing query: {e}")
        conn.close()
        return False

# Create table if not exists
def create_tables():
    create_growth_table = """
    CREATE TABLE IF NOT EXISTS growth_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        City VARCHAR(100),
        Date DATE,
        Population INT,
        Growth_Rate FLOAT,
        Birth_Rate FLOAT,
        Death_Rate FLOAT,
        Migration_Rate FLOAT,
        UNIQUE KEY unique_record (City, Date)
    )
    """
    return execute_query(create_growth_table)

# Initialize tables
create_tables()

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #333;
        padding: 10px 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.radio(
    "Select Section",
    ["🏠 Home", "📈 Data Visualization", "🔍 SQL Queries", "👩‍💻 Creator Info"]
)

# Sidebar for data upload (Admin)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Data Management")
if st.sidebar.button("📤 Upload Sample Data"):
    # Insert sample data
    sample_data = [
        ("India", "2026-01-01", 8419600, 0.12, 11.2, 6.5, 3.2, 1000),
        ("India", "2026-02-01", 8423800, 0.14, 11.5, 6.3, 3.5, 1200),
        ("Chennai", "2026-01-01", 3980400, 0.08, 10.8, 7.2, 2.1, 800),
        ("Chennai", "2026-02-01", 3985400, 0.10, 11.0, 7.0, 2.3, 900),
        ("Chicago", "2026-01-01", 2716000, 0.05, 10.2, 8.1, 1.5, 600),
        ("Chicago", "2026-02-01", 2719000, 0.07, 10.4, 8.0, 1.7, 700)
    ]
    
    for data in sample_data:
        query = """
        INSERT INTO growth_data (City, Date, Population, Growth_Rate, Birth_Rate, Death_Rate, Migration_Rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        Population = VALUES(Population),
        Growth_Rate = VALUES(Growth_Rate),
        Birth_Rate = VALUES(Birth_Rate),
        Death_Rate = VALUES(Death_Rate),
        Migration_Rate = VALUES(Migration_Rate),
        child_Death_Rate = VALUES(child_Death_Rate)
        """
        conn = connect_to_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, data)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
    st.sidebar.success("✅ Sample data uploaded successfully!")

# --------------------- HOME PAGE ---------------------
if page == "🏠 Home":
    st.markdown('<div class="main-header">🌍 Growth Population Analysis</div>', unsafe_allow_html=True)
    
    # Get summary statistics
    total_cities = get_data("SELECT COUNT(DISTINCT City) as total FROM growth_data")
    total_records = get_data("SELECT COUNT(*) as total FROM growth_data")
    
    if not total_cities.empty and not total_records.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>🏙️</h2>
                <h3>{total_cities.iloc[0]['total']}</h3>
                <p>Total Cities</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2>📊</h2>
                <h3>{total_records.iloc[0]['total']}</h3>
                <p>Total Records</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Project Introduction
    st.markdown("### 📖 Project Introduction")
    st.markdown("""
    <div class="info-box">
        <h4>🎯 Project Overview</h4>
        <p>This project analyzes growth population data from different cities using MySQL database. 
        It provides comprehensive visualizations and insights into population trends, growth rates, 
        birth rates, and migration patterns.</p>
        
        <h4>⭐ Key Features</h4>
        <ul>
            <li>📊 Interactive data visualization with multiple chart types</li>
            <li>🔍 Advanced filtering by city, date range, and metrics</li>
            <li>📈 Pre-built SQL queries for data insights</li>
            <li>📥 Export data to CSV</li>
            <li>🎨 Beautiful and responsive UI</li>
        </ul>
        
        <h4>🗄️ Database Schema</h4>
        <ul>
            <li><b>growth_data</b> - City, Date, Population, Growth_Rate, Birth_Rate, Death_Rate, Migration_Rate</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --------------------- VISUALIZATION PAGE ---------------------
elif page == "📈 Data Visualization":
    st.markdown('<div class="main-header">📊 Growth Data Visualizer</div>', unsafe_allow_html=True)
    
    # Fetch city list
    cities_df = get_data("SELECT DISTINCT City FROM growth_data")
    if cities_df.empty:
        st.warning("⚠️ No data available. Please upload sample data using the button in the sidebar.")
        st.stop()
    
    cities = cities_df["City"].tolist()
    
    # Filters Section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🔍 Filters")
        selected_city = st.selectbox("📍 Select City", ["All Cities"] + cities)
        
        date_option = st.radio("📅 Date Filter", ["Specific Date", "Date Range", "All Data"])
        
        if date_option == "Specific Date":
            selected_date = st.date_input("Choose a Date", datetime.now().date())
            date_filter = f"Date = '{selected_date}'"
        elif date_option == "Date Range":
            start_date = st.date_input("Start Date", datetime.now().date())
            end_date = st.date_input("End Date", datetime.now().date())
            date_filter = f"Date BETWEEN '{start_date}' AND '{end_date}'"
        else:
            date_filter = "1=1"
    
    # Build query based on filters
    query = "SELECT * FROM growth_data"
    conditions = []
    
    if selected_city != "All Cities":
        conditions.append(f"City = '{selected_city}'")
    
    if date_filter:
        conditions.append(date_filter)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY Date"
    
    # Get data
    df = get_data(query)
    
    if df.empty:
        st.warning("⚠️ No data available for the selected filters.")
    else:
        st.success(f"✅ Found {len(df)} records")
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            avg_population = df['Population'].mean()
            st.metric("Average Population", f"{avg_population:,.0f}")
        with col2:
            avg_growth = df['Growth_Rate'].mean()
            st.metric("Average Growth Rate", f"{avg_growth:.2f}%")
        with col3:
            avg_birth = df['Birth_Rate'].mean()
            st.metric("Average Birth Rate", f"{avg_birth:.2f}‰")
        with col4:
            avg_migration = df['Migration_Rate'].mean()
            st.metric("Average Migration Rate", f"{avg_migration:.2f}‰")
        
        st.markdown("---")
        
        # Data Table
        st.markdown("### 📋 Data Table")
        st.dataframe(
            df.style.background_gradient(subset=['Growth_Rate'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Export button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="growth_data.csv",
            mime="text/csv"
        )
        
        # Visualization Section
        st.markdown("---")
        st.markdown("### 📈 Growth Trends")
        
        # Chart type selection
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot", "Multi-Line Chart", "Correlation Heatmap", "Box Plot", "Histogram", "Stacked Area Chart", "Dual Axis Chart"]
        )
        
        # Metrics to visualize
        metrics = st.multiselect(
            "Select Metrics to Visualize",
            ['Growth_Rate', 'Birth_Rate', 'Death_Rate', 'Migration_Rate', 'Population'],
            default=['Growth_Rate', 'Birth_Rate', 'Death_Rate', 'Migration_Rate']
        )
        
        if metrics:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            if chart_type == "Line Chart":
                for metric in metrics:
                    sns.lineplot(data=df, x='Date', y=metric, marker='o', label=metric)
            
            elif chart_type == "Bar Chart":
                df_grouped = df.groupby('Date')[metrics].mean().reset_index()
                df_grouped.plot(x='Date', kind='bar', ax=ax)
                plt.xticks(rotation=45)
            
            elif chart_type == "Area Chart":
                df.set_index('Date')[metrics].plot(kind='area', ax=ax)
            
            elif chart_type == "Scatter Plot":
                if len(metrics) >= 2:
                    sns.scatterplot(data=df, x=metrics[0], y=metrics[1], hue='City', size='Population', ax=ax)
                else:
                    st.warning("Please select at least 2 metrics for scatter plot")
            
            elif chart_type == "Multi-Line Chart":
                # Group by city and show trends
                for city in df['City'].unique():
                    city_data = df[df['City'] == city]
                    for metric in metrics:
                        sns.lineplot(data=city_data, x='Date', y=metric, marker='o', label=f"{city} - {metric}")
            elif chart_type == "Box Plot":
                sns.boxplot(data=df[metrics], ax=ax)
            elif chart_type == "Histogram":
                df[metrics].hist(bins=15, ax=ax)
            elif chart_type == "Stacked Area Chart":
                df.set_index('Date')[metrics].plot(kind='area', stacked=True, ax=ax)
            elif chart_type == "Dual Axis Chart":
                if len(metrics) >= 2:
                    ax2 = ax.twinx()
                    sns.lineplot(data=df, x='Date', y=metrics[0], marker='o', color='blue', ax=ax, label=metrics[0])
                    sns.lineplot(data=df, x='Date', y=metrics[1], marker='o', color='orange', ax=ax2, label=metrics[1])
                    ax.set_ylabel(metrics[0])
                    ax2.set_ylabel(metrics[1])
                else:
                    st.warning("Please select at least 2 metrics for dual axis chart")
                    
            plt.xlabel("Date")
            plt.ylabel("Value")
            plt.title(f"{chart_type} of {', '.join(metrics)}")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)
        
        # Correlation Heatmap
        st.markdown("### 🔥 Correlation Heatmap")
        if len(df) > 1:
            numeric_cols = ['Population', 'Growth_Rate', 'Birth_Rate', 'Death_Rate', 'Migration_Rate']
            corr_df = df[numeric_cols]
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_df.corr(), annot=True, cmap='coolwarm', center=0, ax=ax)
            st.pyplot(fig)

# --------------------- SQL QUERIES PAGE ---------------------
elif page == "🔍 SQL Queries":
    st.markdown('<div class="main-header">🔍 SQL Query Explorer</div>', unsafe_allow_html=True)
    
    queries = {
        "1. Population Trend by City": """
            SELECT 
                City,
                DATE_FORMAT(Date, '%Y-%m') as Month,
                AVG(Population) as Avg_Population,
                AVG(Growth_Rate) as Avg_Growth_Rate
            FROM growth_data
            GROUP BY City, DATE_FORMAT(Date, '%Y-%m')
            ORDER BY Month DESC, City;
        """,
        
        "2. Top 5 Cities by Growth Rate": """
            SELECT 
                City,
                AVG(Growth_Rate) as Avg_Growth_Rate,
                MAX(Population) as Current_Population
            FROM growth_data
            GROUP BY City
            ORDER BY Avg_Growth_Rate DESC
            LIMIT 5;
        """,
        
        "3. Monthly Population Summary": """
            SELECT 
                DATE_FORMAT(Date, '%Y-%m') as Month,
                COUNT(DISTINCT City) as Num_Cities,
                SUM(Population) as Total_Population,
                AVG(Growth_Rate) as Avg_Growth_Rate,
                AVG(Birth_Rate) as Avg_Birth_Rate,
                AVG(Death_Rate) as Avg_Death_Rate
            FROM growth_data
            GROUP BY DATE_FORMAT(Date, '%Y-%m')
            ORDER BY Month DESC;
        """,
        
        "4. Cities with Highest Migration": """
            SELECT 
                City,
                Date,
                Migration_Rate,
                Population
            FROM growth_data
            WHERE Migration_Rate = (
                SELECT MAX(Migration_Rate) 
                FROM growth_data
            )
            ORDER BY Date DESC;
        """,
        
        "5. Population Growth vs Birth Rate": """
            SELECT 
                City,
                AVG(Growth_Rate) as Avg_Growth_Rate,
                AVG(Birth_Rate) as Avg_Birth_Rate,
                AVG(Death_Rate) as Avg_Death_Rate,
                AVG(Migration_Rate) as Avg_Migration_Rate
            FROM growth_data
            GROUP BY City
            HAVING AVG(Growth_Rate) > 0
            ORDER BY Avg_Growth_Rate DESC;
        """,
        
        "6. Custom Query": """
            -- Write your custom query here
            SELECT * FROM growth_data LIMIT 10;
        """
    }
    
    selected_query = st.selectbox("📝 Select a Query", list(queries.keys()))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.code(queries[selected_query], language='sql')
    
    with col2:
        if st.button("▶️ Run Query", use_container_width=True):
            df = get_data(queries[selected_query])
            if not df.empty:
                st.success(f"✅ Query returned {len(df)} rows")
                st.dataframe(df, use_container_width=True)
                
                # Download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ No results found")

# --------------------- CREATOR INFO PAGE ---------------------
elif page == "👩‍💻 Creator Info":
    st.markdown('<div class="main-header">👩‍💻 About the Creator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/200x200/667eea/ffffff?text=Developer", use_container_width=True)
    
    with col2:
        st.markdown("""
        ### **Farith Ahamed**
        
        **Role:** Data Analytics Developer
        
        **Skills:**
        - 🐍 Python
        - 📊 Data Analysis & Visualization
        - 🗄️ SQL / MySQL
        - 🎨 Streamlit
        - 📈 Pandas & NumPy
        - 📉 Matplotlib & Seaborn
        
        **Contact:**
        - 📧 Email: farithahamed736@gmail.com
        - 🔗 LinkedIn: linkedin.com/in/farith
        - 🐙 GitHub: github.com/farith
        """)
    
    st.markdown("---")
    st.markdown("### 🛠️ Technologies Used in This Project")
    
    tech_cols = st.columns(4)
    with tech_cols[0]:
        st.markdown("""
        **Frontend**
        - Streamlit
        - HTML/CSS
        """)
    with tech_cols[1]:
        st.markdown("""
        **Backend**
        - Python
        - MySQL
        """)
    with tech_cols[2]:
        st.markdown("""
        **Data Processing**
        - Pandas
        - NumPy
        """)
    with tech_cols[3]:
        st.markdown("""
        **Visualization**
        - Matplotlib
        - Seaborn
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📝 Project Details
    - **Database:** MySQL (global_literacy)
    - **Tables:** growth_data
    - **Total Records:** Dynamic
    - **Last Updated:** 2026
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>© 2026 Growth Population Analysis thanks for using | Built with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
