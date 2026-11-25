
import streamlit as st
from datetime import date

from database.db import get_courses
from modules.assignment_manager import (
    create_assignment,
    retrieve_assignments,
    remove_assignment,
    edit_assignment,
    complete_assignment
)


def show_assignments():
    st.title("Assignment Manager")

    courses = get_courses()

    if not courses:
        st.warning("Please add a course first.")
        return

    course_options = {
        f"{course['code']} - {course['name']}": course['id']
        for course in courses
    }

    #Add Assignment
    st.subheader("Add an Assignment")

    with st.form("assignment_form"):
        selected_course = st.selectbox(
            "Course",
            options=list(course_options.keys())
        )

        assignment_name = st.text_input("Assignment Name")

        due_date = st.date_input("Due Date")

        estimated_hours = st.number_input(
            "Estimated Completion Hours",
            min_value=0.0,
            step=0.5
        )

        importance = st.selectbox(
            "Importance",
            ["Important", "Not Important"]
        )

        submitted = st.form_submit_button("Add Assignment")

        if submitted:
            try:
                create_assignment(
                    course_options[selected_course],
                    assignment_name,
                    due_date,
                    estimated_hours,
                    1 if importance == "Important" else 0
                )

                st.success("Assignment added successfully!")
                st.rerun()

            except ValueError as error:
                st.error(str(error))

    st.divider()

    #Display Assignments
    st.subheader("Your Assignments")

    assignments = retrieve_assignments()

    if not assignments:
        st.info("You haven't added any assignments yet.")
        return

    for assignment in assignments:
        with st.expander(
            f"{assignment['name']} - {assignment['course_code']}"
        ):
            st.write(f"**Course:** {assignment['course_name']}")
            st.write(f"**Due Date:** {assignment['due_date']}")
            st.write(f"**Estimated Hours:** {assignment['estimated_hours']}")
            st.write(
                f"**Importance:** "
                f"{'Important' if assignment['importance'] else 'Not Important'}"
            )

            #Completion Checkbox
            completed = st.checkbox(
                "Completed",
                value=bool(assignment["completed"]),
                key=f"completed_{assignment['id']}"
            )

            if completed != bool(assignment["completed"]):
                complete_assignment(assignment["id"], completed)
                st.rerun()

            st.divider()


            #Edit Assignment
            with st.form(f"edit_{assignment['id']}"):
                current_course = next(
                    course_name
                    for course_name, course_id in course_options.items()
                    if course_id == assignment["course_id"]
                )

                edited_course = st.selectbox(
                    "Course",
                    options=list(course_options.keys()),
                    index=list(course_options.keys()).index(current_course)
                )

                edited_name = st.text_input(
                    "Assignment Name",
                    value=assignment["name"]
                )

                edited_date = st.date_input(
                    "Due Date",
                    value=date.fromisoformat(assignment["due_date"])
                )

                edited_hours = st.number_input(
                    "Estimated Hours",
                    min_value=0.0,
                    value=float(assignment["estimated_hours"] or 0),
                    step=0.5
                )

                edited_importance = st.selectbox(
                    "Importance",
                    ["Important", "Not Important"],
                    index=0 if assignment["importance"] == 1 else 1
                )

                save_changes = st.form_submit_button("Save Changes")

                if save_changes:
                    try:
                        edit_assignment(
                            assignment["id"],
                            course_options[edited_course],
                            edited_name,
                            edited_date,
                            edited_hours,
                            1 if edited_importance == "Important" else 0
                        )

                        st.success("Assignment updated!")
                        st.rerun()

                    except ValueError as error:
                        st.error(str(error))


            #Delete Assignment
            if st.button(
                "Delete Assignment",
                key=f"delete_{assignment['id']}"
            ):
                remove_assignment(assignment["id"])
                st.success("Assignment deleted!")
                st.rerun()