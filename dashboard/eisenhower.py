import streamlit as st

from database.db import get_assignments
from modules.priority_engine import classify_assignment


def show_eisenhower():

    st.title("Eisenhower Matrix")

    assignments = get_assignments()

    # Remove completed assignments
    assignments = [
        assignment for assignment in assignments
        if not assignment["completed"]
    ]

    # Create four quadrants
    quadrants = {
        "Do First": [],
        "Schedule": [],
        "Do Later": [],
        "Optional": []
    }

    # Classify every assignment
    for assignment in assignments:
        category = classify_assignment(assignment)
        quadrants[category].append(assignment)

    # Display quadrants
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔴 Do First")
        for assignment in quadrants["Do First"]:
            st.write(
                f"**{assignment['name']}**"
                f" — {assignment['course_code']}"
            )
            st.caption(f"Due: {assignment['due_date']}")

        st.divider()

        st.subheader("🟠 Do Later")
        for assignment in quadrants["Do Later"]:
            st.write(
                f"**{assignment['name']}**"
                f" — {assignment['course_code']}"
            )
            st.caption(f"Due: {assignment['due_date']}")

    with col2:
        st.subheader("🔵 Schedule")
        for assignment in quadrants["Schedule"]:
            st.write(
                f"**{assignment['name']}**"
                f" — {assignment['course_code']}"
            )
            st.caption(f"Due: {assignment['due_date']}")

        st.divider()

        st.subheader("⚪ Optional")
        for assignment in quadrants["Optional"]:
            st.write(
                f"**{assignment['name']}**"
                f" — {assignment['course_code']}"
            )
            st.caption(f"Due: {assignment['due_date']}")