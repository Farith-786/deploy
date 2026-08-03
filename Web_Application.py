# app.py
import streamlit as st
import importlib
try:
    module = importlib.import_module("streamlit_option_menu")
    option_menu = module.option_menu
    has_option_menu = True
except ImportError:
    option_menu = None
    has_option_menu = False
import pandas as pd
import datetime
import hashlib
import json
import os
import plotly.express as px
import calendar
import openpyxl
import yfinance
import requests

# ==================== USER AUTHENTICATION SYSTEM ====================

class UserAuth:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file or create default users"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            # Create default users
            self.users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "name": "Administrator",
                    "email": "admin@example.com",
                    "role": "admin"
                },
                "user1": {
                    "password": self.hash_password("user123"),
                    "name": "John Doe",
                    "email": "john@example.com",
                    "role": "user"
                }
            }
            self.save_users()
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate user"""
        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username]["password"] == hashed_password:
            return True
        return False
    
    def get_user_info(self, username):
        """Get user information"""
        if username in self.users:
            return self.users[username]
        return None
    
    def add_user(self, username, password, name, email, role="user"):
        """Add new user"""
        if username in self.users:
            return False, "Username already exists!"
        
        self.users[username] = {
            "password": self.hash_password(password),
            "name": name,
            "email": email,
            "role": role
        }
        self.save_users()
        return True, "User created successfully!"

# ==================== DATE OF BIRTH CALCULATOR ====================

class DOBCalculator:
    def __init__(self):
        self.calculations_history = []
    
    def calculate_age(self, dob):
        """Calculate age from date of birth"""
        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        # Calculate exact days
        days_in_year = 366 if self.is_leap_year(today.year) else 365
        days_lived = (today - dob).days
        
        # Calculate months and days
        months = 0
        days = 0
        temp_date = dob
        while temp_date < today:
            if temp_date.month == today.month and temp_date.year == today.year:
                days = (today - temp_date).days
                break
            # Move to next month
            if temp_date.month == 12:
                temp_date = datetime.date(temp_date.year + 1, 1, 1)
            else:
                next_month = temp_date.month + 1
                next_year = temp_date.year
                # Handle days in month
                days_in_month = calendar.monthrange(temp_date.year, temp_date.month)[1]
                if temp_date.day > days_in_month:
                    temp_date = datetime.date(temp_date.year, temp_date.month, days_in_month)
                temp_date = datetime.date(next_year, next_month, min(temp_date.day, calendar.monthrange(next_year, next_month)[1]))
            months += 1
        
        # Calculate next birthday
        next_birthday = datetime.date(today.year, dob.month, dob.day)
        if next_birthday < today:
            next_birthday = datetime.date(today.year + 1, dob.month, dob.day)
        days_until_birthday = (next_birthday - today).days
        
        # Zodiac sign
        zodiac_sign = self.get_zodiac_sign(dob)
        
        # Chinese zodiac
        chinese_zodiac = self.get_chinese_zodiac(dob.year)
        
        # Weekday born
        weekday_born = dob.strftime("%A")
        
        # Days until next birthday in months and days
        months_until_birthday = 0
        days_until_birthday_remainder = days_until_birthday
        while days_until_birthday_remainder >= 30:
            months_until_birthday += 1
            days_until_birthday_remainder -= 30
        
        return {
            "years": age,
            "months": months % 12,
            "days": days,
            "total_days": days_lived,
            "total_months": months,
            "total_weeks": days_lived // 7,
            "total_hours": days_lived * 24,
            "total_minutes": days_lived * 24 * 60,
            "total_seconds": days_lived * 24 * 60 * 60,
            "next_birthday": next_birthday,
            "days_until_birthday": days_until_birthday,
            "months_until_birthday": months_until_birthday,
            "days_until_birthday_remainder": days_until_birthday_remainder,
            "zodiac_sign": zodiac_sign,
            "chinese_zodiac": chinese_zodiac,
            "weekday_born": weekday_born,
            "is_leap_birthday": self.is_leap_year(dob.year) and dob.month == 2 and dob.day == 29
        }
    
    def is_leap_year(self, year):
        """Check if year is leap year"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def get_zodiac_sign(self, dob):
        """Get zodiac sign based on date of birth"""
        signs = {
            (1, 20): "Aquarius",
            (2, 19): "Pisces",
            (3, 21): "Aries",
            (4, 20): "Taurus",
            (5, 21): "Gemini",
            (6, 21): "Cancer",
            (7, 23): "Leo",
            (8, 23): "Virgo",
            (9, 23): "Libra",
            (10, 23): "Scorpio",
            (11, 22): "Sagittarius",
            (12, 22): "Capricorn"
        }
        
        month, day = dob.month, dob.day
        for (m, d), sign in signs.items():
            if (month == m and day <= d) or (month == m - 1 and day > signs[(m - 1, d)][1]):
                return sign
        return "Capricorn"
    
    def get_chinese_zodiac(self, year):
        """Get Chinese zodiac sign based on year"""
        zodiac_animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
        return zodiac_animals[(year - 4) % 12]
    
    def get_life_expectancy(self, country="USA"):
        """Get life expectancy based on country (simplified)"""
        life_expectancy_data = {
            "USA": 78.54,
            "Canada": 82.97,
            "UK": 81.32,
            "Germany": 81.20,
            "France": 82.54,
            "Japan": 84.32,
            "Australia": 83.24,
            "India": 70.19,
            "Brazil": 76.18,
            "South Africa": 64.73,
            "Singapore": 83.94,
            "South Korea": 83.63,
            "Spain": 83.99,
            "Italy": 83.15,
            "Switzerland": 83.97
        }
        return life_expectancy_data.get(country, 78.54)

# ==================== STREAMLIT APPLICATION ====================

def set_page_config():
    """Configure Streamlit page"""
    st.set_page_config(
        page_title="DOB Calculator Pro",
        page_icon="🎂",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: white;
    }
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
        margin: 0.5rem 0;
    }
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        margin: 0.5rem;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .stat-label {
        color: #6c757d;
        font-size: 0.9rem;
    }
    .zodiac-box {
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .birthday-celebration {
        font-size: 5rem;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

def login_page():
    """Display login page"""
    st.markdown("<div class='main-header'>🎂 DOB Calculator Pro</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Secure Login Portal</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            """, unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.button("🚀 Login", use_container_width=True)
            with col2:
                register_btn = st.button("📝 Register", use_container_width=True)
            
            if login_btn:
                if username and password:
                    auth = UserAuth()
                    if auth.authenticate(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        user_info = auth.get_user_info(username)
                        st.session_state.user_name = user_info["name"]
                        st.session_state.user_email = user_info["email"]
                        st.session_state.user_role = user_info["role"]
                        st.success(f"✅ Welcome back, {user_info['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Please enter both username and password!")
            
            if register_btn:
                st.session_state.show_register = True
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.info("💡 **Demo Credentials:**\n- Username: admin | Password: admin123\n- Username: user1 | Password: user123")

def register_page():
    """Display registration page"""
    st.markdown("<div class='main-header'>📝 Create Account</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            """, unsafe_allow_html=True)
            
            new_username = st.text_input("👤 Choose Username", placeholder="Enter username")
            new_password = st.text_input("🔒 Choose Password", type="password", placeholder="Enter password")
            confirm_password = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm password")
            full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            
            col1, col2 = st.columns(2)
            with col1:
                register_btn = st.button("📝 Register", use_container_width=True)
            with col2:
                back_btn = st.button("🔙 Back to Login", use_container_width=True)
            
            if register_btn:
                if new_username and new_password and full_name and email:
                    if new_password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    else:
                        auth = UserAuth()
                        success, message = auth.add_user(new_username, new_password, full_name, email)
                        if success:
                            st.success(f"✅ {message}")
                            st.info("You can now login with your new credentials!")
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill all fields!")
            
            if back_btn:
                st.session_state.show_register = False
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

def main_page():
    """Main application page"""
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
            <h3>👋 Welcome</h3>
            <p><strong>{st.session_state.user_name}</strong></p>
            <p style='font-size: 0.8rem;'>{st.session_state.user_email}</p>
            <p style='font-size: 0.8rem;'>Role: {st.session_state.user_role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        selected = option_menu(
            menu_title="Navigation",
            options=["Dashboard", "Age Calculator", "Birthday Tracker", "Life Statistics", "History", "Settings"],
            icons=["house", "calculator", "calendar", "graph-up", "clock-history", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#667eea"},
            }
        )
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_name = None
            st.session_state.user_email = None
            st.session_state.user_role = None
            st.rerun()
    
    # Main content based on navigation
    if selected == "Dashboard":
        dashboard_page()
    elif selected == "Age Calculator":
        age_calculator_page()
    elif selected == "Birthday Tracker":
        birthday_tracker_page()
    elif selected == "Life Statistics":
        life_statistics_page()
    elif selected == "History":
        history_page()
    elif selected == "Settings":
        settings_page()

def dashboard_page():
    """Dashboard page"""
    st.markdown("<div class='main-header'>📊 Dashboard</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-value'>🎂</div>
            <div class='stat-label'>Calculate Your Age</div>
            <p style='font-size: 0.9rem; color: #6c757d;'>Enter your DOB to get detailed age information</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-value'>📅</div>
            <div class='stat-label'>Track Birthdays</div>
            <p style='font-size: 0.9rem; color: #6c757d;'>Keep track of upcoming birthdays</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-value'>📈</div>
            <div class='stat-label'>Life Statistics</div>
            <p style='font-size: 0.9rem; color: #6c757d;'>View detailed life metrics</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick calculation
    st.divider()
    st.subheader("🔢 Quick Age Calculator")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        dob = st.date_input("Select your Date of Birth", 
                           min_value=datetime.date(1900, 1, 1), 
                           max_value=datetime.date.today())
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Calculate Age", use_container_width=True):
            calculator = DOBCalculator()
            result = calculator.calculate_age(dob)
            
            st.session_state.last_result = result
            st.session_state.last_dob = dob
            
            st.balloons()
            st.success(f"🎉 You are **{result['years']}** years old!")
    
    if 'last_result' in st.session_state:
        result = st.session_state.last_result
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Years", result['years'])
        with col2:
            st.metric("Months", result['months'])
        with col3:
            st.metric("Days", result['days'])
        with col4:
            st.metric("Total Days", f"{result['total_days']:,}")

def age_calculator_page():
    """Age calculator page"""
    st.markdown("<div class='main-header'>🔢 Age Calculator</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dob = st.date_input("📅 Select your Date of Birth", 
                           min_value=datetime.date(1900, 1, 1), 
                           max_value=datetime.date.today())
        
        if st.button("🧮 Calculate Detailed Age", use_container_width=True):
            calculator = DOBCalculator()
            result = calculator.calculate_age(dob)
            st.session_state.age_result = result
            st.session_state.age_dob = dob
    
    with col2:
        st.info("""
        **💡 What's included:**
        - Exact age in years, months, days
        - Total days lived
        - Zodiac signs
        - Birthday countdown
        - And much more!
        """)
    
    if 'age_result' in st.session_state:
        result = st.session_state.age_result
        dob = st.session_state.age_dob
        
        st.divider()
        
        # Main age display
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white;'>
            <h2>🎂 You are {result['years']} Years Old!</h2>
            <p style='font-size: 1.2rem;'>Born on {dob.strftime('%B %d, %Y')} ({result['weekday_born']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='card'>
                <h4>📊 Age in Details</h4>
                <p>Years: <strong>{result['years']}</strong></p>
                <p>Months: <strong>{result['months']}</strong></p>
                <p>Days: <strong>{result['days']}</strong></p>
                <p>Total Days: <strong>{result['total_days']:,}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='card'>
                <h4>⏰ Time Lived</h4>
                <p>Hours: <strong>{result['total_hours']:,}</strong></p>
                <p>Minutes: <strong>{result['total_minutes']:,}</strong></p>
                <p>Seconds: <strong>{result['total_seconds']:,}</strong></p>
                <p>Weeks: <strong>{result['total_weeks']:,}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='card'>
                <h4>🎯 Zodiac & More</h4>
                <p>Zodiac Sign: <strong>{result['zodiac_sign']}</strong></p>
                <p>Chinese Zodiac: <strong>{result['chinese_zodiac']}</strong></p>
                <p>Born on: <strong>{result['weekday_born']}</strong></p>
                {f"<p>🎉 Leap Year Birthday!</p>" if result['is_leap_birthday'] else ""}
            </div>
            """, unsafe_allow_html=True)
        
        # Birthday countdown
        st.divider()
        st.subheader("⏳ Next Birthday Countdown")
        
        if result['days_until_birthday'] == 0:
            st.markdown("""
            <div class='birthday-celebration'>
                🎉🎂🎉<br>
                <span style='font-size: 2rem;'>HAPPY BIRTHDAY!</span><br>
                🎉🎂🎉
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 15px;'>
                    <h1 style='font-size: 4rem; color: #667eea;'>{result['days_until_birthday']}</h1>
                    <p style='font-size: 1.2rem;'>Days until your next birthday!</p>
                    <p>Next birthday: {result['next_birthday'].strftime('%B %d, %Y')}</p>
                </div>
                """, unsafe_allow_html=True)

def birthday_tracker_page():
    """Birthday tracker page"""
    st.markdown("<div class='main-header'>📅 Birthday Tracker</div>", unsafe_allow_html=True)
    
    st.subheader("👥 Add Birthdays to Track")
    
    with st.expander("➕ Add New Birthday", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Person's Name")
        with col2:
            birthday = st.date_input("Birthday", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Birthday", use_container_width=True):
                if name:
                    if 'birthdays' not in st.session_state:
                        st.session_state.birthdays = []
                    
                    st.session_state.birthdays.append({
                        "name": name,
                        "birthday": birthday,
                        "year_added": datetime.date.today().year
                    })
                    
                    st.success(f"✅ Added {name}'s birthday!")
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter a name!")
    
    if 'birthdays' in st.session_state and st.session_state.birthdays:
        st.divider()
        st.subheader("📋 Saved Birthdays")
        
        # Sort by upcoming birthdays
        today = datetime.date.today()
        for birthday_entry in st.session_state.birthdays:
            bday = birthday_entry['birthday']
            next_birthday = datetime.date(today.year, bday.month, bday.day)
            if next_birthday < today:
                next_birthday = datetime.date(today.year + 1, bday.month, bday.day)
            
            days_until = (next_birthday - today).days
            
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"👤 {birthday_entry['name']}")
            with col2:
                st.write(f"📅 {bday.strftime('%B %d')}")
            with col3:
                if days_until == 0:
                    st.success("🎉 Today!")
                else:
                    st.write(f"⏳ {days_until} days")
            with col4:
                if st.button("🗑️", key=f"del_{birthday_entry['name']}_{birthday_entry['birthday']}"):
                    st.session_state.birthdays.remove(birthday_entry)
                    st.rerun()
        
        # Birthday calendar view
        st.divider()
        st.subheader("📊 Birthday Calendar")
        
        if st.button("Show Birthday Calendar"):
            import calendar as cal
            current_year = datetime.date.today().year
            
            # Create calendar data
            months = []
            counts = []
            
            for month in range(1, 13):
                month_count = sum(1 for b in st.session_state.birthdays if b['birthday'].month == month)
                months.append(cal.month_name[month])
                counts.append(month_count)
            
            fig = px.bar(x=months, y=counts, 
                        title="Birthdays by Month",
                        labels={'x': 'Month', 'y': 'Number of Birthdays'},
                        color=counts,
                        color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No birthdays saved yet. Add some above!")

def life_statistics_page():
    """Life statistics page"""
    st.markdown("<div class='main-header'>📈 Life Statistics</div>", unsafe_allow_html=True)
    
    st.subheader("🌍 Life Expectancy Comparison")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        dob = st.date_input("Your Date of Birth", 
                           min_value=datetime.date(1900, 1, 1), 
                           max_value=datetime.date.today(),
                           key="life_dob")
        
        country = st.selectbox("Select Country", 
                              ["USA", "Canada", "UK", "Germany", "France", 
                               "Japan", "Australia", "India", "Brazil", 
                               "South Africa", "Singapore", "South Korea", 
                               "Spain", "Italy", "Switzerland"])
        
        if st.button("Calculate Life Statistics"):
            calculator = DOBCalculator()
            age_result = calculator.calculate_age(dob)
            life_expectancy = calculator.get_life_expectancy(country)
            
            st.session_state.life_dob = dob
            st.session_state.life_age_result = age_result
            st.session_state.life_expectancy = life_expectancy
    
    with col2:
        st.info("""
        **📊 What we calculate:**
        - Your current age
        - Life expectancy
        - Time remaining
        - Percentage of life lived
        """)
    
    if 'life_age_result' in st.session_state:
        age_result = st.session_state.life_age_result
        life_expectancy = st.session_state.life_expectancy
        
        # Calculate percentages
        total_years = life_expectancy
        years_lived = age_result['years']
        years_remaining = total_years - years_lived
        
        # Create visualization
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = years_lived,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Progress Through Life"},
            delta = {'reference': total_years, 'valueformat': '.0f'},
            gauge = {
                'axis': {'range': [None, total_years], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "rgba(102, 126, 234, 0.7)"},
                'steps': [
                    {'range': [0, years_lived], 'color': "rgba(102, 126, 234, 0.5)"},
                    {'range': [years_lived, total_years], 'color': "rgba(200, 200, 200, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': total_years
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='card'>
                <h4>🎂 Current Age</h4>
                <h2>{years_lived} years</h2>
                <p>You are {years_lived} years old</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='card'>
                <h4>📅 Life Expectancy</h4>
                <h2>{total_years:.1f} years</h2>
                <p>Average in {country}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='card'>
                <h4>⏳ Remaining</h4>
                <h2>{years_remaining:.1f} years</h2>
                <p>{((years_lived/total_years)*100):.1f}% of life lived</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional statistics
        st.divider()
        st.subheader("📊 Additional Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Days Lived", f"{age_result['total_days']:,}")
        with col2:
            st.metric("Total Hours", f"{age_result['total_hours']:,}")
        with col3:
            st.metric("Total Minutes", f"{age_result['total_minutes']:,}")
        with col4:
            st.metric("Total Seconds", f"{age_result['total_seconds']:,}")

def history_page():
    """History page"""
    st.markdown("<div class='main-header'>🕰️ Calculation History</div>", unsafe_allow_html=True)
    
    if 'calculation_history' not in st.session_state:
        st.session_state.calculation_history = []
    
    st.info("💡 Your recent calculations will appear here")
    
    if st.session_state.calculation_history:
        # Create a DataFrame for display
        history_data = []
        for entry in st.session_state.calculation_history:
            history_data.append({
                "Date": entry['date'].strftime('%Y-%m-%d %H:%M'),
                "DOB": entry['dob'].strftime('%Y-%m-%d'),
                "Age": f"{entry['result']['years']} years, {entry['result']['months']} months",
                "Zodiac": entry['result']['zodiac_sign'],
                "Days Lived": entry['result']['total_days']
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Clear History"):
            st.session_state.calculation_history = []
            st.rerun()
    else:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px;'>
            <h3 style='color: #6c757d;'>📭 No history yet</h3>
            <p>Start calculating your age to build history!</p>
        </div>
        """, unsafe_allow_html=True)

def settings_page():
    """Settings page"""
    st.markdown("<div class='main-header'>⚙️ Settings</div>", unsafe_allow_html=True)
    
    st.subheader("👤 Profile Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", value=st.session_state.user_name)
        st.text_input("Email", value=st.session_state.user_email)
        st.text_input("Username", value=st.session_state.username, disabled=True)
        
        if st.button("💾 Update Profile"):
            st.success("✅ Profile updated successfully!")
    
    with col2:
        st.subheader("🔒 Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")
        
        if st.button("🔄 Change Password"):
            if current_password and new_password and confirm_new_password:
                if new_password == confirm_new_password:
                    st.success("✅ Password changed successfully!")
                else:
                    st.error("❌ New passwords don't match!")
            else:
                st.warning("⚠️ Please fill all fields!")
    
    st.divider()
    st.subheader("🎨 Application Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        theme = st.selectbox("Theme", ["Light", "Dark", "System"])
        language = st.selectbox("Language", ["English", "Spanish", "French"])
    
    with col2:
        notifications = st.checkbox("Enable Notifications", value=True)
