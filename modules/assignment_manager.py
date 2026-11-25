
from datetime import date
from database.db import (
    add_assignment,
    get_assignments,
    update_assignment,
    delete_assignment,
    mark_assignment_completed
)


def create_assignment(course_id, name, due_date, estimated_hours, importance):
    if not name or not name.strip():
        raise ValueError("Assignment name cannot be empty.")
    if course_id is None:
        raise ValueError("Please select a course.")
    if due_date is None:
        raise ValueError("Please select a due date.")
    if estimated_hours < 0:
        raise ValueError("Estimated hours cannot be negative.")
    if importance not in (0, 1):
        raise ValueError("Invalid importance value.")

    add_assignment(
        course_id,
        name.strip(),
        due_date.isoformat(),
        estimated_hours,
        importance
    )

def retrieve_assignments():
    return get_assignments()

def remove_assignment(assignment_id):
    delete_assignment(assignment_id)

def edit_assignment(
    assignment_id,
    course_id,
    name,
    due_date,
    estimated_hours,
    importance
):
    if not name or not name.strip():
        raise ValueError("Assignment name cannot be empty.")

    if course_id is None:
        raise ValueError("Please select a course.")

    if due_date is None:
        raise ValueError("Please select a due date.")

    if estimated_hours < 0:
        raise ValueError("Estimated hours cannot be negative.")

    if importance not in (0, 1):
        raise ValueError("Invalid importance value.")

    update_assignment(
        assignment_id,
        course_id,
        name.strip(),
        due_date.isoformat(),
        estimated_hours,
        importance
    )

def complete_assignment(assignment_id, completed):
    mark_assignment_completed(assignment_id, completed)