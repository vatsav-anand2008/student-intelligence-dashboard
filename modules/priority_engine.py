from datetime import date

def classify_assignment(assignment):
    """
    Classifies an assignment into an Eisenhower quadrant.
    """

    due_date = date.fromisoformat(assignment["due_date"])
    today = date.today()

    days_remaining = (due_date - today).days

    urgent = days_remaining <= 2
    important = assignment["importance"] == 1

    if urgent and important:
        return "Do First"

    elif not urgent and important:
        return "Schedule"

    elif urgent and not important:
        return "Do Later"

    else:
        return "Optional"
