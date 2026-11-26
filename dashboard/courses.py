
import streamlit as st
import sqlite3

from modules.course_manager import (
    create_course,
    retrieve_courses,
    edit_course,
    remove_course
)


def show_courses():
    st.title("Course Manager")

    #Add Course
    st.subheader("Add a Course")

    with st.form("course_form"):

        course_name = st.text_input("Course Name")

        course_code = st.text_input("Course Code")

        submitted = st.form_submit_button("Add Course")

        if submitted:
            try:
                create_course(course_name, course_code)

                st.success("Course added successfully!")
                st.rerun()

            except ValueError as error:
                st.error(str(error))

            except sqlite3.IntegrityError:
                st.error("That course code already exists.")

    st.divider()

    #Display Courses
    st.subheader("Your Courses")

    courses = retrieve_courses()

    if not courses:
        st.info("You haven't added any courses yet.")
        return

    for course in courses:
        with st.expander(f"{course['code']} - {course['name']}"):

            st.write(f"**Course ID:** {course['id']}")
            st.write(f"**Course Name:** {course['name']}")
            st.write(f"**Course Code:** {course['code']}")

            st.divider()

            #Edit Course
            with st.form(f"edit_course_{course['id']}"):
                edited_name = st.text_input(
                    "Course Name",
                    value=course["name"],
                    key=f"name_{course['id']}"
                )

                edited_code = st.text_input(
                    "Course Code",
                    value=course["code"],
                    key=f"code_{course['id']}"
                )

                save_changes = st.form_submit_button("Save Changes")

                if save_changes:
                    try:
                        edit_course(
                            course["id"],
                            edited_name,
                            edited_code
                        )

                        st.success("Course updated successfully!")
                        st.rerun()

                    except ValueError as error:
                        st.error(str(error))

                    except sqlite3.IntegrityError:
                        st.error("That course code already exists.")

            st.divider()

            #Delete Course
            confirm_delete = st.checkbox(
                "I understand that deleting this course also deletes its assignments.",
                key=f"confirm_delete_{course['id']}"
            )

            if st.button(
                "Delete Course",
                key=f"delete_course_{course['id']}",
                disabled=not confirm_delete
            ):
                remove_course(course["id"])
                st.success("Course deleted successfully!")
                st.rerun()