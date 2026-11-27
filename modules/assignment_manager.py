from database.db import (
    add_assignment,
    get_assignments,
    update_assignment,
    delete_assignment,
    mark_assignment_completed
)


def validate_assignment(course_id, name, due_date, estimated_hours, importance, planned_start_date, target_completion_date):
    if not name or not name.strip():
        raise ValueError("Assignment name cannot be empty.")
    if course_id is None:
        raise ValueError("Please select a course.")
    if estimated_hours is not None and estimated_hours < 0:
        raise ValueError("Estimated hours cannot be negative.")
    if importance not in (0, 1):
        raise ValueError("Importance must be 0 or 1.")
    if planned_start_date > target_completion_date:
        raise ValueError("Start date cannot be after target completion.")
    if target_completion_date > due_date:
        raise ValueError("Target completion cannot be after the due date.")

def create_assignment(
    course_id,
    name,
    due_date,
    estimated_hours,
    importance,
    planned_start_date,
    target_completion_date
):
    validate_assignment(
        course_id,
        name,
        due_date,
        estimated_hours,
        importance,
        planned_start_date,
        target_completion_date
    )

    add_assignment(
        course_id,
        name.strip(),
        due_date.isoformat(),
        estimated_hours,
        importance,
        planned_start_date.isoformat(),
        target_completion_date.isoformat()
    )

def retrieve_assignments():
    return get_assignments()

def remove_assignment(assignment_id):
    delete_assignment(assignment_id)

def edit_assignment(assignment_id, course_id, name, due_date, estimated_hours, importance, planned_start_date, target_completion_date):
    validate_assignment(
        course_id,
        name,
        due_date,
        estimated_hours,
        importance,
        planned_start_date,
        target_completion_date
    )

    update_assignment(
        assignment_id,
        course_id,
        name.strip(),
        due_date.isoformat(),
        estimated_hours,
        importance,
        planned_start_date.isoformat(),
        target_completion_date.isoformat()
    )

def complete_assignment(assignment_id, completed):
    mark_assignment_completed(assignment_id, completed)
