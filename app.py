import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(page_title="Data Dashboard", layout="wide")

# PINK BACKGROUND STYLE
st.markdown("""
    <style>
    .main {
        background: linear-gradient(120deg, #fbd3e9 0%, #bb377d 100%);
        color: #2c2c2c;
        padding: 2rem;
    }
    .stApp {
        background: linear-gradient(120deg, #fbd3e9 0%, #bb377d 100%);
    }
    .block-container {
        background-color: rgba(255,255,255,0.75);
        border-radius: 12px;
        padding: 2rem;
    }
    .card {
        background: rgba(255,255,255,0.85);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# APP TITLE
st.title("Upload Your Data for Instant Insights")

# FILE UPLOAD
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Preview of Your Data")
    st.dataframe(df.head())
    st.markdown('</div>', unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Basic Stats")
    st.dataframe(df.describe(include='all'))
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart type selector
    st.subheader("Choose Visualizations")
    chart_types = st.multiselect(
        "Select chart types to display:",
        ["Scatter Plot", "Bar Chart", "Line Chart", "Pie Chart", "Correlation Heatmap"]
    )

    numeric_cols = df.select_dtypes(include='number').columns
    all_cols = df.columns

    for chart in chart_types:
        if chart == "Scatter Plot":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Scatter Plot")
            x_col = st.selectbox("X-axis (scatter)", numeric_cols, key="scatx")
            y_col = st.selectbox("Y-axis (scatter)", numeric_cols, key="scaty")
            fig = px.scatter(df, x=x_col, y=y_col, trendline="ols")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif chart == "Bar Chart":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Bar Chart")
            x_col = st.selectbox("X-axis (bar)", all_cols, key="barx")
            y_col = st.selectbox("Y-axis (bar)", numeric_cols, key="bary")
            fig = px.bar(df, x=x_col, y=y_col)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif chart == "Line Chart":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Line Chart")
            x_col = st.selectbox("X-axis (line)", all_cols, key="linx")
            y_col = st.selectbox("Y-axis (line)", numeric_cols, key="liny")
            fig = px.line(df, x=x_col, y=y_col)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif chart == "Pie Chart":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Pie Chart")
            category = st.selectbox("Category (pie)", all_cols, key="piecat")
            value = st.selectbox("Values (pie)", numeric_cols, key="pieval")
            fig = px.pie(df, names=category, values=value)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif chart == "Correlation Heatmap":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Correlation Heatmap")
            corr = df.corr(numeric_only=True)
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.write("Upload a CSV to start.")
