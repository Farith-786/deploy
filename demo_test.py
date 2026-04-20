import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
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

if st.checkbox("Show Plot"):
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
    st.plotly_chart(fig)

if dataset is not None:
    data = pd.read_csv(dataset)
         
x = data.iloc[:, 0]
y = data.iloc[:, 1]
x_train,y_train,x_test,y_test = train_test_split(x,y,test_size=0.8,random_state=42)
         
model = LinearRegression()
model.fit(x_train,y_train)
else:
    st.warning("Please upload your dataset for model training.")
