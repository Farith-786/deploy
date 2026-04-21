import streamlit as st
def main():
    st.header("Welcome to my First Web App!")
    st.subheader("Most Welcome's to you all")
    st.title("Hello, Yasar!")
st.title("What is your favorite main Doing Activities?")
st.selectbox("Choose a answer", ["Quran", "Prayer", "Fasting", "Hajj", "Zakat", "All of the above"])
st.suprise = st.checkbox("Do you like this app?")
if st.suprise:    st.write("Thank you for liking my app!")
st.balloons()
st.write("I hope you will like it and enjoy it!")


if __name__ == "__main__":
    main()
