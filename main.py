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
    --ivory: #F7F3ED;
    --paper: #FFFDF9;
    --espresso: #332A27;
    --mocha: #65524A;
    --mushroom: #A99A90;
    --sage: #AAB7A5;
    --dusty-rose: #CFA9A5;
    --terracotta: #B97863;
    --blush: #EAD8D2;
    --sand: #D8C9BA;
    --line: #E3D9CF;
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
    st.caption(
        f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
    )

    tasks = read_table("tasks")
    clients = read_table("clients")
    goals = read_table("goals")
    events = read_table("events")

    open_tasks = 0 if tasks.empty else len(
        tasks[tasks["completed"] == 0]
    )

    active_clients = 0 if clients.empty else len(
        clients[clients["status"] == "Active"]
    )

    upcoming_events = 0 if events.empty else len(events)

    average_goal_progress = 0
    if not goals.empty:
        average_goal_progress = round(goals["progress"].mean())

    column1, column2, column3, column4 = st.columns(4)

    column1.metric("Open Tasks", open_tasks)
    column2.metric("Active Clients", active_clients)
    column3.metric("Upcoming Events", upcoming_events)
    column4.metric(
        "Goal Progress",
        f"{average_goal_progress}%",
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Open Tasks")

        if tasks.empty or open_tasks == 0:
            st.info("You have no open tasks.")
        else:
            open_task_list = tasks[tasks["completed"] == 0]

            st.dataframe(
                open_task_list[
                    [
                        "id",
                        "title",
                        "category",
                        "due_date",
                        "priority",
                        "status",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

    with right:
        st.subheader("Current Goals")

        if goals.empty:
            st.info("No goals added yet.")
        else:
            for _, goal in goals.iterrows():
                st.write(
                    f"**{goal['title']}** — "
                    f"{goal['progress']}%"
                )
                st.progress(int(goal["progress"]) / 100)


# =========================================================
# TASKS
# =========================================================

elif page == "Tasks":
    st.title("Tasks")

    with st.expander("➕ Add a task", expanded=True):
        with st.form("add_task_form"):
            title = st.text_input("Task name")

            category = st.selectbox(
                "Category",
                [
                    "Business",
                    "Teaching",
                    "Personal",
                    "Health",
                    "Admin",
                ],
            )

            due_date = st.date_input(
                "Due date",
                value=date.today(),
            )

            priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
            )

            status = st.selectbox(
                "Status",
                ["Not Started", "In Progress", "Done"],
            )

            submitted = st.form_submit_button("Add Task")

            if submitted:
                if title.strip():
                    add_task(
                        title.strip(),
                        category,
                        due_date,
                        priority,
                        status,
                    )
                    st.success("Task added.")
                    st.rerun()
                else:
                    st.warning("Please enter a task name.")

    tasks = read_table("tasks")

    if tasks.empty:
        st.info("No tasks have been added yet.")
    else:
        st.subheader("Your Tasks")

        filter_column1, filter_column2 = st.columns(2)

        with filter_column1:
            status_filter = st.selectbox(
                "Filter by status",
                [
                    "All",
                    "Not Started",
                    "In Progress",
                    "Done",
                ],
            )

        with filter_column2:
            priority_filter = st.selectbox(
                "Filter by priority",
                ["All", "High", "Medium", "Low"],
            )

        filtered_tasks = tasks.copy()

        if status_filter != "All":
            filtered_tasks = filtered_tasks[
                filtered_tasks["status"] == status_filter
            ]

        if priority_filter != "All":
            filtered_tasks = filtered_tasks[
                filtered_tasks["priority"] == priority_filter
            ]

        if filtered_tasks.empty:
            st.info("No tasks match those filters.")
        else:
            for _, task in filtered_tasks.iterrows():
                if task["completed"] == 0:
                    column1, column2 = st.columns([5, 1])

                    with column1:
                        st.write(
                            f"**{task['title']}**  \n"
                            f"{task['category']} · "
                            f"Due {task['due_date']} · "
                            f"{task['priority']} priority · "
                            f"{task['status']}"
                        )

                    with column2:
                        if st.button(
                            "Complete",
                            key=f"complete_{task['id']}",
                        ):
                            complete_task(int(task["id"]))
                            st.rerun()

            completed_tasks = filtered_tasks[
                filtered_tasks["completed"] == 1
            ]

            if not completed_tasks.empty:
                with st.expander("Completed tasks"):
                    st.dataframe(
                        completed_tasks,
                        use_container_width=True,
                        hide_index=True,
                    )


# =========================================================
# CALENDAR
# =========================================================

elif page == "Calendar":
    st.title("Calendar")

    with st.expander("➕ Add an event", expanded=True):
        with st.form("add_event_form"):
            title = st.text_input("Event title")

            event_date = st.date_input(
                "Event date",
                value=date.today(),
            )

            event_time = st.text_input(
                "Time",
                placeholder="Example: 9:00 AM",
            )

            category = st.selectbox(
                "Category",
                [
                    "Client",
                    "Class",
                    "Business",
                    "Personal",
                ],
            )

            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Add Event")

            if submitted:
                if title.strip():
                    add_event(
                        title.strip(),
                        event_date,
                        event_time,
                        category,
                        notes,
                    )
                    st.success("Event added.")
                    st.rerun()
                else:
                    st.warning("Please enter an event title.")

    events = read_table("events")

    if events.empty:
        st.info("No events added yet.")
    else:
        st.dataframe(
            events[
                [
                    "title",
                    "event_date",
                    "event_time",
                    "category",
                    "notes",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# CLIENTS
# =========================================================

elif page == "Clients":
    st.title("Clients")

    with st.expander("➕ Add a client", expanded=True):
        with st.form("add_client_form"):
            name = st.text_input("Client name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

            status = st.selectbox(
                "Status",
                ["Active", "Lead", "Inactive"],
            )

            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Add Client")

            if submitted:
                if name.strip():
                    add_client(
                        name.strip(),
                        email.strip(),
                        phone.strip(),
                        status,
                        notes.strip(),
                    )
                    st.success("Client added.")
                    st.rerun()
                else:
                    st.warning("Please enter the client's name.")

    clients = read_table("clients")

    if clients.empty:
        st.info("No clients added yet.")
    else:
        st.dataframe(
            clients[
                [
                    "name",
                    "email",
                    "phone",
                    "status",
                    "notes",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# GOALS
# =========================================================

elif page == "Goals":
    st.title("Goals")

    with st.expander("➕ Add a goal", expanded=True):
        with st.form("add_goal_form"):
            title = st.text_input("Goal")

            category = st.selectbox(
                "Category",
                [
                    "Business",
                    "Fitness",
                    "Financial",
                    "Personal",
                ],
            )

            target_date = st.date_input(
                "Target date",
                value=date.today(),
            )

            progress = st.slider(
                "Current progress",
                0,
                100,
                0,
            )

            submitted = st.form_submit_button("Add Goal")

            if submitted:
                if title.strip():
                    add_goal(
                        title.strip(),
                        category,
                        target_date,
                        progress,
                    )
                    st.success("Goal added.")
                    st.rerun()
                else:
                    st.warning("Please enter a goal.")

    goals = read_table("goals")

    if goals.empty:
        st.info("No goals added yet.")
    else:
        for _, goal in goals.iterrows():
            st.write(
                f"**{goal['title']}** · "
                f"{goal['category']} · "
                f"Target: {goal['target_date']}"
            )

            st.progress(int(goal["progress"]) / 100)
            st.caption(f"{goal['progress']}% complete")


# =========================================================
# MESSAGE TEMPLATES
# =========================================================

elif page == "Message Templates":
    st.title("Message Templates")

    template_type = st.selectbox(
        "Choose a template",
        [
            "New client welcome",
            "Follow-up after consultation",
            "Class reminder",
            "Payment reminder",
        ],
    )

    templates = {
        "New client welcome": (
            "Hi [Client Name], welcome! "
            "I’m excited to work with you. "
            "I’ll send over the next steps shortly."
        ),
        "Follow-up after consultation": (
            "Hi [Client Name], it was great speaking with you today. "
            "I wanted to follow up and see if you had any questions."
        ),
        "Class reminder": (
            "Hi [Client Name], this is a reminder about your upcoming "
            "class on [Date] at [Time]. See you soon!"
        ),
        "Payment reminder": (
            "Hi [Client Name], this is a friendly reminder that your "
            "payment is due. Please let me know if you have any questions."
        ),
    }

    st.text_area(
        "Template text",
        value=templates[template_type],
        height=180,
    )

    st.caption(
        "Replace the bracketed words before sending."
    )
