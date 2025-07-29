import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Data Insight Dashboard", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #fde2e2 0%, #f7d9d9 100%);
        }
        .main {
            background: transparent;
        }
        div[data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.0);
        }
        .card {
            background-color: white;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📈 Data Insight Dashboard")
st.markdown("Upload a CSV to see charts and explore visually.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    # Let user choose section order
    sections = [
        "Small Charts",
        "Main Scatter Plot",
        "Parameters",
        "Correlation Heatmap"
    ]

    order = st.multiselect(
        "Choose the order of sections (drag to reorder):",
        options=sections,
        default=sections
    )

    # Create columns for layout
    left_col, mid_col, right_col = st.columns([1, 3, 1])

    # Render sections in chosen order
    for section in order:
        if section == "Small Charts":
            with left_col:
                st.markdown('<div class="card">Small Charts</div>', unsafe_allow_html=True)
                if len(numeric_cols) >= 2:
                    fig_small1 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
                    st.plotly_chart(fig_small1, use_container_width=True, height=200)

                    fig_small2 = px.line(df, x=numeric_cols[0], y=numeric_cols[1])
                    st.plotly_chart(fig_small2, use_container_width=True, height=200)

        elif section == "Main Scatter Plot":
            with mid_col:
                st.markdown('<div class="card"><h3 style="text-align:center;">Scatter Plot</h3></div>', unsafe_allow_html=True)
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("X-axis", numeric_cols, key="x_mid")
                    y_col = st.selectbox("Y-axis", numeric_cols, key="y_mid", index=1)
                    # trendline="ols" requires statsmodels installed
                    try:
                        fig = px.scatter(df, x=x_col, y=y_col, trendline="ols")
                    except Exception:
                        fig = px.scatter(df, x=x_col, y=y_col)
                    st.plotly_chart(fig, use_container_width=True)

        elif section == "Parameters":
            with right_col:
                st.markdown('<div class="card"><b>Parameters</b></div>', unsafe_allow_html=True)
                st.write(df.describe())

        elif section == "Correlation Heatmap":
            with right_col:
                st.markdown('<div class="card"><b>Correlation Heatmap</b></div>', unsafe_allow_html=True)
                if len(numeric_cols) > 1:
                    corr = df[numeric_cols].corr()
                    fig_corr = px.imshow(corr, text_auto=True)
                    st.plotly_chart(fig_corr, use_container_width=True)
