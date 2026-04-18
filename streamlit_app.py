import streamlit as st
import base64
from datetime import date

st.set_page_config(page_title="Birthday Celebration", page_icon="🎂", layout="centered")

# 🎨 Custom CSS (Mobile friendly + animation)
st.markdown("""
<style>
.big-title {
    text-align:center;
    color:#ff4b6e;
    font-size:50px;
    font-weight:bold;
}
.name-text {
    text-align:center;
    font-size:35px;
    color:#ff9800;
    animation: glow 1s ease-in-out infinite alternate;
}
@keyframes glow {
    from {text-shadow: 0 0 10px #fff;}
    to {text-shadow: 0 0 20px #ff4b6e;}
}
.footer {
    text-align:center;
    margin-top:50px;
    color:grey;
}
</style>
""", unsafe_allow_html=True)

# 🎵 Function to play music
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

# 🎉 Title
st.markdown('<p class="big-title">🎂 Birthday Celebration App 🎂</p>', unsafe_allow_html=True)

# Input
name = st.text_input("Enter Birthday Person Name 🎁")

col1, col2 = st.columns(2)

with col1:
    wish = st.button("🎉 Celebrate")

with col2:
    stop = st.button("🛑 Stop")

# 🎊 Celebration Action
if wish:
    if name != "":
        st.balloons()
        st.snow()
        st.markdown(f'<p class="name-text">Happy Birthday {name} 🎉🎂</p>', unsafe_allow_html=True)
        st.success("May your life be filled with happiness, success and good health 🤲")

        # Upload birthday song in same folder (birthday.mp3)
        autoplay_audio("birthday.mp3")
