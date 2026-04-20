import streamlit as st
import pandas as pd
st.title("My First develop App")
demo = st.text_input("Enter your name")

dataset = st.file_uploader("Upload your dataset", type=["csv"])
if dataset is not None:
    df = pd.read_csv(dataset)
    st.dataframe(df)

if st.checkbox("Show Summary"):
    st.write(df.describe())

if st.checkbox("Show Plot"):
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
    st.plotly_chart(fig)

if dataset is not None:
    data = pd.read_csv(dataset)
