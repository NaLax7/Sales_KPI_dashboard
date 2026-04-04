import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("Interactive Sales & KPI Dashboard 📊")

# Load the data
df = pd.read_csv("sales_data.csv")

# Calculate KPIs
total_revenue = df["Revenue"].sum()
total_units = df["Units_Sold"].sum()

# Display KPIs in Columns
st.subheader("Key Performance Indicators")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,}")
    
with col2:
    st.metric(label="Total Units Sold", value=total_units)

st.divider()

# --- NEW: Interactive Bar Chart ---
st.subheader("Revenue by Category")

# Group the data by category
category_revenue = df.groupby("Category")["Revenue"].sum().reset_index()

# Create the bar chart
fig = px.bar(
    category_revenue, 
    x="Category", 
    y="Revenue", 
    text_auto=True, 
    color="Category",
    title="Total Revenue per Category"
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Display the raw data table at the bottom
st.subheader("Raw Sales Data")
st.dataframe(df)