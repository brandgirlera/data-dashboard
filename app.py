import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Dashboard", layout="wide")

# --- HEADER ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #FDDDE6 0%, #FCC6E2 100%);
    }
    .main {
        background-color: rgba(255,255,255,0.6);
        border-radius: 15px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("Upload Your Data – Multi-Chart Dashboard")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview of Your Data")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # --- CHART SELECTION ---
    st.sidebar.title("Chart Options")
    chart_types = st.sidebar.multiselect(
        "Select charts to display",
        ["Scatter", "Bar", "Line", "Heatmap", "Pie"]
    )

    # --- CHART PARAMETERS ---
    x_col = st.sidebar.selectbox("X-axis", df.columns)
    y_col = st.sidebar.selectbox("Y-axis", numeric_cols) if numeric_cols else None

    # --- LAYOUT FOR CHARTS ---
    col1, col2 = st.columns(2)

    # --- SCATTER ---
    if "Scatter" in chart_types and x_col and y_col:
        with col1:
            st.subheader("Scatter Plot")
            fig = px.scatter(df, x=x_col, y=y_col, trendline="ols")
            st.plotly_chart(fig, use_container_width=True)

    # --- BAR ---
    if "Bar" in chart_types and x_col and y_col:
        with col2:
            st.subheader("Bar Chart")
            fig = px.bar(df, x=x_col, y=y_col)
            st.plotly_chart(fig, use_container_width=True)

    # --- LINE ---
    if "Line" in chart_types and x_col and y_col:
        with col1:
            st.subheader("Line Chart")
            fig = px.line(df, x=x_col, y=y_col)
            st.plotly_chart(fig, use_container_width=True)

    # --- PIE ---
    if "Pie" in chart_types and x_col and y_col:
        with col2:
            st.subheader("Pie Chart")
            fig = px.pie(df, names=x_col, values=y_col)
            st.plotly_chart(fig, use_container_width=True)

    # --- HEATMAP ---
    if "Heatmap" in chart_types and len(numeric_cols) >= 2:
        st.subheader("Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

else:
    st.info("Upload a CSV file to get started.")
