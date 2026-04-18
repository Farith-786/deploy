import streamlit as st
import base64
from datetime import date
from PIL import Image

st.set_page_config(page_title="Ultimate Birthday App", page_icon="🎂", layout="centered")

# ---------------- CSS DESIGN ---------------- #
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:55px;
    color:#ff4b6e;
    font-weight:bold;
}
.sub-title{
    text-align:center;
    font-size:30px;
    color:#ffa500;
}
.glow{
    text-align:center;
    font-size:40px;
    color:white;
    animation: glow 1s ease-in-out infinite alternate;
}
@keyframes glow{
    from { text-shadow: 0 0 10px #fff; }
    to { text-shadow: 0 0 25px #ff4b6e; }
}
.footer{
    text-align:center;
    margin-top:40px;
    color:grey;
}
.card{
    padding:20px;
    border-radius:15px;
    background: linear-gradient(45deg,#ff4b6e,#ffa500);
    text-align:center;
    color:white;
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MUSIC FUNCTION ---------------- #
def autoplay_audio(file):
    with open(file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.markdown('<p class="main-title">🎂 Ultimate Birthday Wish App 🎂</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Create a Beautiful Birthday Card 🎁</p>', unsafe_allow_html=True)

st.divider()

# ---------------- USER INPUT ---------------- #
name = st.text_input("🎉 Enter Birthday Person Name")
age = st.number_input("🎈 Enter Age", min_value=1, max_value=100)
message = st.text_area("💌 Custom Birthday Message")

uploaded_file = st.file_uploader("📸 Upload Birthday Photo", type=["jpg","png","jpeg"])

col1, col2 = st.columns(2)
celebrate = col1.button("🎊 Generate Birthday Card")
reset = col2.button("🔄 Reset")

st.divider()

# ---------------- CELEBRATION ---------------- #
if celebrate:
    if name != "":
        st.balloons()
        st.snow()
        autoplay_audio("birthday.mp3")

        st.markdown(f'<p class="glow">Happy Birthday {name} 🎉</p>', unsafe_allow_html=True)

        # Show Image
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Birthday Star ⭐", use_container_width=True)

        # Birthday Card
        st.markdown(f"""
        <div class="card">
        🎂 Happy {age}th Birthday {name}! 🎂 <br><br>
        {message if message else "May Allah bless you with happiness, health and success 🤲"}
        </div>
        """, unsafe_allow_html=True)

        st.success("🎉 Birthday Card Generated Successfully!")

        # Share Message
        share_text = f"Happy Birthday {name}! 🎂🎉"
        st.code(share_text)
        st.info("Copy this message and share in WhatsApp 💚")

    else:
        st.warning("Please enter the name")

# Footer
today = date.today()
st.markdown(f"<div class='footer'>Made with ❤️ using Streamlit | {today}</div>", unsafe_allow_html=True)
