from database.db import (
    add_course,
    get_courses,
    update_course,
    delete_course
)

def create_course(course_name, course_code):
    if not course_name or not course_name.strip():
        raise ValueError("Course name cannot be empty.")

    if not course_code or not course_code.strip():
        raise ValueError("Course code cannot be empty.")

    add_course(
        course_name.strip(),
        course_code.strip().upper()
    )

def retrieve_courses():
    return get_courses()

def edit_course(course_id, course_name, course_code):
    if not course_name or not course_name.strip():
        raise ValueError("Course name cannot be empty.")

    if not course_code or not course_code.strip():
        raise ValueError("Course code cannot be empty.")

    update_course(
        course_id,
        course_name.strip(),
        course_code.strip().upper()
    )

def remove_course(course_id):
    delete_course(course_id)