import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Data Insight Dashboard", layout="wide")

# ----------------- CUSTOM STYLE -----------------
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(120deg, #f9d5e5 0%, #fcefee 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 95%;
        }
        .card {
            background-color: white;
            padding: 15px;
            border-radius: 18px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bot
