import streamlit as st

st.title("This is my first Streamlit app")
st.header("Welcome to Streamlit!")
st.write("This is a basic Streamlit app.")

name=st.text_input("Enter your name:")
if name:
    st.success(f"Hello, {name}! \nHow are you?")
    
number= st.slider("Pick a age",0,100)
st.write(f"Your age is {number}")
if st.button("Click me!"):
    st.write("Button clicked!")
if st.checkbox("Show more info"):
    st.write("Assalamu alaikum Guys very Most Welcome to my 1st App development.")
