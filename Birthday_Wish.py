import streamlit as st

st.markdown(
    """
    <h1 style='text-align: center; color: pink;'>🎂 Happy Birthday Priya 🎂</h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <p style='text-align: center; color: purple;'>Wishing you a day filled with love, joy, and unforgettable moments! 🎉🎁</p>
    """,
    unsafe_allow_html=True
)
st.title("How was your birthday as been going?")
st.selectbox("Choose a answer", ["most Enjoying", "Very Bore", "50% ok", "Not so good", "Worst"])
st.chat_message("PLEASE ENJOY YOUR BIRTHDAY AND MAKE IT MEMORABLE")
name = st.text_input("Enter Name")

if st.button("Click me!"):
    st.write("Button clicked!")
if st.checkbox("Show more info"):
    st.write("Hey Hi priya This is my app development in your birthday wish, intha Birthday unaku happy ha poganum at the same time unaku erukura kashtam ellamae Poidum Kooda aa eruken edhukum Payapidadha Pathukalam.")

if st.button("Celebrate 🎉"):
    if name:
        st.markdown(f"<h2 style='color: gold;'>Happy Birthday {name}! 🎊</h2>", unsafe_allow_html=True)
        st.balloons()
        st.snow()
    else:
        st.warning("Please enter your name to celebrate!")
