import streamlit as st
from matplotlib import pyplot as plt

st.title('Mobile Sales Analysis Dashboard')

# --- Plot 1: Line Chart ---
st.header('Days vs Sales')
# Create figure object
fig1, ax1 = plt.subplots()
ax1.plot([1,2,3,4,5],[21,34,45,65,76], label='Sales Trend')
ax1.set_xlabel('Days')
ax1.set_ylabel('Sales count')
ax1.set_title('Mobile Sales Analysis')
ax1.grid()
ax1.legend()
# Display in Streamlit
st.pyplot(fig1)

# --- Plot 2: Bar Chart ---
st.header('5th Day Sales Analysis')
fig2, ax2 = plt.subplots()
ax2.bar(['Iphone','Samsung','Oppo','Vivo','Nokia'],[19,30,8,15,6])
ax2.set_title('5th Day Sales analysis')
ax2.set_xlabel('Mobile')
ax2.set_ylabel('Sales Count')
# Display in Streamlit
st.pyplot(fig2)

# --- Plot 3: Pie Chart ---
st.header('Sales Distribution')
fig3, ax3 = plt.subplots()
ax3.pie([19,30,8,15,6],labels=['Iphone','Samsung','Oppo','Vivo','Nokia'],autopct='%1.1f%%')
ax3.set_title('Mobile Sales Analysis')
# Display in Streamlit
st.pyplot(fig3)
