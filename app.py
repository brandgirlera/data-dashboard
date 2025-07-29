import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------ COLORS ------------------
colors = ["#F5DDD8", "#ECC5C1", "#DAB5B0", "#CE9F9C", "#B78B86", "#9C6F6A"]

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Data Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #F5DDD8, #ECC5C1);
}
header, footer {visibility: hidden;}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
.header {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #9C6F6A;
    margin-bottom: 20px;
}
.card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    font-size: 14px;
    color: #9C6F6A;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown(
    """
    <div class="header">
        <img src="https://raw.githubusercontent.com/brandgirlera/data-dashboard/main/logo.png" width="80">
        <div>My Data Dashboard</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.size == 0:
            st.error("Uploaded file is empty!")
            st.stop()

        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # ------------------ PREVIEW ------------------
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Preview of Your Data")
        st.dataframe(df.head())
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ BASIC STATS ------------------
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Basic Stats")
        st.write(df.describe())
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ SELECT COLUMNS ------------------
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) >= 2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Scatter Plot")
            x_col = st.selectbox("X-axis", numeric_cols)
            y_col = st.selectbox("Y-axis", numeric_cols, index=1)

            fig = px.scatter(df, x=x_col, y=y_col, trendline="ols",
                             color_discrete_sequence=colors)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ------------------ BAR CHART ------------------
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Bar Chart")
            fig_bar = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=colors)
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ------------------ PIE CHART ------------------
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Pie Chart")
            fig_pie = px.pie(df, names=x_col, values=y_col, color_discrete_sequence=colors)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ------------------ HEATMAP ------------------
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Correlation Heatmap")
            corr = df[numeric_cols].corr()
            fig_hm, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap=sns.color_palette(colors, as_cmap=True), ax=ax)
            st.pyplot(fig_hm)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Not enough numeric columns for visualizations.")

# ------------------ FOOTER ------------------
st.markdown('<div class="footer">Built with Streamlit</div>', unsafe_allow_html=True)
