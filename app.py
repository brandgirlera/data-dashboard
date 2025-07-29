import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Analyzer", layout="wide")
st.title("📊 Upload Your Data for Instant Insights")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview of Your Data")
    st.dataframe(df.head())

    st.subheader("Basic Stats")
    st.write(df.describe())

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        st.subheader("Interactive Scatter Plot")
        x_col = st.selectbox("X-axis", numeric_cols)
        y_col = st.selectbox("Y-axis", numeric_cols, index=1)
        fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)

    if len(numeric_cols) > 1:
        st.subheader("Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
