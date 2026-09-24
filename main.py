import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Studio Sanctuary",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN / CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');

    :root {
        --warm-white: #FDFBF8;
        --soft-beige: #F5F2EF;
        --light-taupe: #E7DED7;
        --clay: #B8A89C;
        --deep-brown: #51453D;
        --charcoal: #3D3935;
        --pink: #D9B9B5;
        --dark-pink: #A9827D;
        --white: #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: var(--charcoal);
    }

    .stApp {
        background-color: var(--warm-white);
    }

    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--deep-brown) !important;
        letter-spacing: 0.02em;
    }

    h1 {
        font-size: 3rem !important;
        font-weight: 600 !important;
    }

    h2 {
        font-size: 2.2rem !important;
        font-weight: 600 !important;
    }

    h3 {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--soft-beige);
        border-right: 1px solid var(--light-taupe);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--deep-brown) !important;
    }

    .brand-mark {
        padding: 18px 0 28px 0;
        border-bottom: 1px solid var(--light-taupe);
        margin-bottom: 25px;
    }

    .brand-mark .small {
        font-size: 0.72rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: var(--dark-pink);
        font-weight: 600;
    }

    .brand-mark .large {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.1rem;
        color: var(--deep-brown);
        line-height: 1.05;
        margin-top: 6px;
    }

    .hero {
        background-color: var(--soft-beige);
        padding: 34px 38px;
        border-left: 5px solid var(--pink);
        margin-bottom: 28px;
    }

    .hero-label {
        color: var(--dark-pink);
        font-size: 0.75rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .hero-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3rem;
        color: var(--deep-brown);
        line-height: 1.05;
    }

    .hero-text {
        color: #6B625C;
        margin-top: 12px;
        font-size: 0.95rem;
    }

    .metric-card {
        background-color: var(--white);
        border: 1px solid var(--light-taupe);
        padding: 22px;
        min-height: 120px;
    }

    .metric-number {
        font-family: 'Cormorant Garamond', serif;
        color: var(--deep-brown);
        font-size: 2.6rem;
        line-height: 1;
    }

    .metric-label {
        color: #746A63;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-top: 10px;
    }

    .section-label {
        color: var(--dark-pink);
        font-size: 0.72rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-weight: 700;
        margin: 30px 0 10px 0;
    }

    .stButton > button {
        border-radius: 0;
        border: 1px solid var(--deep-brown);
        background-color: var(--deep-brown);
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.65rem 1.1rem;
    }

    .stButton > button:hover {
        background-color: var(--dark-pink);
        border-color: var(--dark-pink);
        color: whit
