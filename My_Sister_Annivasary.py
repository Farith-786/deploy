import streamlit as st
import base64


st.set_page_config(
    page_title="Happy Birthday My Love ❤️",
    page_icon="🎂",
    layout="wide"
)

# ---------- Background CSS ----------
page_bg = """
<style>
[data-testid="stAppViewContainer"]{
background: linear-gradient(-45deg,
#ff9a9e,
#fad0c4,
#fbc2eb,
#a18cd1);
background-size: 400% 400%;
animation: gradient 15s ease infinite;
}

@keyframes gradient {
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

h1{
text-align:center;
font-size:70px !important;
color:white;
text-shadow:3px 3px 10px black;
}

.big-text{
font-size:35px;
font-weight:bold;
text-align:center;
color:white;
text-shadow:2px 2px 8px black;
}

.heart{
font-size:60px;
animation: pulse 1.5s infinite;
text-align:center;
}

@keyframes pulse{
0%{transform:scale(1);}
50%{transform:scale(1.2);}
100%{transform:scale(1);}
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------- Title ----------

st.title("How was your birthday as been going?")
st.selectbox("Choose a answer", ["most Enjoying", "Very Bore", "50% ok", "Not so good", "Worst"])
st.chat_message("PLEASE ENJOY YOUR BIRTHDAY AND MAKE IT MEMORABLE")
name = st.text_input("Enter Name")

# ---------- Message ----------
st.markdown(
"""
<div class='big-text'>
🌹 My Dearest Wife 🌹<br><br>

Happy Birthday to the most beautiful woman in my life. ❤️<br><br>

Every day with you is a blessing and every moment spent with you is a precious memory. 💕<br><br>

You are my happiness, my strength, my best friend, and the love of my life. ❤️<br><br>

May your birthday be filled with endless joy, laughter, love, and all the happiness you deserve. 🎁🎂🎉<br><br>

I promise to love you today, tomorrow, and forever. 💖<br><br>

st.markdown("<h1>🎂 Happy Birthday My Love ❤️</h1>", unsafe_allow_html=True)

elif page == "Creator Info":
    st.title("Creator Information")
    st.markdown("""
    **Name:** Farith Ahamed
    **designation:** Software Engineer  
    **Email:** Farith.Tech.Software Engineer.com

    """)
