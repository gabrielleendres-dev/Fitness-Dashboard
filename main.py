import os
import sqlite3
import hashlib
import html
from datetime import date, datetime, timedelta

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

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--background) !important;
        color: var(--espresso) !important;
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

    h1 { font-size: 3.2rem !important; }
    h2 { font-size: 2.4rem !important; }
    h3 { font-size: 1.8rem !important; }

    p, label, span {
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
        box-shadow: 0 14px 35px rgba(0,0,0,.18);
    }

    .hero-title {
        color: var(--cream);
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.5rem;
        line-height: 1;
        margin: 10px 0 14px;
    }

    .hero-copy {
        color: var(--muted) !important;
        font-size: .92rem;
        line-height: 1.8;
        max-width: 720px;
    }

    .metric-card,
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 22px;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,.12);
    }

    .metric-card {
        min-height: 125px;
    }

    .metric-label {
        color: var(--pink) !important;
        font-size: .68rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
    }

    .metric-value {
        color: var(--cream) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.9rem;
        line-height: 1;
        margin-top: 14px;
    }

    .card-title {
        color: var(--cream) !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.65rem;
        font-weight: 600;
    }

    .card-meta {
        color: var(--muted) !important;
        font-size: .78rem;
        line-height: 1.8;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 10px;
        font-size: .62rem;
        font-weight: 700;
        letter-spacing: .08em;
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
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .1em;
        min-height: 42px;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background: var(--cream) !important;
        border-color: var(--cream) !important;
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

    input, textarea,
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
        font-size: .68rem;
        letter-spacing: .12em;
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS automation_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            trigger_type TEXT NOT NULL,
            action_type TEXT NOT NULL,
            description TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Migrate older task databases without deleting existing records.
    cursor.execute("PRAGMA table_info(tasks)")
    task_columns = [row["name"] for row in cursor.fetchall()]

    migrations = {
        "status": "ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'Not Started'",
        "priority": "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'",
        "description": "ALTER TABLE tasks ADD COLUMN description TEXT",
        "due_date": "ALTER TABLE tasks ADD COLUMN due_date TEXT",
    }

    for column, statement in migrations.items():
        if column not in task_columns:
            cursor.execute(statement)

    connection.commit()
    connection.close()


def query_database(query, parameters=(), fetch=False):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, parameters)

    if fetch:
        results = cursor.fetchall()
        connection.close()
        return results

    connection.commit()
    connection.close()
    return True


initialize_database()


# =========================================================
# AUTHENTICATION
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
        <div style="max-width:520px;margin:90px auto 20px;text-align:center;">
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
        password = st.text_input("Password", type="password")
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

def safe(value):
    if value is None:
        return ""
    return html.escape(str(value)).replace("\n", "<br>")


def format_date(value):
    if not value:
        return "No date"

    try:
        return datetime.strptime(
            str(value), "%Y-%m-%d"
        ).strftime("%B %d, %Y")
    except ValueError:
        return safe(value)


def status_class(value):
    return str(value or "Not Started").lower().replace(" ", "-")


def count_records(table):
    allowed = {
        "tasks",
        "clients",
        "goals",
        "events",
        "templates",
        "automation_rules",
    }

    if table not in allowed:
        return 0

    result = query_database(
        f"SELECT COUNT(*) AS count FROM {table}",
        fetch=True,
    )

    return result[0]["count"]


def delete_record(table, record_id):
    allowed = {
        "tasks",
        "clients",
        "goals",
        "events",
        "templates",
        "automation_rules",
    }

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
            <div class="card-title">{safe(task["title"])}</div>
            <div class="card-meta">
                {safe(task["description"]) or "No description provided"}<br>
                Priority: {safe(task["priority"]) or "Medium"}<br>
                Due: {format_date(task["due_date"])}<br><br>
                <span class="status-pill status-{status_class(current_status)}">
                    {safe(current_status)}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def delete_buttons(table, record_id, key_prefix):
    if st.button("Delete", key=f"{key_prefix}_{record_id}"):
        delete_record(table, record_id)
        st.rerun()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">Sanctuary</div>',
        unsafe_allow_html=True,
    )

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
            "Automation Center",
            "Toolbox",
        ],
    )

    st.markdown("---")

    if st.button("Lock workspace", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.caption("Private workspace")


# =========================================================
# OVERVIEW / TODAY
# =========================================================

def show_overview():
    today = date.today().isoformat()

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Today</div>
            <div class="hero-title">Your space for focused progress.</div>
            <div class="hero-copy">
                Organize your responsibilities, relationships, goals, and
                upcoming commitments in one calm, centralized workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(6)

    metrics = [
        ("Tasks", count_records("tasks")),
        ("Clients", count_records("clients")),
        ("Goals", count_records("goals")),
        ("Events", count_records("events")),
        ("Templates", count_records("templates")),
        ("Automations", count_records("automation_rules")),
    ]

    for column, (label, value) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{safe(label)}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Today’s agenda")

    today_tasks = query_database(
        """
        SELECT * FROM tasks
        WHERE status != 'Done'
        AND due_date <= ?
        ORDER BY due_date ASC, id DESC
        """,
        (today,),
        fetch=True,
    )

    today_events = query_database(
        """
        SELECT * FROM events
        WHERE event_date = ?
        ORDER BY event_time ASC, id DESC
        """,
        (today,),
        fetch=True,
    )

    if not today_tasks and not today_events:
        st.info("Your agenda is clear for today.")

    for task in today_tasks:
        task_card(task)

    for event in today_events:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{safe(event["title"])}</div>
                <div class="card-meta">
                    {safe(event["event_time"]) or "Time not specified"} ·
                    {safe(event["category"]) or "Other"}<br>
                    {safe(event["notes"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Recent tasks")

    recent_tasks = query_database(
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

    if not recent_tasks:
        st.info("No tasks have been added yet.")
    else:
        for task in recent_tasks:
            task_card(task)

    st.markdown(
        '<div class="footer">Studio Sanctuary · Personal executive workspace</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# TASKS
# =========================================================

def show_tasks():
    st.markdown(
        '<div class="eyebrow">Work management</div>',
        unsafe_allow_html=True,
    )
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
            due_date = st.date_input(
                "Due date",
                value=None,
            )

            if st.form_submit_button("Save task"):
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

    filters = st.columns(4)

    with filters[0]:
        status_filter = st.selectbox(
            "Status",
            ["All", "Not Started", "In Progress", "Done"],
        )

    with filters[1]:
        priority_filter = st.selectbox(
            "Priority",
            ["All", "Low", "Medium", "High", "Urgent"],
        )

    with filters[2]:
        date_filter = st.selectbox(
            "Due date",
            ["All", "Today", "This Week", "Overdue", "No Date"],
        )

    with filters[3]:
        search = st.text_input("Search")

    query = "SELECT * FROM tasks WHERE 1=1"
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

    today = date.today()
    week_end = today + timedelta(days=7)

    if date_filter == "Today":
        query += " AND due_date = ?"
        parameters.append(today.isoformat())
    elif date_filter == "This Week":
        query += " AND due_date BETWEEN ? AND ?"
        parameters.extend([today.isoformat(), week_end.isoformat()])
    elif date_filter == "Overdue":
        query += " AND due_date < ? AND status != 'Done'"
        parameters.append(today.isoformat())
    elif date_filter == "No Date":
        query += " AND (due_date IS NULL OR due_date = '')"

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
                delete_buttons("tasks", task["id"], "delete_task")


# =========================================================
# CALENDAR
# =========================================================

def show_calendar():
    st.markdown(
        '<div class="eyebrow">Schedule</div>',
        unsafe_allow_html=True,
    )
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

            if st.form_submit_button("Save event"):
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

    filters = st.columns(2)

    with filters[0]:
        category_filter = st.selectbox(
            "Category filter",
            ["All", "Work", "Personal", "Client", "Health", "Other"],
        )

    with filters[1]:
        calendar_filter = st.selectbox(
            "Date filter",
            ["All", "Today", "Upcoming", "Past"],
        )

    query = "SELECT * FROM events WHERE 1=1"
    parameters = []

    if category_filter != "All":
        query += " AND category = ?"
        parameters.append(category_filter)

    if calendar_filter == "Today":
        query += " AND event_date = ?"
        parameters.append(date.today().isoformat())
    elif calendar_filter == "Upcoming":
        query += " AND event_date >= ?"
        parameters.append(date.today().isoformat())
    elif calendar_filter == "Past":
        query += " AND event_date < ?"
        parameters.append(date.today().isoformat())

    query += " ORDER BY event_date ASC, event_time ASC, id DESC"

    events = query_database(query, parameters, fetch=True)

    if not events:
        st.info("No calendar events match your filters.")
    else:
        for event in events:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{safe(event["title"])}</div>
                        <div class="card-meta">
                            {format_date(event["event_date"])} ·
                            {safe(event["event_time"]) or "Time not specified"}<br>
                            Category: {safe(event["category"]) or "Other"}<br>
                            {safe(event["notes"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                delete_buttons("events", event["id"], "delete_event")


# =========================================================
# CLIENTS
# =========================================================

def show_clients():
    st.markdown(
        '<div class="eyebrow">Relationships</div>',
        unsafe_allow_html=True,
    )
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

            if st.form_submit_button("Save client"):
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

    sort_by = st.selectbox(
        "Sort clients",
        ["Name A–Z", "Newest", "Oldest"],
    )

    order = "name ASC"
    if sort_by == "Newest":
        order = "id DESC"
    elif sort_by == "Oldest":
        order = "id ASC"

    clients = query_database(
        f"SELECT * FROM clients ORDER BY {order}",
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
                        <div class="card-title">{safe(client["name"])}</div>
                        <div class="card-meta">
                            Email: {safe(client["email"]) or "Not provided"}<br>
                            Phone: {safe(client["phone"]) or "Not provided"}<br>
                            {safe(client["notes"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                delete_buttons("clients", client["id"], "delete_client")


# =========================================================
# GOALS
# =========================================================

def show_goals():
    st.markdown(
        '<div class="eyebrow">Direction</div>',
        unsafe_allow_html=True,
    )
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

            if st.form_submit_button("Save goal"):
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

    goal_filter = st.selectbox(
        "Progress filter",
        [
            "All",
            "Not Started",
            "In Progress",
            "Nearly Complete",
            "Complete",
        ],
    )

    goals = query_database(
        "SELECT * FROM goals ORDER BY target_date ASC, id DESC",
        fetch=True,
    )

    filtered_goals = []

    for goal in goals:
        progress = int(goal["progress"] or 0)

        if goal_filter == "Not Started" and progress != 0:
            continue
        if goal_filter == "In Progress" and not 0 < progress < 75:
            continue
        if goal_filter == "Nearly Complete" and not 75 <= progress < 100:
            continue
        if goal_filter == "Complete" and progress != 100:
            continue

        filtered_goals.append(goal)

    if not filtered_goals:
        st.info("No goals match your filter.")
    else:
        for goal in filtered_goals:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{safe(goal["title"])}</div>
                        <div class="card-meta">
                            {safe(goal["description"]) or "No description provided"}<br>
                            Target date: {format_date(goal["target_date"])}<br>
                            Progress: {goal["progress"]}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(int(goal["progress"] or 0) / 100)

            with right:
                st.write("")
                st.write("")
                delete_buttons("goals", goal["id"], "delete_goal")


# =========================================================
# MESSAGE TEMPLATES
# =========================================================

def show_templates():
    st.markdown(
        '<div class="eyebrow">Communication</div>',
        unsafe_allow_html=True,
    )
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
                [
                    "Follow-up",
                    "Introduction",
                    "Reminder",
                    "Thank you",
                    "Other",
                ],
            )
            body = st.text_area("Message", height=180)

            if st.form_submit_button("Save template"):
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

    category_filter = st.selectbox(
        "Category filter",
        [
            "All",
            "Follow-up",
            "Introduction",
            "Reminder",
            "Thank you",
            "Other",
        ],
    )

    if category_filter == "All":
        templates = query_database(
            "SELECT * FROM templates ORDER BY title ASC",
            fetch=True,
        )
    else:
        templates = query_database(
            """
            SELECT * FROM templates
            WHERE category = ?
            ORDER BY title ASC
            """,
            (category_filter,),
            fetch=True,
        )

    if not templates:
        st.info("No message templates match your filter.")
    else:
        for template in templates:
            left, right = st.columns([5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{safe(template["title"])}</div>
                        <div class="card-meta">
                            Category: {safe(template["category"]) or "Other"}
                        </div>
                        <br>
                        <div style="color:#f4e4d3; white-space:pre-wrap;">
                            {safe(template["body"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                delete_buttons(
                    "templates",
                    template["id"],
                    "delete_template",
                )


# =========================================================
# AUTOMATION CENTER
# =========================================================

def show_automation():
    st.markdown(
        '<div class="eyebrow">Workflows</div>',
        unsafe_allow_html=True,
    )
    st.title("Automation Center")
    st.markdown(
        '<div class="subtitle">Create simple rules for recurring actions.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("＋ Add automation rule"):
        with st.form("automation_form"):
            name = st.text_input("Rule name")

            trigger_type = st.selectbox(
                "When this happens",
                [
                    "Task becomes overdue",
                    "Task is marked Done",
                    "Calendar event is approaching",
                    "Goal reaches 100%",
                    "New client is added",
                ],
            )

            action_type = st.selectbox(
                "Then do this",
                [
                    "Create a follow-up task",
                    "Create a calendar reminder",
                    "Display a dashboard alert",
                    "Mark a related task",
                    "No action yet",
                ],
            )

            description = st.text_area("Notes about this automation")
            active = st.checkbox("Active", value=True)

            if st.form_submit_button("Save automation"):
                if not name.strip():
                    st.error("Please enter a rule name.")
                else:
                    query_database(
                        """
                        INSERT INTO automation_rules
                        (name, trigger_type, action_type, description, active)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            name.strip(),
                            trigger_type,
                            action_type,
                            description.strip(),
                            1 if active else 0,
                        ),
                    )
                    st.success("Automation saved.")
                    st.rerun()

    active_filter = st.selectbox(
        "Show rules",
        ["All", "Active", "Inactive"],
    )

    query = "SELECT * FROM automation_rules"
    parameters = []

    if active_filter == "Active":
        query += " WHERE active = 1"
    elif active_filter == "Inactive":
        query += " WHERE active = 0"

    query += " ORDER BY id DESC"

    rules = query_database(query, parameters, fetch=True)

    if not rules:
        st.info("No automation rules have been added yet.")
    else:
        for rule in rules:
            left, right = st.columns([5, 1])

            with left:
                state = "Active" if rule["active"] else "Inactive"

                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{safe(rule["name"])}</div>
                        <div class="card-meta">
                            Status: {state}<br>
                            Trigger: {safe(rule["trigger_type"])}<br>
                            Action: {safe(rule["action_type"])}<br>
                            {safe(rule["description"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:
                st.write("")
                st.write("")
                delete_buttons(
                    "automation_rules",
                    rule["id"],
                    "delete_automation",
                )


# =========================================================
# TOOLBOX
# =========================================================

def show_toolbox():
    st.markdown(
        '<div class="eyebrow">Workspace utilities</div>',
        unsafe_allow_html=True,
    )
    st.title("Toolbox")
    st.markdown(
        '<div class="subtitle">Quick tools for organizing your work.</div>',
        unsafe_allow_html=True,
    )

    tool = st.selectbox(
        "Choose a tool",
        [
            "Quick Note",
            "Date Calculator",
            "Task Planning Prompt",
            "Workspace Summary",
        ],
    )

    if tool == "Quick Note":
        st.subheader("Quick Note")
        st.text_area(
            "Write a note",
            height=220,
            placeholder="Capture an idea, reminder, or thought...",
        )
        st.caption(
            "Quick notes are not saved to the database yet. Use Tasks or "
            "Message Templates for permanent records."
        )

    elif tool == "Date Calculator":
        st.subheader("Date Calculator")

        start_date = st.date_input(
            "Start date",
            value=date.today(),
        )

        number_of_days = st.number_input(
            "Number of days",
            min_value=0,
            max_value=3650,
            value=7,
            step=1,
        )

        calculated_date = start_date + timedelta(days=int(number_of_days))

        st.success(
            f"{int(number_of_days)} days after "
            f"{start_date.strftime('%B %d, %Y')} is "
            f"{calculated_date.strftime('%B %d, %Y')}."
        )

    elif tool == "Task Planning Prompt":
        st.subheader("Task Planning Prompt")

        project = st.text_input(
            "What are you trying to accomplish?"
        )

        if st.button("Generate planning checklist"):
            if not project.strip():
                st.warning("Enter a project or outcome first.")
            else:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">
                            Planning checklist for {safe(project)}
                        </div>
                        <div class="card-meta">
                            1. Define the desired outcome.<br>
                            2. List the major steps.<br>
                            3. Identify the first actionable task.<br>
                            4. Assign due dates.<br>
                            5. Review dependencies and priorities.<br>
                            6. Schedule a follow-up review.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    elif tool == "Workspace Summary":
        st.subheader("Workspace Summary")

        summary = [
            ("Tasks", count_records("tasks")),
            ("Calendar events", count_records("events")),
            ("Clients", count_records("clients")),
            ("Goals", count_records("goals")),
            ("Message templates", count_records("templates")),
            ("Automation rules", count_records("automation_rules")),
        ]

        for label, value in summary:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-meta">
                        {safe(label)}
                        <strong style="float:right;color:#f4e4d3;">
                            {value}
                        </strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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
elif page == "Automation Center":
    show_automation()
elif page == "Toolbox":
    show_toolbox()
