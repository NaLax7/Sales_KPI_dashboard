import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration - Crucial for centering!
st.set_page_config(
    page_title="Sales Dashboard", 
    page_icon=":bar_chart:", 
    layout="centered" # Changed from wide to centered
)

# ------------------------------------------------------------------
# --- CUSTOM CSS INJECTION (This makes it look like the image) ---
# ------------------------------------------------------------------
st.markdown("""
<style>
    /* 1. Center all text by default */
    .stMarkdown, .stTitle, .stSubheader, .stAlert, .stFileUploader {
        text-align: center;
        justify-content: center;
    }

    /* 2. Custom Styling for the Title Stack (like the image) */
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

    /* 3. STYLING THE FILE UPLOADER BOX (to mimic the red button) */
    /* Target the main dropzone container */
    .stFileUploader {
        border: none !important;
    }
    
    .stFileUploader > div > button {
        /* Hide the default tiny standard 'Browse' button */
        display: none !important;
    }

    .stFileUploader > div[data-testid="stFileUploaderDropzone"] {
        /* The main large gray box from the target image */
        background-color: #E24A3F !important; /* Bold Red/Orange from image */
        border: 2px solid #D93F34 !important; /* Slightly darker border */
        color: white !important; /* Text color inside */
        border-radius: 12px !important; /* Rounded corners */
        padding: 40px !important; /* Make it large and clickable */
        min-height: 150px !important;
        margin-top: -10px !important;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .stFileUploader > div[data-testid="stFileUploaderDropzone"]:hover {
        background-color: #D93F34 !important; /* Slightly darker on hover */
    }

    /* Styling the text *inside* the dropzone */
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] > span {
        color: white !important;
        font-size: 20px !important;
        font-weight: 600 !important;
    }

    /* Change "or drop PDF here" text color to light gray below the button */
    [data-testid="stMarkdownContainer"] p + .stFileUploader + div p {
        color: #888;
        font-size: 14px;
        margin-top: -15px !important;
    }
    
    /* 4. Tidy up the rest of the dashboard components */
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

# Mimicking the Title Stack hierarchy from image_5.png
st.markdown('<p class="dashboard-title">Interactive Sales & KPI Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-subtitle">Analyze your custom sales data instantly.</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-attribution">Powered by Python & Streamlit.</p>', unsafe_allow_html=True)

# Important instruction note, kept outside the styling
st.info("⚠️ *Your CSV file must contain the following exact column names: `Category`, `Revenue`, and `Units_Sold`.*")

# The File Uploader - Custom Styled using CSS above
uploaded_file = st.file_uploader("", type=["csv"]) # No label (we use custom title stack)

# Mimic the "or drop file here" text styling from the image
if uploaded_file is None:
    st.markdown("or drop CSV data here", unsafe_allow_html=True)

# --- Stop the app if no file is uploaded (Same logic as before) ---
if uploaded_file is None:
    st.stop() 

# --- (The rest of the dashboard logic remains the same, just slightly prettier) ---
df = pd.read_csv(uploaded_file)
st.success("Custom data loaded successfully!")
st.divider()

# KPIs
st.subheader("Key Performance Indicators")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Revenue", value=f"${df['Revenue'].sum():,}")
with col2:
    st.metric(label="Total Units Sold", value=df['Units_Sold'].sum())

st.divider()

# Chart
st.subheader("Revenue by Category")
category_revenue = df.groupby("Category")["Revenue"].sum().reset_index()
fig = px.bar(category_revenue, x="Category", y="Revenue", text_auto=True, color="Category", title="Total Revenue per Category", template="simple_white") # used white template
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Raw Data
st.subheader("Raw Sales Data")
st.dataframe(df)