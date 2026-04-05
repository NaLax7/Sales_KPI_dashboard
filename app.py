import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sales Dashboard", 
    page_icon=":bar_chart:", 
    layout="centered" 
)

# ------------------------------------------------------------------
# --- CUSTOM CSS INJECTION ---
# ------------------------------------------------------------------
st.markdown("""
<style>
    .stMarkdown, .stTitle, .stSubheader, .stAlert {
        text-align: center;
        justify-content: center;
    }

    .dashboard-title {
        font-size: 40px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
        color: #333;
    }
    .dashboard-subtitle {
        font-size: 18px !important;
        color: #666;
        margin-bottom: 0px !important;
    }
    .dashboard-attribution {
        font-size: 14px !important;
        color: #888;
        margin-bottom: 30px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #E24A3F !important;
        border: 2px solid #D93F34 !important;
        border-radius: 12px !important;
        padding: 20px !important; 
        max-width: 350px !important; 
        margin: 0 auto !important; 
        display: flex !important; 
        justify-content: center !important; 
        align-items: center !important; 
        min-height: 80px !important;
        transition: background-color 0.2s;
        cursor: pointer;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background-color: #D93F34 !important;
    }

    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] div {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzone"]::after {
        content: "Select CSV file";
        color: white;
        font-size: 20px;
        font-weight: 700;
        text-align: center;
        width: 100%;
    }

    .stMetric {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# --- DASHBOARD LAYOUT & CONTENT ---
# ------------------------------------------------------------------

st.markdown('<p class="dashboard-title">Interactive Sales & KPI Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-subtitle">Analyze your custom sales data instantly.</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-attribution">Powered by Python & Streamlit.</p>', unsafe_allow_html=True)

st.info("⚠️ *Your CSV file must contain the following exact column names: `Date`, `Product`, `Category`, `Revenue`, and `Units_Sold`.*")

uploaded_file = st.file_uploader("", type=["csv"]) 

if uploaded_file is None:
    st.markdown('<p style="text-align: center; color: #888; font-size: 14px; margin-top: 10px;">or drop CSV data here</p>', unsafe_allow_html=True)
    st.stop() 

# --- READ THE DATA ---
df = pd.read_csv(uploaded_file)
st.success("Custom data loaded successfully!")
st.divider()

# Get all unique categories for our dropdowns
all_categories = df["Category"].unique()

# --- 1. OVERALL KPIs (Always shows total data) ---
st.subheader("Overall Key Performance Indicators")
col1, col2, col3 = st.columns(3)

total_revenue = df['Revenue'].sum()
total_units = df['Units_Sold'].sum()
avg_price = total_revenue / total_units if total_units > 0 else 0

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="Total Units Sold", value=total_units)
with col3:
    st.metric(label="Avg Price per Unit", value=f"${avg_price:,.2f}")

st.divider()

# --- 2. LINE CHART (With its own filter) ---
st.subheader("Sales Trend")
line_categories = st.multiselect(
    "Filter Trend by Category:", 
    options=all_categories, 
    default=all_categories, 
    key="line_filter" # <-- Unique ID!
)

line_df = df[df["Category"].isin(line_categories)]

if line_df.empty:
    st.warning("Please select at least one category to view the trend.")
else:
    daily_revenue = line_df.groupby("Date")["Revenue"].sum().reset_index()
    fig_line = px.line(daily_revenue, x="Date", y="Revenue", markers=True, title="Daily Revenue", template="simple_white")
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# --- 3. SIDE-BY-SIDE BAR CHARTS (Each with its own filter) ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### Revenue by Category")
    cat_categories = st.multiselect(
        "Select Categories to compare:", 
        options=all_categories, 
        default=all_categories, 
        key="cat_filter" # <-- Unique ID!
    )
    
    cat_df = df[df["Category"].isin(cat_categories)]
    
    if cat_df.empty:
        st.warning("Please select a category.")
    else:
        category_revenue = cat_df.groupby("Category")["Revenue"].sum().reset_index()
        fig_cat = px.bar(category_revenue, x="Category", y="Revenue", text_auto=True, color="Category", title="", template="simple_white") 
        fig_cat.update_layout(showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

with chart_col2:
    st.markdown("### Top Products")
    prod_categories = st.multiselect(
        "Filter products by Category:", 
        options=all_categories, 
        default=all_categories, 
        key="prod_filter" # <-- Unique ID!
    )
    
    prod_df = df[df["Category"].isin(prod_categories)]
    
    if prod_df.empty:
        st.warning("Please select a category.")
    else:
        product_revenue = prod_df.groupby("Product")["Revenue"].sum().reset_index().sort_values(by="Revenue", ascending=True)
        fig_prod = px.bar(product_revenue, x="Revenue", y="Product", orientation='h', text_auto=True, title="", template="simple_white") 
        st.plotly_chart(fig_prod, use_container_width=True)

st.divider()

# --- 4. RAW DATA ---
st.subheader("Raw Sales Data")
st.dataframe(df, use_container_width=True)