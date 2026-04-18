import streamlit as st
import datetime

st.set_page_config(page_title="Happy Birthday App", page_icon="🎂")

st.title("🎉 Happy Birthday App 🎉")

name = st.text_input("Enter the Birthday Person Name")

if st.button("Celebrate 🎊"):
    if name:
        st.success(f"🎂 Happy Birthday {name}! 🎉")
        st.balloons()
        st.write("May Allah bless you with happiness, success, and long life 🤲")
    else:
        st.warning("Please enter a name first!")

today = datetime.date.today()
st.write("Today's Date:", today)
