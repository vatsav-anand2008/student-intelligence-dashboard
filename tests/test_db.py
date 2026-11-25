from database.db import (
    initialize_database,
    add_course,
    get_courses,
    add_assignment,
    get_assignments,
    delete_assignment,
    update_assignment,
    mark_assignment_completed
)

initialize_database()

# Add courses
add_course("Calculus III", "MA 261")
add_course("Object-Oriented Programming", "CS 180")

# Retrieve courses
courses = get_courses()

for course in courses:
    print(course["id"], course["name"], course["code"])

# Add an assignment to the first course
course_id = courses[0]["id"]

add_assignment(
    course_id,
    "Homework 1",
    "2026-12-01",
    2.5,
    1
)

# Retrieve assignments
assignments = get_assignments()

for assignment in assignments:
    print(
        assignment["name"],
        assignment["course_code"],
        assignment["due_date"]
    )

# Delete the assignment
delete_assignment(assignments[0]["id"])