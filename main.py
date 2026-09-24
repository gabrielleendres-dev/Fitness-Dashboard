import os
import sqlite3
import hashlib
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

    [data-testid="stHeader"] {
        background: var(--background-deep) !important;
    }

    section[data-testid="stSidebar"] {
        background: var(--sidebar) !important;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] * {
        color: var(--espresso) !important;
    }

    h1, h2, h3, h4 {
        color: var(--cream) !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 600 !important;
    }

    h1 {
        font-size: 3.2rem !important;
        letter-spacing: -0.03em;
    }

    h2 {
        font-size: 2.4rem !important;
    }

    h3 {
        font-size: 1.8rem !important;
    }

    p, label, span, div {
        color: var(--espresso);
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
    }

    .hero {
        background: linear-gradient(135deg, #45292c, #321f22);
        border: 1px solid var(--border);
        padding: 36px;
        margin-bottom: 28px;
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.18);
    }

    .hero-title {
        color: var(--cream);
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.5rem;
        line-height: 1;
        margin: 10px 0 14px 0;
    }

    .hero-copy {
        color: var(--muted) !important;
        font-size: 0.92rem;
        line-height: 1.8;
        max-width: 720px;
    }

    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 22px;
        min-height: 125px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }

    .metric-label {
        color: var(--pink) !important;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .metric-value {
        color: var(--cream) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.9rem;
        line-height: 1;
        margin-top: 14px;
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

    .status-pill {
        display: inline-block;
        padding: 6px 10px;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .status-not-started {
        background: #59494a;
        color: #f4e4d3 !important;
    }

    .status-in-progress {
        background: #80565d;
        color: #ffe9df !important;
    }

    .status-done {
        background: #536451;
        color: #edf4e7 !important;
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

    .stButton > button:hover {
        background: var(--cream) !important;
        border-color: var(--cream) !important;
        color: #241719 !important;
    }

    div[data-testid="stForm"],
    [data-testid="stExpander"] {
        background: var(--surface-soft) !important;
        border: 1px solid var(--border) !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: var(--cream) !important;
    }

    input, textarea, select,
    div[data-baseweb="input"],
    div[data-baseweb="select"],
    div[data-baseweb="textarea"] {
        background-color: #241719 !important;
        color: var(--cream) !important;
        border-color: var(--border) !important;
        border-radius: 0 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #a8898b !important;
    }

    [data-baseweb="select"] * {
        color: var(--cream) !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        color: var(--cream) !important;
    }

    [data-testid="stAlert"] {
        background: var(--surface-light) !important;
        color: var(--cream) !important;
        border: 1px solid var(--border) !important;
    }

    .stProgress > div > div > div {
        background-color: var(--rose) !important;
    }

    hr {
        border-color: var(--border) !important;
    }

    .footer {
        border-top: 1px solid var(--border);
        color: var(--muted) !important;
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        margin-top: 50px;
        padding: 20px;
        text-align: center;
        text-transform: uppercase;
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Not Started',
            due_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            target_date TEXT,
            progress INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT,
            category TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            body TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute("PRAGMA table_info(tasks)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "status" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'Not Started'"
        )

    if "priority" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'"
        )

    if "description" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN description TEXT"
        )

    if "due_date" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN due_date TEXT"
        )

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
# PASSWORD PROTECTION
# =========================================================

def get_app_password():
    try:
        secret = st.secrets.get("APP_PASSWORD", "")
    except Exception:
        secret = ""

    return secret or os.environ.get("APP_PASSWORD", "")


def check_password():
    if st.session_state.get("authenticated", False):
        return True

    st.markdown(
        """
        <div style="max-width:520px; margin:90px auto 20px auto; text-align:center;">
            <div class="eyebrow">Private workspace</div>
            <div class="hero-title">Studio Sanctuary</div>
            <p class="hero-copy" style="margin:0 auto;">
                Enter your password to access your personal executive assistant.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    configured_password = get_app_password()

    if not configured_password:
        st.warning(
            "APP_PASSWORD is not configured. Add it in Streamlit Cloud under "
            "Settings → Secrets."
        )
        return False

    with st.form("login_form"):
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your private password",
        )
        submitted = st.form_submit_button("Enter workspace")

        if submitted:
            entered_hash = hashlib.sha256(
                password.encode("utf-8")
            ).hexdigest()

            correct_hash = hashlib.sha256(
                configured_password.encode("utf-8")
            ).hexdigest()

            if entered_hash == correct_hash:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("That password is not correct.")

    return False


if not check_password():
    st.stop()


# =========================================================
# HELPERS
# =========================================================

def format_date(value):
    if not value:
        return "No date"

    try:
        return datetime.strptime(
            str(value), "%Y-%m-%d"
        ).strftime("%B %d, %Y")
    except ValueError:
        return str(value)


def status_class(value):
    return str(value).lower().replace(" ", "-")


def count_records(table):
    allowed = {"tasks", "clients", "goals", "events", "templates"}

    if table not in allowed:
        return 0

    result = query_database(
        f"SELECT COUNT(*) AS count FROM {table}",
        fetch=True,
    )

    return result[0]["count"]


def delete_record(table, record_id):
    allowed = {"tasks", "clients", "goals", "events", "templates"}

    if table in allowed:
        query_database(
            f"DELETE FROM {table} WHERE id = ?",
            (record_id,),
        )


def task_card(task):
    current_status = task["status"] or "Not Started"

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{task["title"]}</div>
            <div class="card-meta">
                {task["description"] or "No description provided"}<br>
                Priority: {task["priority"] or "Medium"}<br>
                Due: {format_date(task["due_date"])}<br><br>
                <span class="status-pill status-{status_class(current_status)}">
                    {current_status}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown('<div class="brand">Sanctuary</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eyebrow">Personal executive assistant</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Tasks",
            "Calendar",
            "Clients",
            "Goals",
            "Message Templates",
        ],
    )

    st.markdown("---")

    if st.button("Lock workspace", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.caption("Private workspace")


# =========================================================
# OVERVIEW
# =========================================================

def show_overview():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Good to see you</div>
            <div class="hero-title">Your space for focused progress.</div>
            <div class="hero-copy">
                Organize your responsibilities, relationships, goals, and
                upcoming commitments in one calm, centralized workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(5)

    metrics = [
        ("Open tasks", count_records("tasks")),
        ("Clients", count_records("clients")),
        ("Goals", count_records("goals")),
        ("Events", count_records("events")),
        ("Templates", count_records("templates")),
    ]

    for column, (label, value) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Recent tasks")

    tasks = query_database(
        """
        SELECT * FROM tasks
        ORDER BY
            CASE WHEN status = 'Done' THEN 1 ELSE 0 END,
            due_date ASC,
            id DESC
        LIMIT 5
        """,
        fetch=True,
    )

    if not tasks:
        st.info("No tasks have been added yet.")
    else:
        for task in tasks:
            task_card(task)

    st.markdown(
        '<div class="footer">Studio Sanctuary · Personal executive workspace</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# TASKS
# =========================================================

def show_tasks():
    st.markdown('<div class="eyebrow">Work management</div>', unsafe_allow_html=True)
    st.title("Tasks")
    st.markdown(
        '<div class="subtitle">Keep your commitments visible and actionable.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("＋ Add a new task"):
        with st.form("task_form"):
            title = st.text_input("Task title")
            description = st.text_area("Description")
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High", "Urgent"],
            )
            status = st.selectbox(
                "Status",
                ["Not Started", "In Progress", "Done"],
            )
            due_date = st.date_input("Due date", value=None)
            submitted = st.form_submit_button("Save task")

            if submitted:
                if not title.strip():
                    st.error("Please enter a task title.")
                else:
                    query_database(
                        """
                        INSERT INTO tasks
                        (title, description, priority, status, due_date)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            title.strip(),
                            description.strip(),
                            priority,
                            status,
                            due_date.isoformat() if due_date else None,
                        ),
                    )
                    st.success("Task saved.")
                    st.rerun()

    filters = st.columns(3)

    with filters[0]:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "Not Started", "In Progress", "Done"],
        )

    with filters[1]:
        priority_filter = st.selectbox(
            "Filter by priority",
            ["All", "Low", "Medium", "High", "Urgent"],
        )

    with filters[2]:
        search = st.text_input("Search tasks")

    query = "SELECT * FROM tasks WHERE 1 = 1"
    parameters = []

    if status_filter != "All":
        query += " AND status = ?"
        parameters.append(status_filter)

    if priority_filter != "All":
        query += " AND priority = ?"
        parameters.append(priority_filter)

    if search.strip():
        query += " AND (title LIKE ? OR description LIKE ?)"
        value = f"%{search.strip()}%"
        parameters.extend([value, value])

    query += """
        ORDER BY
            CASE WHEN status = 'Done' THEN 1 ELSE 0 END,
            due_date ASC,
            id DESC
    """

    tasks = query_database(query, parameters, fetch=True)

    if not tasks:
        st.info("No tasks match your filters.")
    else:
        for task in tasks:
            left, right = st.columns([5, 1])

            with left:
                task_card(task)

            with right:
                st.write("")
                st.write("")
                if st.button("Delete", key=f"delete_task_{task['id']}"):
                    delete_record("tasks", task["id"])
                    st.rerun()


# =========================================================
# CALENDAR
# =========================================================

def show_calendar():
    st.markdown('<div class="eyebrow">Schedule</div>', unsafe_allow_html=True)
    st.title("Calendar")
    st.markdown(
        '<div class="subtitle">Keep important moments in view.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("＋ Add calendar event"):
        with st.form("event_form"):
            title = st.text_input("Event title")
            event_date = st.date_input("Date", value=date.today())
            event_time = st.text_input("Time")
            category = st.selectbox(
                "Category",
                ["Work", "Personal", "Client", "Health", "Other"],
            )
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save event")

            if submitted:
                if not title.strip():
                    st.error("Please enter an event title.")
                else:
                    query_database(
                        """
                        INSERT INTO events
                        (title, event_date, event_time, category, notes)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            title.strip(),
                            event_date.isoformat(),
                            event_time.strip(),
                            category,
                            notes.strip(),
                        ),
                    )
                    st.success("Event saved.")
                    st.rerun()

    events = query_database(
        """
        SELECT * FROM events
        ORDER BY event_date ASC, event_time ASC, id DESC
        """,
        fetch=True,
    )

    if not events:
        st.info("No calendar events have been added yet.")
    else:
        for event in events:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{event["title"]}</div>
                        <div class="card-meta">
                            {format_date(event["event_date"])} ·
                            {event["event_time"] or "Time not specified"}<br>
                            Category: {event["category"] or "Other"}<br>
                            {event["notes"] or ""}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                if st.button("Delete", key=f"delete_event_{event['id']}"):
                    delete_record("events", event["id"])
                    st.rerun()


# =========================================================
# CLIENTS
# =========================================================

def show_clients():
    st.markdown('<div class="eyebrow">Relationships</div>', unsafe_allow_html=True)
    st.title("Clients")
    st.markdown(
        '<div class="subtitle">Keep essential client details accessible.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("＋ Add client"):
        with st.form("client_form"):
            name = st.text_input("Client name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save client")

            if submitted:
                if not name.strip():
                    st.error("Please enter a client name.")
                else:
                    query_database(
                        """
                        INSERT INTO clients
                        (name, email, phone, notes)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            name.strip(),
                            email.strip(),
                            phone.strip(),
                            notes.strip(),
                        ),
                    )
                    st.success("Client saved.")
                    st.rerun()

    clients = query_database(
        "SELECT * FROM clients ORDER BY name ASC",
        fetch=True,
    )

    if not clients:
        st.info("No clients have been added yet.")
    else:
        for client in clients:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{client["name"]}</div>
                        <div class="card-meta">
                            Email: {client["email"] or "Not provided"}<br>
                            Phone: {client["phone"] or "Not provided"}<br>
                            {client["notes"] or ""}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                if st.button("Delete", key=f"delete_client_{client['id']}"):
                    delete_record("clients", client["id"])
                    st.rerun()


# =========================================================
# GOALS
# =========================================================

def show_goals():
    st.markdown('<div class="eyebrow">Direction</div>', unsafe_allow_html=True)
    st.title("Goals")
    st.markdown(
        '<div class="subtitle">Turn your larger vision into visible progress.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("＋ Add goal"):
        with st.form("goal_form"):
            title = st.text_input("Goal title")
            description = st.text_area("Description")
            target_date = st.date_input("Target date", value=None)
            progress = st.slider("Progress", 0, 100, 0)
            submitted = st.form_submit_button("Save goal")

            if submitted:
                if not title.strip():
                    st.error("Please enter a goal title.")
                else:
                    query_database(
                        """
                        INSERT INTO goals
                        (title, description, target_date, progress)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            title.strip(),
                            description.strip(),
                            target_date.isoformat()
                            if target_date else None,
                            progress,
                        ),
                    )
                    st.success("Goal saved.")
                    st.rerun()

    goals = query_database(
        "SELECT * FROM goals ORDER BY target_date ASC, id DESC",
        fetch=True,
    )

    if not goals:
        st.info("No goals have been added yet.")
    else:
        for goal in goals:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{goal["title"]}</div>
                        <div class="card-meta">
                            {goal["description"] or "No description provided"}<br>
                            Target date: {format_date(goal["target_date"])}<br>
                            Progress: {goal["progress"]}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(int(goal["progress"]) / 100)

            with right:
                st.write("")
                st.write("")
                if st.button("Delete", key=f"delete_goal_{goal['id']}"):
                    delete_record("goals", goal["id"])
                    st.rerun()


# =========================================================
# MESSAGE TEMPLATES
# =========================================================

def show_templates():
    st.markdown('<div class="eyebrow">Communication</div>', unsafe_allow_html=True)
    st.title("Message Templates")
    st.markdown(
        '<div class="subtitle">Save messages you use often.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("＋ Add message template"):
        with st.form("template_form"):
            title = st.text_input("Template title")
            category = st.selectbox(
                "Category",
                ["Follow-up", "Introduction", "Reminder", "Thank you", "Other"],
            )
            body = st.text_area("Message", height=180)
            submitted = st.form_submit_button("Save template")

            if submitted:
                if not title.strip() or not body.strip():
                    st.error("Please enter both a title and a message.")
                else:
                    query_database(
                        """
                        INSERT INTO templates
                        (title, category, body)
                        VALUES (?, ?, ?)
                        """,
                        (
                            title.strip(),
                            category,
                            body.strip(),
                        ),
                    )
                    st.success("Template saved.")
                    st.rerun()

    templates = query_database(
        "SELECT * FROM templates ORDER BY title ASC",
        fetch=True,
    )

    if not templates:
        st.info("No message templates have been added yet.")
    else:
        for template in templates:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{template["title"]}</div>
                        <div class="card-meta">
                            Category: {template["category"] or "Other"}
                        </div>
                        <br>
                        <div style="color:#f4e4d3;">
                            {template["body"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                if st.button(
                    "Delete",
                    key=f"delete_template_{template['id']}",
                ):
                    delete_record("templates", template["id"])
                    st.rerun()


# =========================================================
# PAGE ROUTING
# =========================================================

if page == "Overview":
    show_overview()
elif page == "Tasks":
    show_tasks()
elif page == "Calendar":
    show_calendar()
elif page == "Clients":
    show_clients()
elif page == "Goals":
    show_goals()
elif page == "Message Templates":
    show_templates()
