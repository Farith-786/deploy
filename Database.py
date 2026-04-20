# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")

# ------------------------------
# CREATE SAMPLE DATA
# ------------------------------
np.random.seed(42)

data = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=120),
    "Region": np.random.choice(["North", "South", "East", "West"], 120),
    "Category": np.random.choice(["Electronics", "Clothing", "Food"], 120),
    "Sales": np.random.randint(1000, 5000, 120),
    "Profit": np.random.randint(200, 1500, 120)
})

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
st.sidebar.header("🔎 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=data["Region"].unique(),
    default=data["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)

filtered_data = data[
    (data["Region"].isin(region_filter)) &
    (data["Category"].isin(category_filter))
]

# ------------------------------
# KPI METRICS
# ------------------------------
total_sales = filtered_data["Sales"].sum()
total_profit = filtered_data["Profit"].sum()
avg_sales = filtered_data["Sales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Avg Sales", f"${avg_sales:,.0f}")

st.divider()

# ------------------------------
# SALES OVER TIME (LINE CHART)
# ------------------------------
st.subheader("📅 Sales Over Time")

sales_by_date = filtered_data.groupby("Date")["Sales"].sum()

fig1, ax1 = plt.subplots()
ax1.plot(sales_by_date.index, sales_by_date.values)
ax1.set_xlabel("Date")
ax1.set_ylabel("Sales")
st.pyplot(fig1)

# ------------------------------
# SALES BY REGION (BAR CHART)
# ------------------------------
st.subheader("🌍 Sales by Region")

sales_region = filtered_data.groupby("Region")["Sales"].sum()

fig2, ax2 = plt.subplots()
ax2.bar(sales_region.index, sales_region.values)
st.pyplot(fig2)

# ------------------------------
# SALES BY CATEGORY (PIE CHART)
# ------------------------------
st.subheader("🥧 Sales by Category")

sales_cat = filtered_data.groupby("Category")["Sales"].sum()

fig3, ax3 = plt.subplots()
ax3.pie(sales_cat.values, labels=sales_cat.index, autopct="%1.1f%%")
st.pyplot(fig3)

# ------------------------------
# DATA TABLE
# ------------------------------
st.subheader("📋 Filtered Data")
st.dataframe(filtered_data)
