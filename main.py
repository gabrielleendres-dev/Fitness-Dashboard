import sqlite3
from datetime import date, datetime

import pandas as pd
import streamlit as st


# -----------------------------
# App configuration
# -----------------------------
st.set_page_config(
    page_title="Personal Executive Assistant",
    page_icon="💪",
    layout="wide",
)


# -----------------------------
# Private passcode protection
# -----------------------------
def check_password():
    """Require the password before displaying the private dashboard."""

    if st.session_state.get("authenticated", False):
        return True

st.sidebar.title("💪 My Assistant")

if st.sidebar.button("Lock Dashboard"):
    st.session_state.authenticated = False
    st.rerun()


if st.sidebar.button("Lock Dashboard"):
    st.session_state.authenticated = False
    st.rerun()

    st.subheader("Private dashboard")

    password = st.text_input(
        "Enter your passcode",
        type="password",
    )

    if st.button("Unlock Dashboard", type="primary"):
        correct_password = st.secrets.get("APP_PASSWORD")

        if not correct_password:
            st.error(
                "The app password has not been configured yet. "
                "Add APP_PASSWORD in Streamlit Secrets."
            )
            return False

        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect passcode.")

    st.caption("This dashboard is private. Do not share your passcode.")
    return False


if not check_password():
    st.stop()



# -----------------------------
# Database setup
# -----------------------------
DB_NAME = "assistant_dashboard.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            due_date TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            status TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            target_date TEXT,
            progress INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT,
            event_time TEXT,
            category TEXT,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()


initialize_database()


# -----------------------------
# Database helper functions
# -----------------------------
def add_task(title, category, due_date, priority):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO tasks (title, category, due_date, priority)
        VALUES (?, ?, ?, ?)
        """,
        (title, category, str(due_date), priority),
    )
    connection.commit()
    connection.close()


def complete_task(task_id):
    connection = get_connection()
    connection.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
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
        INSERT INTO events (title, event_date, event_time, category, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, str(event_date), event_time, category, notes),
    )
    connection.commit()
    connection.close()


def read_table(table_name):
    connection = get_connection()
    data = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
    connection.close()
    return data


# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("💪 My Assistant")

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


# -----------------------------
# Dashboard
# -----------------------------
if page == "Dashboard":
    st.title("Personal + Executive Assistant")
    st.caption(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}")

    tasks = read_table("tasks")
    clients = read_table("clients")
    goals = read_table("goals")
    events = read_table("events")

    active_tasks = 0
    if not tasks.empty:
        active_tasks = len(tasks[tasks["completed"] == 0])

    active_clients = 0
    if not clients.empty:
        active_clients = len(clients[clients["status"] == "Active"])

    upcoming_events = 0
    if not events.empty:
        upcoming_events = len(events)

    average_goal_progress = 0
    if not goals.empty:
        average_goal_progress = round(goals["progress"].mean())

    column1, column2, column3, column4 = st.columns(4)

    column1.metric("Open Tasks", active_tasks)
    column2.metric("Active Clients", active_clients)
    column3.metric("Upcoming Events", upcoming_events)
    column4.metric("Goal Progress", f"{average_goal_progress}%")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Open Tasks")
        if tasks.empty or active_tasks == 0:
            st.info("You have no open tasks.")
        else:
            open_tasks = tasks[tasks["completed"] == 0]
            st.dataframe(
                open_tasks[
                    ["id", "title", "category", "due_date", "priority"]
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
                st.write(f"**{goal['title']}** — {goal['progress']}%")
                st.progress(int(goal["progress"]) / 100)


# -----------------------------
# Tasks
# -----------------------------
elif page == "Tasks":
    st.title("Tasks")

    with st.expander("➕ Add a task", expanded=True):
        with st.form("add_task_form"):
            title = st.text_input("Task name")
            category = st.selectbox(
                "Category",
                ["Business", "Teaching", "Personal", "Health", "Admin"],
            )
            due_date = st.date_input("Due date", value=date.today())
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if title.strip():
                    add_task(title.strip(), category, due_date, priority)
                    st.success("Task added.")
                    st.rerun()
                else:
                    st.warning("Please enter a task name.")

    tasks = read_table("tasks")

    if tasks.empty:
        st.info("No tasks have been added yet.")
    else:
        st.subheader("Your Tasks")

        for _, task in tasks.iterrows():
            if task["completed"] == 0:
                column1, column2 = st.columns([5, 1])

                with column1:
                    st.write(
                        f"**{task['title']}**  \n"
                        f"{task['category']} · Due {task['due_date']} · "
                        f"{task['priority']} priority"
                    )

                with column2:
                    if st.button("Complete", key=f"complete_{task['id']}"):
                        complete_task(int(task["id"]))
                        st.rerun()

        completed_tasks = tasks[tasks["completed"] == 1]
        if not completed_tasks.empty:
            with st.expander("Completed tasks"):
                st.dataframe(
                    completed_tasks,
                    use_container_width=True,
                    hide_index=True,
                )


# -----------------------------
# Calendar
# -----------------------------
elif page == "Calendar":
    st.title("Calendar")

    with st.expander("➕ Add an event", expanded=True):
        with st.form("add_event_form"):
            title = st.text_input("Event title")
            event_date = st.date_input("Event date", value=date.today())
            event_time = st.text_input("Time", placeholder="Example: 9:00 AM")
            category = st.selectbox(
                "Category",
                ["Client", "Class", "Business", "Personal"],
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
                ["title", "event_date", "event_time", "category", "notes"]
            ],
            use_container_width=True,
            hide_index=True,
        )


# -----------------------------
# Clients
# -----------------------------
elif page == "Clients":
    st.title("Clients")

    with st.expander("➕ Add a client", expanded=True):
        with st.form("add_client_form"):
            name = st.text_input("Client name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            status = st.selectbox("Status", ["Active", "Lead", "Inactive"])
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add Client")

            if submitted:
                if name.strip():
                    add_client(name, email, phone, status, notes)
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
                ["name", "email", "phone", "status", "notes"]
            ],
            use_container_width=True,
            hide_index=True,
        )


# -----------------------------
# Goals
# -----------------------------
elif page == "Goals":
    st.title("Goals")

    with st.expander("➕ Add a goal", expanded=True):
        with st.form("add_goal_form"):
            title = st.text_input("Goal")
            category = st.selectbox(
                "Category",
                ["Business", "Fitness", "Financial", "Personal"],
            )
            target_date = st.date_input("Target date", value=date.today())
            progress = st.slider("Current progress", 0, 100, 0)
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
                f"**{goal['title']}** · {goal['category']} · "
                f"Target: {goal['target_date']}"
            )
            st.progress(int(goal["progress"]) / 100)
            st.caption(f"{goal['progress']}% complete")


# -----------------------------
# Message templates
# -----------------------------
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
            "Hi [Client Name], welcome! I’m excited to work with you. "
            "I’ll send over the next steps shortly."
        ),
        "Follow-up after consultation": (
            "Hi [Client Name], it was great speaking with you today. "
            "I wanted to follow up and see if you had any questions."
        ),
        "Class reminder": (
            "Hi [Client Name], this is a reminder about your upcoming class "
            "on [Date] at [Time]. See you soon!"
        ),
        "Payment reminder": (
            "Hi [Client Name], this is a friendly reminder that your payment "
            "is due. Please let me know if you have any questions."
        ),
    }

    st.text_area(
        "Template text",
        value=templates[template_type],
        height=180,
    )

    st.caption("Replace the bracketed words before sending.")
