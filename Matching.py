import streamlit as st
import json
import os
from datetime import datetime

# ---------- CONFIG ----------
st.set_page_config(page_title="💘 Find Your Match", page_icon="💘", layout="centered")
DATA_FILE = "matches.json"

# ---------- HELPERS ----------
def load_matches():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_match(entry):
    matches = load_matches()
    matches.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(matches, f, indent=2)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
    }
    h1 { color: #d6336c; text-align: center; }
    .stButton>button {
        background: #d6336c;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
page = st.sidebar.radio("Navigate", ["💘 Find Your Match", "👩‍💻 Creator Info"])

st.title("💘 Find Your Perfect Match Friendship Bond")
st.write("Answer a few questions so I can find your perfect Boy & Girl Friendship Bond 💕")

# ---------- FORM ----------
with st.form("dating_form"):
    name = st.text_input("Your Name 👤")
    age = st.slider("Your Age", 18, 60, 25)
    interests = st.multiselect(
        "Your Interests 💫",
        ["Music", "Travel", "Books", "Gaming", "Fitness", "Coding", "Movies", "Cooking", "Art"]
    )
    vibe = st.radio("Your vibe?", ["Funny 😄", "Romantic 🌹", "Adventurous 🌍", "Intellectual 🧠"])
    message = st.text_area("Enna pathi ungaluku Therinjadha Solunga Honest ha erundhalum i Agree 💌")

    submitted = st.form_submit_button("Find My Match 💘")

# ---------- PROCESS ----------
if submitted:
    if not name.strip():
        st.error("Please enter your name 😅")
    elif not interests:
        st.error("Pick at least one interest 💫")
    else:
        # Fake matching algorithm (fun logic)
        score = min(100, 40 + len(interests) * 8 + (age % 20))
        
        if score >= 85:
            match_name = "Sofia 💖"
            match_desc = "Loves the same things you do. Perfect match!"
        elif score >= 70:
            match_name = "Emma 🌸"
            match_desc = "Great chemistry detected!"
        else:
            match_name = "Chloe ✨"
            match_desc = "A lovely girl who shares your vibe."

        # Save to file (so you can see results later)
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "age": age,
            "interests": interests,
            "vibe": vibe,
            "message": message,
            "match": match_name,
            "score": score,
            "description": match_desc,
            
        }
        save_match(entry)

        # Show results
        st.balloons()
        st.success(f"🎉 Match Found for {name}!")
        st.markdown(f"### 💕 Your match: **{match_name}**")
        st.progress(score / 100)
        st.write(f"**Compatibility Score:** {score}%")
        st.info(match_desc)
        st.write(f"**Her vibe:** {vibe}")
        st.write(f"**Shared interests:** {', '.join(interests)}")
        
        if message:
            st.write("**Your message was delivered 💌**")
            st.code(message, language=None)

# ---------- ADMIN: VIEW ALL SUBMISSIONS ----------
st.markdown("---")
with st.expander("🔒 Owner Panel – View All Matches (for you)"):
    password = st.text_input("Enter admin password", type="password")
    if password == "admin123":   # change this!
        matches = load_matches()
        if not matches:
            st.warning("No one has filled the form yet.")
        else:
            st.success(f"Total submissions: {len(matches)}")
            for m in matches[::-1]:
                st.markdown(f"""
                ---
                **🕒 {m['timestamp']}**  
                **👤 Name:** {m['name']} (age {m['age']})  
                **🎯 Vibe:** {m['vibe']}  
                **💫 Interests:** {', '.join(m['interests'])}  
                **💌 Message:** {m['message']}  
                **💘 Match:** {m['match']} — **{m['score']}%**
                """)
            st.download_button(
                "📥 Download All Matches (JSON)",
                data=json.dumps(matches, indent=2),
                file_name="all_matches.json",
                mime="application/json"
            )
    elif password:
        st.error("Wrong password ❌")
        
# --------------------- CREATOR INFO PAGE ---------------------
if page == "👩‍💻 Creator Info":
    st.markdown('<div class="main-header">👩‍💻 About the Creator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/200x200/667eea/ffffff?text=Developer", use_container_width=True)
    
    with col2:
        st.markdown("""
        ### **Farith Ahamed**
        
        **Role:** Software Developer
        
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
    - **Database:** MySQL (Matching_2026)
    - **Tables:** Matching_data
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
