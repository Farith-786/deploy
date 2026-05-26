import streamlit as st
from datetime import datetime
# Set the title of the app
st.title("My Sister's Anniversary Alshifa & Yousuf")
# Get the current date
import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Happy Anniversary Sister ❤️",
    page_icon="💖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #ffdde1, #ee9ca7);
}
.title {
    text-align: center;
    font-size: 55px;
    color: #d63384;
    font-weight: bold;
}
.message {
    text-align: center;
    font-size: 24px;
    color: #333333;
    line-height: 1.8;
}
.quote {
    background-color: rgba(255,255,255,0.7);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
}
.footer {
    text-align: center;
    color: #555;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Balloons
st.balloons()

# Title
st.markdown(
    '<p class="title">💖 Happy Wedding Anniversary Dear Sister Alshifa & Yousuf 💖</p>',
    unsafe_allow_html=True
)

# Image
st.image(
    "https://your-image-link.com/sister.jpg",
    use_container_width=True
)

st.markdown("---")

# Main Message
st.markdown("""
<div class="message">

🌹 Dear Sister 🌹

On this beautiful day, I wish you a very Happy Wedding Anniversary.

May your love continue to grow stronger with every passing year.
May Allah bless your marriage with endless happiness, peace,
prosperity, and countless beautiful memories.

Your journey together is an inspiration to everyone around you.
May your hearts always remain connected with love, trust, and understanding.

💐 Wishing you many more years of togetherness and joy. 💐

❤️ Happy Anniversary! ❤️

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Quotes Section
st.markdown("""
<div class="quote">

✨ "A successful marriage requires falling in love many times,
always with the same person." ✨

<br><br>

💞 "May your love story continue forever and become more beautiful each year." 💞

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Anniversary Counter
current_year = datetime.now().year

years = st.number_input(
    "How many years of marriage?",
    min_value=1,
    max_value=100,
    value=5
)

st.success(f"🎉 Celebrating {years} Wonderful Years Together! 🎉")

# Special Wishes Button
if st.button("💌 Open Special Anniversary Wish"):
    st.snow()

    st.markdown("""
    ## 💖 Special Message 💖

    Dear Sister,

    Thank you for being such a wonderful sister and role model.

    May Allah bless your family with happiness,
    good health, success, and endless love.

    🌹 Happy Anniversary to you! 🌹

    With Love,
    Your Brother ❤️
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    '<div class="footer">Made with ❤️ for My Beloved Sister</div>',
    unsafe_allow_html=True
)
