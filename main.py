import streamlit as st
from dashboard.assignments import show_assignments
from dashboard.courses import show_courses
from dashboard.home import show_home
from database.db import initialize_database, migrate_database

st.set_page_config(
    page_title="Purdue Student Dashboard",
    page_icon="📚",
    layout="wide"
)

initialize_database()
migrate_database()

# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    ["Home", "Courses", "Assignments"]
)

# Home page
if page == "Home":
    show_home()

#Course page
elif page == "Courses":
    show_courses()

# Assignment page
elif page == "Assignments":
    show_assignments()