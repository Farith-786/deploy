import streamlit as st

st.markdown(
    """
    <h1 style='text-align: center; color: pink;'>🎂 Happy Birthday 🎂</h1>
    """,
    unsafe_allow_html=True
)

name = st.text_input("Enter Name")

if st.button("Celebrate 🎉"):
    if name:
        st.markdown(f"<h2 style='color: gold;'>Happy Birthday {name}! 🎊</h2>", unsafe_allow_html=True)
        st.balloons()
        st.snow()
        if st.button("Click me!"):
    st.write("Button clicked!")
if st.checkbox("Show more info"):
    st.write("Assalamu alaikum Guys very Most Welcome to my 1st App development.")
