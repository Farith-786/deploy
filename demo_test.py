import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


st.title("My First develop App")
demo = st.text_input("Enter your name")

dataset = st.file_uploader("Upload your dataset", type=["csv"])
if dataset is not None:
    df = pd.read_csv(dataset)
    st.dataframe(df)

if st.checkbox("Show Summary"):
    st.write(df.describe())
    
