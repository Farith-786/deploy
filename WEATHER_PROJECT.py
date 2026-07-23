import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class AbstractMatplotlib(ABC):
    """Abstract base class defining common matplotlib plotting methods."""

    @abstractmethod
    def plot_line(self, x, y, title=None, xlabel=None, ylabel=None, legend=None, marker="o", color=None):
        pass

    @abstractmethod
    def plot_bar(self, x, y, title=None, xlabel=None, ylabel=None, color=None):
        pass

    @abstractmethod
    def plot_scatter(self, x, y, title=None, xlabel=None, ylabel=None, color=None, size=None):
        pass

    @abstractmethod
    def plot_pie(self, values, labels, title=None, autopct="%1.1f%%", cmap="tab20"):
        pass

    @abstractmethod
    def plot_heatmap(self, data, xlabels=None, ylabels=None, title=None, annot=True, cmap="viridis"):
        pass

    @abstractmethod
    def savefig(self, filename, dpi=300):
        pass

class matplotlib(AbstractMatplotlib):
    """Concrete matplotlib wrapper implementing abstract plotting methods."""

    def plot_line(self, x, y, title=None, xlabel=None, ylabel=None, legend=None, marker="o", color=None):
        fig, ax = plt.subplots()
        ax.plot(x, y, marker=marker, color=color or "#1f77b4")
        ax.set_title(title or "")
        ax.set_xlabel(xlabel or "")
        ax.set_ylabel(ylabel or "")
        if legend:
            ax.legend(legend)
        ax.grid(True, linestyle="--", alpha=0.5)
        return fig

    def plot_bar(self, x, y, title=None, xlabel=None, ylabel=None, color=None):
        fig, ax = plt.subplots()
        ax.bar(x, y, color=color or "#1f77b4")
        ax.set_title(title or "")
        ax.set_xlabel(xlabel or "")
        ax.set_ylabel(ylabel or "")
        ax.grid(True, axis="y", linestyle="--", alpha=0.5)
        return fig

    def plot_scatter(self, x, y, title=None, xlabel=None, ylabel=None, color=None, size=None):
        fig, ax = plt.subplots()
        sizes = size if size is not None else 50
        ax.scatter(x, y, c=color or "#1f77b4", s=sizes, alpha=0.8, edgecolor="k")
        ax.set_title(title or "")
        ax.set_xlabel(xlabel or "")
        ax.set_ylabel(ylabel or "")
        ax.grid(True, linestyle="--", alpha=0.5)
        return fig

    def plot_pie(self, values, labels, title=None, autopct="%1.1f%%", cmap="tab20"):
        fig, ax = plt.subplots()
        colors = plt.get_cmap(cmap)(range(len(values)))
        ax.pie(values, labels=labels, autopct=autopct, colors=colors, startangle=90)
        ax.set_title(title or "")
        ax.axis("equal")
        return fig

    def plot_heatmap(self, data, xlabels=None, ylabels=None, title=None, annot=True, cmap="viridis"):
        fig, ax = plt.subplots()
        sns.heatmap(
            data,
            annot=annot,
            fmt=".2f",
            cmap=cmap,
            xticklabels=xlabels,
            yticklabels=ylabels,
            ax=ax
        )
        ax.set_title(title or "")
        return fig

    def savefig(self, filename, dpi=300):
        fig = plt.gcf()
        fig.savefig(filename, dpi=dpi, bbox_inches="tight")
        return filename

class plotly(AbstractMatplotlib):
    """Concrete plotly wrapper implementing abstract plotting methods."""

    def plot_line(self, x, y, title=None, xlabel=None, ylabel=None, legend=None, marker="o", color=None):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines+markers',
            marker=dict(size=8, symbol=marker, color=color or "#1f77b4"),
            name=legend[0] if legend else "Line"
        ))
        fig.update_layout(
            title=title or "",
            xaxis_title=xlabel or "",
            yaxis_title=ylabel or "",
            hovermode='x unified',
            template='plotly_white'
        )
        return fig

    def plot_bar(self, x, y, title=None, xlabel=None, ylabel=None, color=None):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x, y=y,
            marker=dict(color=color or "#1f77b4"),
            name="Bar"
        ))
        fig.update_layout(
            title=title or "",
            xaxis_title=xlabel or "",
            yaxis_title=ylabel or "",
            template='plotly_white',
            showlegend=False
        )
        return fig

    def plot_scatter(self, x, y, title=None, xlabel=None, ylabel=None, color=None, size=None):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers',
            marker=dict(
                size=size or 8,
                color=color or "#1f77b4",
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            name="Scatter"
        ))
        fig.update_layout(
            title=title or "",
            xaxis_title=xlabel or "",
            yaxis_title=ylabel or "",
            hovermode='closest',
            template='plotly_white'
        )
        return fig

    def plot_pie(self, values, labels, title=None, autopct="%1.1f%%", cmap="tab20"):
        fig = go.Figure()
        fig.add_trace(go.Pie(
            values=values,
            labels=labels,
            textposition='inside',
            textinfo='label+percent'
        ))
        fig.update_layout(
            title=title or "",
            template='plotly_white'
        )
        return fig

    def plot_heatmap(self, data, xlabels=None, ylabels=None, title=None, annot=True, cmap="viridis"):
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=data,
            x=xlabels,
            y=ylabels,
            colorscale=cmap,
            text=data if annot else None,
            texttemplate='%{text:.2f}' if annot else None,
            textfont={"size": 10} if annot else None
        ))
        fig.update_layout(
            title=title or "",
            template='plotly_white'
        )
        return fig

    def savefig(self, filename, dpi=300):
        st.write(f"Note: Plotly figures should be saved using Streamlit's built-in features.")
        return filename


class px_wrapper(AbstractMatplotlib):
    """Wrapper around plotly.express (px) implementing abstract plotting methods."""

    def plot_line(self, x, y, title=None, xlabel=None, ylabel=None, legend=None, marker="o", color=None):
        fig = px.line(x=x, y=y, labels={"x": xlabel or "", "y": ylabel or ""}, title=title or "")
        fig.update_traces(marker=dict(size=8, symbol=marker, color=color or "#1f77b4"))
        fig.update_layout(template='plotly_white')
        return fig

    def plot_bar(self, x, y, title=None, xlabel=None, ylabel=None, color=None):
        fig = px.bar(x=x, y=y, labels={"x": xlabel or "", "y": ylabel or ""}, title=title or "")
        if color is not None:
            fig.update_traces(marker_color=color)
        fig.update_layout(template='plotly_white')
        return fig

    def plot_scatter(self, x, y, title=None, xlabel=None, ylabel=None, color=None, size=None):
        fig = px.scatter(x=x, y=y, size=size or None, color=color or None,
                         labels={"x": xlabel or "", "y": ylabel or ""}, title=title or "")
        fig.update_layout(template='plotly_white')
        return fig

    def plot_pie(self, values, labels, title=None, autopct="%1.1f%%", cmap="tab20"):
        # plotly.express pie uses names and values
        fig = px.pie(values=values, names=labels, title=title or "")
        fig.update_traces(textposition='inside', textinfo='label+percent')
        fig.update_layout(template='plotly_white')
        return fig

    def plot_heatmap(self, data, xlabels=None, ylabels=None, title=None, annot=True, cmap="viridis"):
        # px.imshow handles heatmaps conveniently
        fig = px.imshow(data, x=xlabels, y=ylabels, color_continuous_scale=cmap, title=title or "")
        if annot:
            # px.imshow will show z values when text_auto is enabled
            fig.update_traces(texttemplate="%{z:.2f}", textfont_size=10)
        fig.update_layout(template='plotly_white')
        return fig

    def savefig(self, filename, dpi=300):
        # Prefer HTML export for Plotly Express figures for portability
        try:
            # if filename ends with .html use write_html
            if not filename.lower().endswith('.html'):
                filename = filename + '.html'
            # create a minimal blank figure and write a note (caller should pass fig instead normally)
            # This method just returns filename for compatibility
            open(filename, 'w').write('<!-- Plotly px export placeholder -->')
            return filename
        except Exception:
            return filename

# Page configuration
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
        font-size: 3rem;
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

def execute_query(query, params=None):
    """Execute a query and return results as DataFrame"""
    conn = connect_to_mysql()
    if conn is None:
        return pd.DataFrame()
    
    try:
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()
    finally:
        if conn.is_connected():
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
        query += " AND City = %s"
        params.append(city)
    
    if date_start and date_end:
        query += " AND Date BETWEEN %s AND %s"
        params.extend([date_start, date_end])
    
    if month:
        query += " AND MONTH(Date) = %s"
        params.append(month)
    
    return execute_query(query, params=tuple(params) if params else None)

# Main Application
def main():
    # Sidebar Navigation
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1163/1163661.png", width=100)
    st.sidebar.title("🌦️ Weather Explorer")
    
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "📊 Visualizations", "📈 Advanced Analytics", "💾 SQL Queries", "ℹ️ About"],
        index=0
    )
    
    # Get cities for filters
    cities = get_cities()
    
    if page == "🏠 Home":
        home_page(cities)
    elif page == "📊 Visualizations":
        visualization_page(cities)
    elif page == "📈 Advanced Analytics":
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
    df = execute_query("SELECT COUNT(*) as total_records, COUNT(DISTINCT City) as total_cities FROM weather_data")
    if not df.empty:
        total_records = df['total_records'].iloc[0]
        total_cities = df['total_cities'].iloc[0]
        
        avg_temp = execute_query("SELECT AVG(Temperature_C) as avg_temp FROM weather_data")
        max_temp = execute_query("SELECT MAX(Temperature_C) as max_temp FROM weather_data")
        min_temp = execute_query("SELECT MIN(Temperature_C) as min_temp FROM weather_data")
        
        with col1:
            st.metric("Total Records", f"{total_records:,}")
        with col2:
            st.metric("Cities Covered", total_cities)
        with col3:
            st.metric("Average Temperature", f"{avg_temp['avg_temp'].iloc[0]:.1f}°C" if not avg_temp.empty else "N/A")
        with col4:
            st.metric("Temperature Range", f"{min_temp['min_temp'].iloc[0]:.1f}°C - {max_temp['max_temp'].iloc[0]:.1f}°C" if not min_temp.empty else "N/A")
    
    # Show sample data
    st.subheader("📋 Sample Weather Data")
    sample_df = execute_query("SELECT * FROM weather_data LIMIT 10")
    if not sample_df.empty:
        st.dataframe(sample_df, use_container_width=True)
    
    # Quick filters
    st.subheader("🔍 Quick Search")
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Select City", ["All"] + cities)
    with col2:
        date_range = st.date_input("Date Range", [])
    
    if st.button("Search Data"):
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
        st.warning("No cities found in database. Please add weather data first.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_city = st.selectbox("Select City", cities)
    with col2:
        date_start = st.date_input("Start Date", datetime.now().date())
    with col3:
        date_end = st.date_input("End Date", datetime.now().date())
    
    # Fetch data
    df = get_weather_data(
        city=selected_city,
        date_start=date_start.strftime("%Y-%m-%d"),
        date_end=date_end.strftime("%Y-%m-%d")
    )
    
    if df.empty:
        st.warning("No data available for selected filters")
        return
    
    st.success(f"Found {len(df)} records for {selected_city}")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "💧 Humidity", "💨 Wind", "🌧️ Weather Conditions"])
    
    with tab1:
        st.subheader("Temperature Trends")
        
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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Wind Speed", f"{df['Wind_Speed_kmh'].mean():.1f} km/h")
        with col2:
            st.metric("Max Wind Speed", f"{df['Wind_Speed_kmh'].max():.1f} km/h")
        with col3:
            st.metric("Min Wind Speed", f"{df['Wind_Speed_kmh'].min():.1f} km/h")
    
    with tab4:
        st.subheader("Weather Conditions Distribution")
        
        # Weather condition distribution
        weather_counts = df['Weather_Condition'].value_counts()
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
        st.warning("No cities found in database. Please add weather data first.")
        return
    
    # Multi-city comparison
    st.subheader("🏙️ Multi-City Comparison")
    selected_cities = st.multiselect("Select cities to compare", cities, default=cities[:2] if len(cities) >= 2 else cities)
    
    if selected_cities:
        df = get_weather_data()
        if not df.empty:
            df_filtered = df[df['City'].isin(selected_cities)]
            
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
        
        # Scatter matrix
        st.subheader("🔄 Scatter Plot Matrix")
        fig3 = px.scatter_matrix(df,
                                 dimensions=numeric_cols,
                                 title="Weather Parameter Relationships",
                                 color="City" if 'City' in df.columns else None)
        st.plotly_chart(fig3, use_container_width=True)

def sql_queries_page():
    """SQL Queries page"""
    st.subheader("💾 SQL Query Runner")
    
    # Predefined queries
    st.write("### 📋 Predefined Queries")
    predefined_queries = {
        "Average Temperature per City": "SELECT City, AVG(Temperature_C) AS Avg_Temperature, COUNT(*) as Records FROM weather_data GROUP BY City ORDER BY Avg_Temperature DESC",
        "Highest Humidity per City": "SELECT City, MAX(Humidity_Percentage) AS Max_Humidity, Date FROM weather_data GROUP BY City ORDER BY Max_Humidity DESC",
        "Temperature Extremes": "SELECT City, MIN(Temperature_C) AS Min_Temp, MAX(Temperature_C) AS Max_Temp, (MAX(Temperature_C) - MIN(Temperature_C)) AS Temp_Range FROM weather_data GROUP BY City ORDER BY Temp_Range DESC",
        "Most Common Weather Conditions": "SELECT Weather_Condition, COUNT(*) AS Frequency, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM weather_data), 2) AS Percentage FROM weather_data GROUP BY Weather_Condition ORDER BY Frequency DESC",
        "Wind Speed Analysis": "SELECT City, AVG(Wind_Speed_kmh) AS Avg_Wind, MAX(Wind_Speed_kmh) AS Max_Wind, MIN(Wind_Speed_kmh) AS Min_Wind FROM weather_data GROUP BY City ORDER BY Avg_Wind DESC",
        "Monthly Temperature Trends": "SELECT City, MONTH(Date) AS Month, AVG(Temperature_C) AS Avg_Temp FROM weather_data GROUP BY City, MONTH(Date) ORDER BY City, Month"
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
                st.success(f"Query executed successfully! {len(result)} rows returned.")
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
        if st.button("▶️ Run Custom Query"):
            try:
                result = execute_query(custom_query)
                if not result.empty:
                    st.success("Query executed successfully!")
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
                st.error(f"Error executing custom query: {e}")

def about_page():
    """About page"""
    st.markdown("<h1 class='main-header'>ℹ️ About This Project</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ## 🌦️ Weather Data Analysis Dashboard
    
    ### Project Overview
    This Streamlit application provides comprehensive weather data analysis and visualization capabilities.
    It connects to a MySQL database containing weather information from various cities.
    
    ### Features
    - **📊 Interactive Visualizations**: Dynamic charts for temperature, humidity, wind speed, and weather conditions
    - **🔍 Data Filtering**: Filter weather data by city, date range, and month
    - **📈 Advanced Analytics**: Multi-city comparison, correlation analysis, and statistical insights
    - **💾 SQL Query Runner**: Predefined and custom SQL queries for data exploration
    - **📥 Data Export**: Download query results as CSV files
    
    ### Technologies Used
    - **Python** - Core programming language
    - **Streamlit** - Web application framework
    - **MySQL** - Database management system
    - **Pandas** - Data manipulation and analysis
    - **Plotly** - Interactive visualizations
    - **Seaborn/Matplotlib** - Statistical visualizations
    
    ### Database Schema
    ```sql
    weather_data (
        id INT PRIMARY KEY AUTO_INCREMENT,
        City VARCHAR(100),
        Date DATE,
        Temperature_C DECIMAL(5,2),
        Humidity_Percentage DECIMAL(5,2),
        Wind_Speed_kmh DECIMAL(5,2),
        Weather_Condition VARCHAR(100)
"""   )
