import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).resolve().parent / "dashboard.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database():
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                due_date TEXT NOT NULL,
                estimated_hours REAL,
                importance INTEGER NOT NULL CHECK (importance IN (0, 1)),
                planned_start_date TEXT,
                target_completion_date TEXT,
                completed INTEGER NOT NULL DEFAULT 0,

                FOREIGN KEY (course_id)
                    REFERENCES courses (id)
                    ON DELETE CASCADE
            )
        """)

    conn.close()

def migrate_database():
    conn = get_connection()

    # Get the existing columns in the assignments table
    columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(assignments)").fetchall()
    ]

    with conn:
        if "planned_start_date" not in columns:
            conn.execute("""
                ALTER TABLE assignments
                ADD COLUMN planned_start_date TEXT
            """)

        if "target_completion_date" not in columns:
            conn.execute("""
                ALTER TABLE assignments
                ADD COLUMN target_completion_date TEXT
            """)

    conn.close()

def add_course(course_name, course_code):
    conn = get_connection()

    with conn:
        conn.execute("""
            INSERT INTO courses (name, code)
            VALUES (?, ?)
        """, (course_name, course_code))
    conn.close()

def get_courses():
    conn = get_connection()
    
    with conn:
        cursor = conn.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
    conn.close()
    return courses

def update_course(course_id, course_name, course_code):
    conn = get_connection()

    with conn:
        conn.execute("""
            UPDATE courses
            SET name = ?, code = ?
            WHERE id = ?
        """, (course_name, course_code, course_id))

    conn.close()

def delete_course(course_id):
    conn = get_connection()

    with conn:
        conn.execute("""
            DELETE FROM courses
            WHERE id = ?
        """, (course_id,))

    conn.close()

def add_assignment(course_id, name, due_date, estimated_hours, importance, planned_start_date, target_completion_date):
    conn = get_connection()

    with conn:
        conn.execute("""
            INSERT INTO assignments (
                course_id,
                name,
                due_date,
                estimated_hours,
                importance,
                planned_start_date,
                target_completion_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            course_id,
            name,
            due_date,
            estimated_hours,
            importance,
            planned_start_date,
            target_completion_date
        ))

    conn.close()
    
def get_assignments():
    conn = get_connection()

    with conn:
        cursor = conn.execute("""
            SELECT
                assignments.id,
                assignments.course_id,
                assignments.name,
                assignments.due_date,
                assignments.estimated_hours,
                assignments.importance,
                assignments.planned_start_date,
                assignments.target_completion_date,
                assignments.completed,
                courses.name AS course_name,
                courses.code AS course_code
            FROM assignments
            JOIN courses
                ON assignments.course_id = courses.id
            ORDER BY assignments.due_date ASC
        """)

        assignments = cursor.fetchall()

    conn.close()
    return assignments

def delete_assignment(assignment_id):
    conn = get_connection()

    with conn:
        conn.execute("""
            DELETE FROM assignments
            WHERE id = ?
        """, (assignment_id,))

    conn.close()

def update_assignment(assignment_id, course_id, name, due_date, estimated_hours, importance, planned_start_date, target_completion_date):
    conn = get_connection()

    with conn:
        conn.execute("""
            UPDATE assignments
            SET course_id = ?,
                name = ?,
                due_date = ?,
                estimated_hours = ?,
                importance = ?,
                planned_start_date = ?,
                target_completion_date = ?
            WHERE id = ?
        """, (
            course_id,
            name,
            due_date,
            estimated_hours,
            importance,
            planned_start_date,
            target_completion_date,
            assignment_id
        ))

    conn.close()

def mark_assignment_completed(assignment_id, completed):
    conn = get_connection()

    with conn:
        conn.execute("""
            UPDATE assignments
            SET completed = ?
            WHERE id = ?
        """, (int(completed), assignment_id))

    conn.close()