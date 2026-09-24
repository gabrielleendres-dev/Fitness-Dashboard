import os
import sqlite3
import hashlib
import html
from datetime import date, datetime
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Studio Sanctuary",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DARK ESPRESSO / BURGUNDY DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');

    :root {
        --background: #211719;
        --background-deep: #160f11;
        --sidebar: #2b1c1d;
        --surface: #382526;
        --surface-light: #493133;
        --surface-soft: #302021;
        --border: #68484a;
        --espresso: #f7eee5;
        --cream: #f4e4d3;
        --pink: #e7b8b7;
        --rose: #d89198;
        --muted: #c9aead;
        --gold: #d8b27c;
        --sage: #b7c8ae;
        --danger: #e6a2a2;
    }

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: var(--espresso);
    }

    .stApp {
        background: var(--background) !important;
        color: var(--espresso) !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"] {
        background: var(--background) !important;
    }

    section[data-testid="stSidebar"] {
        background: var(--sidebar) !important;
        border-right: 1px solid var(--border);
    }

    h1, h2, h3, h4 {
        color: var(--cream) !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 600 !important;
    }

    .brand {
        color: var(--cream);
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.3rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .eyebrow {
        color: var(--pink) !important;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    .subtitle {
        color: var(--muted) !important;
        font-size: 0.9rem;
        margin-top: -18px;
        margin-bottom: 20px;
    }

    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 22px;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    .card-title {
        color: var(--cream) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.65rem;
        font-weight: 600;
    }

    .card-meta {
        color: var(--muted) !important;
        font-size: 0.78rem;
        line-height: 1.8;
    }

    .stButton > button {
        background: var(--rose) !important;
        border: 1px solid var(--rose) !important;
        border-radius: 0 !important;
        color: #241719 !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        min-height: 42px;
        text-transform: uppercase;
    }

    div[data-testid="stForm"],
    [data-testid="stExpander"] {
        background: var(--surface-soft) !important;
        border: 1px solid var(--border) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATABASE
# =========================================================

DB_FILE = "assistant_dashboard.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Not Started',
            due_date TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT,
            category TEXT,
            notes TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trigger_event TEXT,
            action_type TEXT,
            action_data TEXT,
            is_active BOOLEAN DEFAULT 1
        )
    """)
    # (Simplified initialization for brevity - add other tables similarly)
    connection.commit()
    connection.close()


def query_database(query, parameters=(), fetch=False):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    if fetch:
        result = cursor.fetchall()
        connection.close()
        return result
    connection.commit()
    connection.close()
    return True


initialize_database()


# =========================================================
# AUTHENTICATION
# =========================================================

def check_password():
    if st.session_state.get("authenticated", False):
        return True

    password = st.text_input("Password", type="password")
    if st.button("Enter"):
        # Replace with your secure hashing logic
        if password == st.secrets.get("APP_PASSWORD", "dev"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    return False


if not check_password():
    st.stop()


# =========================================================
# HELPERS
# =========================================================

def format_date(value):
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime("%B %d, %Y")
    except:
        return str(value)


def safe_html(text):
    return html.escape(str(text or "")).replace("\n", "<br>")


# =========================================================
# PAGES
# =========================================================

def show_overview():
    st.title("Today's Agenda")
    today = date.today().isoformat()
    
    # Query tasks due today or overdue
    tasks = query_database(
        "SELECT * FROM tasks WHERE status != 'Done' AND (due_date <= ? OR due_date IS NULL) ORDER BY due_date ASC",
        (today,),
        fetch=True
    )
    
    if not tasks:
        st.info("Nothing urgent for today. Focus on your goals.")
    else:
        for task in tasks:
            st.markdown(f'<div class="card"><div class="card-title">{safe_html(task["title"])}</div><div class="card-meta">Due: {format_date(task["due_date"])}</div></div>', unsafe_allow_html=True)


def show_automation():
    st.title("Automation Center")
    st.markdown("Define rules to automate your workflow.")
    
    with st.form("new_rule"):
        trigger = st.selectbox("Trigger", ["Task Added", "Client Added", "Event Added"])
        action = st.text_input("Action (e.g., Create Follow-up Task)")
        if st.form_submit_button("Save Rule"):
            query_database("INSERT INTO automation_rules (trigger_event, action_type) VALUES (?, ?)", (trigger, action))
            st.success("Rule saved.")
            st.rerun()

    rules = query_database("SELECT * FROM automation_rules", fetch=True)
    for rule in rules:
        st.write(f"When **{rule['trigger_event']}** → Then **{rule['action_type']}**")


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown('<div class="brand">Sanctuary</div>', unsafe_allow_html=True)
    page = st.radio("Navigate", ["Overview", "Tasks", "Calendar", "Automation"])
    if st.button("Lock"):
        st.session_state.authenticated = False
        st.rerun()

# Routing
if page == "Overview": show_overview()
elif page == "Automation": show_automation()
# ... Add other page functions (show_tasks, show_calendar) here as before
