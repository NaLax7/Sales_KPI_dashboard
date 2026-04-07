# Universal Data Analytics Dashboard

**Live Demo:** https://saleskpidashboard-rq23hjmsflmy8xjeucnv5f.streamlit.app/

![App Demo]([DRAG_AND_DROP_YOUR_GIF_HERE])

- Overview
This is a dynamic, high-performance web application designed to democratize data analysis. Instead of relying on hardcoded column names or specific datasets, this "universal" dashboard allows users to upload **any** standard CSV or Excel file and instantly generate insights. 

It acts as a lightweight alternative to heavy BI tools like Tableau or PowerBI, offering an intuitive, centered UI and dynamic chart generation.

- Key Features
* **Universal File Support:** Accepts both `.csv` and `.xlsx` / `.xls` files.
* **Dynamic Data Mapping:** Automatically detects numeric vs. categorical columns, allowing the user to map their own X and Y axes on the fly.
* **High-Performance Caching:** Utilizes Streamlit's `@st.cache_data` to store data in memory, ensuring the app remains lightning-fast even when processing large datasets.
* **Interactive Visualizations:** Powered by `plotly`, featuring:
  * Automated KPI generation.
  * Full-width Time Series / Trend Lines.
  * Categorical Bar and Donut charts.
  * Scatter Plots for deep-dive correlation analysis.
* **Custom UI:** Features a custom CSS-injected file dropzone and a fully responsive, wide-grid dashboard layout.

- Tech Stack
* **Language:** Python
* **Data Manipulation:** `pandas`, `openpyxl`
* **Data Visualization:** `plotly`
* **Web Framework & Hosting:** `Streamlit` / Streamlit Community Cloud

- Data Requirements
To get the best results out of this dashboard, your uploaded dataset should follow three simple rules:
1. It must be a standard `.csv` or `.xlsx` file.
2. It must contain at least one column with **numeric** data to generate metrics.
3. It should have a standard table structure with headers in the first row.

- How to Run Locally
If you want to run this project on your own machine:
1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/Sales_KPI_dashboard.git](https://github.com/YOUR_GITHUB_USERNAME/Sales_KPI_dashboard.git)
