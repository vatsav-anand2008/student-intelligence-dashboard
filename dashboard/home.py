
import streamlit as st
import pandas as pd
from datetime import date
import altair as alt
from database.db import get_assignments
from modules.priority_engine import classify_assignment
from modules.workload import calculate_weekly_workload


def show_home():
    st.title("Purdue Student Intelligence Dashboard")
    st.write("Welcome! Here's an overview of your academic workload.")

    # Retrieve assignments
    assignments = get_assignments()

    # Separate completed and incomplete assignments
    active_assignments = [
        assignment for assignment in assignments
        if not assignment["completed"]
    ]

    completed_assignments = [
        assignment for assignment in assignments
        if assignment["completed"]
    ]

    # Calculate dashboard statistics
    today = date.today()

    due_soon = [
        assignment for assignment in active_assignments
        if 0 <= (date.fromisoformat(assignment["due_date"]) - today).days <= 2
    ]

    total_hours = sum(
        assignment["estimated_hours"] or 0
        for assignment in active_assignments
    )

    # Display statistics
    st.subheader("Your Academic Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Active Assignments", len(active_assignments))
    col2.metric("Due Within 2 Days", len(due_soon))
    col3.metric("Completed Assignments", len(completed_assignments))

    st.caption(f"Estimated remaining workload: {total_hours:.1f} hours")

    st.divider()

    # Upcoming deadlines
    st.subheader("Upcoming Deadlines")
    
    upcoming = sorted(
        active_assignments,
        key=lambda assignment: assignment["due_date"]
    )
    
    upcoming = [
        assignment for assignment in upcoming
        if date.fromisoformat(assignment["due_date"]) >= today
    ]
    
    if not upcoming:
        st.success("No upcoming deadlines!")
    else:
        for assignment in upcoming[:5]:
            st.write(
                f"**{assignment['name']}** "
                f"({assignment['course_code']})"
            )
            st.caption(f"Due: {assignment['due_date']}")

    # Classify assignments into Eisenhower quadrants
    quadrants = {
        "Do First": [],
        "Schedule": [],
        "Do Later": [],
        "Optional": []
    }

    for assignment in active_assignments:
        category = classify_assignment(assignment)
        quadrants[category].append(assignment)

    # Sort assignments by due date
    for category in quadrants:
        quadrants[category].sort(
            key=lambda assignment: assignment["due_date"]
        )

    # Display Eisenhower Matrix
    st.subheader("Your Eisenhower Matrix")

    st.write(
        "Prioritize your assignments based on urgency and importance."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 Do First")
        st.caption("Urgent and important")

        display_quadrant(quadrants["Do First"])

        st.markdown("### 🟠 Do Later")
        st.caption("Urgent but less important")

        display_quadrant(quadrants["Do Later"])

    with col2:
        st.markdown("### 🔵 Schedule")
        st.caption("Important but not urgent")

        display_quadrant(quadrants["Schedule"])

        st.markdown("### ⚪ Optional")
        st.caption("Neither urgent nor important")

        display_quadrant(quadrants["Optional"])

    st.divider()
    
    # Weekly Workload
    st.subheader("Weekly Workload")

    workload = calculate_weekly_workload(assignments)

    # Create readable weekday labels in chronological order
    day_labels = [
        day.strftime("%a %b %d")
        for day in workload.keys()
    ]

    workload_df = pd.DataFrame({
        "Day": day_labels,
        "Planned Hours": list(workload.values())
    })

    # Calculate total hours
    total_hours = sum(workload.values())

    st.metric(
        "Total Planned Hours This Week",
        f"{total_hours:.1f} hours"
    )

    # Create chart with an explicitly ordered categorical axis
    chart = alt.Chart(workload_df).mark_bar().encode(
        x=alt.X(
            "Day:N",
            sort=day_labels,
            axis=alt.Axis(
                title="Day",
                labelAngle=0
            )
        ),
        y=alt.Y(
            "Planned Hours:Q",
            title="Estimated Hours",
            scale=alt.Scale(domainMin=0)
        ),
        tooltip=[
            alt.Tooltip("Day:N"),
            alt.Tooltip("Planned Hours:Q", format=".2f")
        ]
    ).properties(
        height=350
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )

    st.caption(
        "Estimated hours are distributed evenly across each "
        "assignment's planned date range."
    )

def display_quadrant(assignments):

    if not assignments:
        st.info("No assignments here!")

    for assignment in assignments:
        with st.container(border=True):

            st.write(f"**{assignment['name']}**")
            st.caption(
                f"{assignment['course_code']} | "
                f"Due: {assignment['due_date']}"
            )

            if assignment["estimated_hours"] is not None:
                st.caption(
                    f"Estimated time: "
                    f"{assignment['estimated_hours']} hours"
                )