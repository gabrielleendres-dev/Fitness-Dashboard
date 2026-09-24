import sqlite3
from datetime import date, datetime

import pandas as pd
import streamlit as st


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Studio Sanctuary",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# STUDIO SANCTUARY DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');

    :root {
        --ivory: #F9F6F1;
        --paper: #FFFDF9;
        --espresso: #40332E;
        --brown: #6E5A50;
        --mocha: #806B60;
        --clay: #B59686;
        --rose: #C99C98;
        --blush: #EAD8D2;
        --sand: #D8C8B9;
        --sage: #AEB9A7;
        --line: #E2D7CE;
        --muted: #8B7D74;
        --white: #FFFFFF;
    }

    html,
    body,
    [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: var(--espresso);
    }

    .stApp {
        background-color: var(--ivory);
        color: var(--espresso);
    }

    h1,
    h2,
    h3,
    h4 {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--espresso) !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em;
    }

    h1 {
        font-size: 3rem !important;
        line-height: 1.05 !important;
    }

    h2 {
        font-size: 2.25rem !important;
    }

    h3 {
        font-size: 1.65rem !important;
    }

    p,
    label,
    div,
    span {
        color: var(--espresso);
    }

    [data-testid="stSidebar"] {
        background-color: #EEE5DD;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: var(--espresso) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: var(--line);
    }

    .brand-block {
        padding: 12px 0 26px 0;
        border-bottom: 1px solid var(--line);
        margin-bottom: 24px;
    }

    .brand-eyebrow {
        color: var(--rose) !important;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .brand-title {
        font-family: 'Cormorant Garamond', serif;
        color: var(--espresso) !important;
        font-size: 2.35rem;
        line-height: 0.9;
    }

    .brand-subtitle {
        color: var(--muted) !important;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        margin-top: 12px;
    }

    .stButton > button {
        background-color: var(--espresso);
        color: white !important;
        border: 1px solid var(--espresso);
        border-radius: 0;
        min-height: 2.5rem;
        padding: 0.55rem 1rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background-color: var(--rose);
        border-color: var(--rose);
        color: white !important;
    }

    .stButton > button p {
        color: white !important;
    }

    [data-testid="stMetric"] {
        background-color: var(--paper);
        border: 1px solid var(--line);
        border-radius: 0;
        padding: 20px;
        box-shadow: 0 3px 14px rgba(76, 57, 46, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    [data-testid="stMetricValue"] {
        color: var(--espresso) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.45rem;
    }

    [data-testid="stExpander"] {
        background-color: var(--paper);
        border: 1px solid var(--line);
        border-radius: 0;
    }

    [data-testid="stExpander"] summary p {
        color: var(--espresso) !important;
        font-weight: 600;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div,
    .stDateInput input,
    .stNumberInput input {
        border-radius: 0 !important;
        border-color: var(--line) !important;
        background-color: var(--paper);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
    }

    .hero-card {
        background-color: var(--blush);
        border-left: 5px solid var(--rose);
        padding: 34px 38px;
        margin-bottom: 28px;
    }

    .hero-eyebrow {
        color: var(--mocha) !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-heading {
        color: var(--espresso) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.15rem;
        line-height: 1;
        margin-bottom: 12px;
    }

    .hero-copy {
        color: var(--brown) !important;
        font-size: 0.9rem;
        max-width: 650px;
        line-height: 1.7;
    }

    .section-label {
        color: var(--rose) !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin: 30px 0 10px 0;
    }

    .login-card {
        max-width: 540px;
        margin: 80px auto 20px auto;
        padding: 44px;
        background-color: var(--paper);
        border: 1px solid var(--line);
        border-top: 5px solid var(--rose);
        text-align: center;
    }

    .login-eyebrow {
        color: var(--rose) !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    .login-heading {
        color: var(--espresso) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.7rem;
        margin: 10px 0;
    }

    .login-copy {
        color: var(--muted) !important;
        font-size: 0.85rem;
    }

    .footer {
