
from datetime import date, timedelta


def calculate_weekly_workload(assignments, week_start=None):
    """
    Calculate the planned workload for each day of a week.

    Each assignment's estimated hours are distributed evenly
    across its planned start and target completion dates.
    """

    if week_start is None:
        week_start = date.today()

    # Find Monday of the selected week
    monday = week_start - timedelta(days=week_start.weekday())

    # Initialize all seven days to zero hours
    workload = {}

    for i in range(7):
        current_day = monday + timedelta(days=i)
        workload[current_day] = 0.0

    # Process each assignment
    for assignment in assignments:

        # Ignore completed assignments
        if assignment["completed"]:
            continue

        # Skip assignments without planned dates
        if not assignment["planned_start_date"]:
            continue

        if not assignment["target_completion_date"]:
            continue

        # Retrieve assignment information
        start_date = date.fromisoformat(
            assignment["planned_start_date"]
        )

        end_date = date.fromisoformat(
            assignment["target_completion_date"]
        )

        estimated_hours = assignment["estimated_hours"] or 0

        # Avoid invalid date ranges
        if end_date < start_date:
            continue

        # Calculate hours assigned to each day
        total_days = (end_date - start_date).days + 1

        daily_hours = estimated_hours / total_days

        # Add the assignment's hours to the relevant days
        for current_day in workload:

            if start_date <= current_day <= end_date:
                workload[current_day] += daily_hours

    return workload
