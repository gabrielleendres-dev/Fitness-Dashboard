import sqlite3
from datetime import date, datetime

import pandas as pd
import streamlit as st


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="My Personal Assistant",
    page_icon="🤍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PILATES-INSPIRED DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');

    :root {
        --cream: #F8F4EF;
        --warm-white: #FFFDFC;
        --brown: #6F5548;
        --dark-brown: #49382F;
        --taupe: #B7A497;
        --pink: #DDB9B5;
        --light-pink: #F2DFDC;
        --line: #E5DAD2;
    }

    .stApp {
        background-color: var(--cream);
        color: var(--dark-brown);
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--dark-brown) !important;
    }

    h1 {
        font-size: 2.5rem !important;
    }

    [data-testid="stSidebar"] {
        background-color: #EDE3DB;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: var(--dark-brown) !important;
    }

    .stButton > button {
        background-color: var(--brown);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: var(--dark-brown);
        color: white;
    }

    div[data-testid="stMetric"] {
        background-color: var(--warm-white);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(90, 65, 50, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--brown);
    }

    div[data-testid="stMetricValue"] {
        color: var(--dark-brown);
    }

    [data-testid="stExpander"] {
        background-color: var(--warm-white);
        border: 1px solid var(--line);
        border-radius: 12px;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div,
    .stDateInput input,
    .stNumberInput input {
        border-radius: 8px;
    }

    .brand-note {
        color: var(--brown);
        font-size: 0.9rem;
        letter-spacing: 0.03em;
    }

    .welcome-card {
        background-color: var(--light-pink);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        border: 1px solid var(--pink);
    }

    hr {
        border-color: var(--line);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PASSWORD PROTECTION
# =========================================================

def check_password():
    """Show the password screen until the correct password is entered."""

    if st.session_state.get("authenticated", False):
        return True

    st.markdown(
        """
        <div class="welcome-card">
            <h2>Welcome to your private assistant</h2>
            <p>Enter your passcode to continue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "Passcode",
        type="password",
        key="login_password",
    )

    if st.button("Unlock Dashboard", type="primary"):
        try:
            correct_password = st.secrets["APP_PASSWORD"]
        except Exception:
            correct_password = None

        if not correct_password:
            st.error(
                "APP_PASSWORD has not been added yet. "
                "Add it under your Streamlit app's Secrets settings."
            )
            return False

        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect passcode.")

    st.caption("This dashboard is private.")
    return False


if not check_password():
    st.stop()


# =========================================================
# DATABASE
# =========================================================

DB_NAME = "assistant_dashboard.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            due_date TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Not Started',
            completed INTEGER DEFAULT 0
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            status TEXT,
            notes TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            target_date TEXT,
            progress INTEGER DEFAULT 0
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT,
            event_time TEXT,
            category TEXT,
            notes TEXT
        )
        """
    )

    # Upgrade older versions of the tasks table automatically.
    cursor.execute("PRAGMA table_info(tasks)")
    task_columns = [column[1] for column in cursor.fetchall()]

    if "status" not in task_columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'Not Started'"
        )

    # Keep older completed tasks consistent with their status.
    cursor.execute(
        """
        UPDATE tasks
        SET status = 'Done'
        WHERE completed = 1
        """
    )

    connection.commit()
    connection.close()


initialize_database()


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def add_task(title, category, due_date, priority, status):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO tasks
        (title, category, due_date, priority, status, completed)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            category,
            str(due_date),
            priority,
            status,
            1 if status == "Done" else 0,
        ),
    )
    connection.commit()
    connection.close()


def complete_task(task_id):
    connection = get_connection()
    connection.execute(
        """
        UPDATE tasks
        SET completed = 1, status = 'Done'
        WHERE id = ?
        """,
        (task_id,),
    )
    connection.commit()
    connection.close()


def add_client(name, email, phone, status, notes):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO clients (name, email, phone, status, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, phone, status, notes),
    )
    connection.commit()
    connection.close()


def add_goal(title, category, target_date, progress):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO goals (title, category, target_date, progress)
        VALUES (?, ?, ?, ?)
        """,
        (title, category, str(target_date), progress),
    )
    connection.commit()
    connection.close()


def add_event(title, event_date, event_time, category, notes):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO events
        (title, event_date, event_time, category, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, str(event_date), event_time, category, notes),
    )
    connection.commit()
    connection.close()


def read_table(table_name):
    allowed_tables = {"tasks", "clients", "goals", "events"}

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    connection = get_connection()
    data = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        connection,
    )
    connection.close()
    return data


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <h2 style="font-family: 'Playfair Display', serif;">
    🤍 My Assistant
    </h2>
    <p class="brand-note">Personal • Focused • Organized</p>
    """,
    unsafe_allow_html=True,
)

if st.sidebar.button("Lock Dashboard"):
    st.session_state.authenticated = False
    st.rerun()

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Tasks",
        "Calendar",
        "Clients",
        "Goals",
        "Message Templates",
    ],
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("Personal + Executive Assistant")
            
