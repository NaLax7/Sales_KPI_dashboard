import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. WIDE LAYOUT ---
st.set_page_config(
    page_title="Universal Data Dashboard", 
    page_icon=":bar_chart:", 
    layout="wide" 
)

# ------------------------------------------------------------------
# --- CUSTOM CSS INJECTION ---
# ------------------------------------------------------------------
st.markdown("""
<style>
    .stMarkdown, .stTitle, .stSubheader, .stAlert { text-align: center; justify-content: center; }
    .dashboard-title { font-size: 40px !important; font-weight: 700 !important; margin-bottom: 5px !important; color: #333; }
    .dashboard-subtitle { font-size: 18px !important; color: #666; margin-bottom: 0px !important; }
    .dashboard-attribution { font-size: 14px !important; color: #888; margin-bottom: 30px !important; }

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
    [data-testid="stFileUploaderDropzone"]:hover { background-color: #D93F34 !important; }
    [data-testid="stFileUploaderDropzone"] button, [data-testid="stFileUploaderDropzone"] small, [data-testid="stFileUploaderDropzone"] div { display: none !important; }
    [data-testid="stFileUploaderDropzone"]::after {
        content: "Select CSV or Excel file";
        color: white; font-size: 20px; font-weight: 700; text-align: center; width: 100%;
    }
    .stMetric { background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# --- HEADER & UPLOADER ---
# ------------------------------------------------------------------
st.markdown('<p class="dashboard-title">Universal Data Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-subtitle">Upload ANY dataset to generate instant insights.</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["csv", "xlsx", "xls"]) 

if uploaded_file is None:
    st.stop() 

# --- NEW: CACHING THE DATA (Lightning Fast!) ---
# This decorator tells Streamlit to save the data in memory after the first load
@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)

try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

all_columns = df.columns.tolist()
numeric_columns = df.select_dtypes(include='number').columns.tolist()

if not numeric_columns:
    st.error("Your dataset must contain at least one column with numbers to generate KPIs!")
    st.stop()

st.divider()

# ------------------------------------------------------------------
# --- 2. DYNAMIC COLUMN MAPPING ---
# ------------------------------------------------------------------
st.markdown("### ⚙️ 1. Map Your Data")
map_col1, map_col2, map_col3 = st.columns(3)

with map_col1:
    cat_col = st.selectbox("Select your Category/Text column:", all_columns, index=0)
with map_col2:
    val_col = st.selectbox("Select your Value/Metric column (Numbers):", numeric_columns, index=0)
with map_col3:
    date_col = st.selectbox("Select your Date column (Optional):", ["None"] + all_columns, index=0)

# --- GLOBAL FILTER ---
st.markdown("### 🔍 2. Filter Data")
_, filter_mid, _ = st.columns([1, 2, 1])
with filter_mid:
    unique_categories = df[cat_col].unique()
    selected_cats = st.multiselect(f"Filter by {cat_col}:", options=unique_categories, default=unique_categories, label_visibility="collapsed")

filtered_df = df[df[cat_col].isin(selected_cats)]

if filtered_df.empty:
    st.warning("No data selected to display.")
    st.stop()

st.divider()

# ------------------------------------------------------------------
# --- 3. WIDE DASHBOARD GRID LAYOUT ---
# ------------------------------------------------------------------
st.subheader(f"📊 Analyzing {val_col} grouped by {cat_col}")

# -- ROW 1: KPIs --
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_val = filtered_df[val_col].sum()
avg_val = filtered_df[val_col].mean()
max_val = filtered_df[val_col].max()
total_rows = len(filtered_df)

kpi1.metric(label=f"Total {val_col}", value=f"{total_val:,.2f}")
kpi2.metric(label=f"Average {val_col}", value=f"{avg_val:,.2f}")
kpi3.metric(label=f"Max {val_col}", value=f"{max_val:,.2f}")
kpi4.metric(label="Total Records", value=total_rows)

st.divider()

# -- ROW 2: FULL WIDTH LINE CHART --
if date_col != "None":
    trend_data = filtered_df.groupby(date_col)[val_col].sum().reset_index()
    trend_data = trend_data.sort_values(by=date_col) 
    fig_line = px.line(trend_data, x=date_col, y=val_col, markers=True, title=f"{val_col} Trend over Time", template="simple_white")
    st.plotly_chart(fig_line, use_container_width=True)
    st.divider()

# -- ROW 3: CATEGORY CHARTS --
chart1, chart2 = st.columns(2)

with chart1:
    bar_data = filtered_df.groupby(cat_col)[val_col].sum().reset_index().sort_values(by=val_col, ascending=False).head(10)
    fig_bar = px.bar(bar_data, x=cat_col, y=val_col, text_auto=True, color=cat_col, title=f"Top 10 {cat_col} by {val_col}", template="simple_white")
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with chart2:
    pie_data = filtered_df.groupby(cat_col)[val_col].sum().reset_index()
    fig_pie = px.pie(pie_data, names=cat_col, values=val_col, hole=0.4, title=f"Distribution of {val_col} across {cat_col}", template="simple_white")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# -- NEW: ROW 4: SCATTER PLOT (CORRELATION) --
# Only show this section if the dataset has at least 2 numeric columns to compare
if len(numeric_columns) >= 2:
    st.markdown("### 🔬 Deep Dive: Correlation Analysis")
    st.markdown("<p style='text-align: center; color: #666;'>See how two different metrics relate to one another.</p>", unsafe_allow_html=True)
    
    scat_col1, scat_col2 = st.columns(2)
    with scat_col1:
        x_axis = st.selectbox("X-Axis Metric:", numeric_columns, index=0)
    with scat_col2:
        y_axis = st.selectbox("Y-Axis Metric:", numeric_columns, index=1)
        
    fig_scatter = px.scatter(
        filtered_df, 
        x=x_axis, 
        y=y_axis, 
        color=cat_col, 
        opacity=0.7,
        title=f"Correlation: {x_axis} vs {y_axis}", 
        template="simple_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.divider()

# -- ROW 5: RAW DATA --
st.markdown("### 🗃️ Raw Data View")
st.dataframe(filtered_df, use_container_width=True)