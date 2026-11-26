import streamlit as st
from dashboard.assignments import show_assignments
from dashboard.courses import show_courses

st.set_page_config(
    page_title="Purdue Student Dashboard",
    page_icon="📚",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    ["Home", "Courses", "Assignments"]
)

# Home page
if page == "Home":
    st.title("Purdue Student Intelligence Dashboard")

    st.write("Welcome to your academic dashboard!")

    st.subheader("Upcoming Assignments")

    st.info("No assignments added yet.")

#Course page
elif page == "Courses":
    show_courses()

# Assignment page
elif page == "Assignments":
    show_assignments()