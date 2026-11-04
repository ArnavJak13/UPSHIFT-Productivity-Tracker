"""Simple calculation functions used by Dashboard and Statistics."""

from datetime import date, timedelta, datetime

from app import database


WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def habit_is_scheduled(habit, day):
    """Return True if a habit should appear on the given date."""
    if habit["active"] == 0:
        return False

    created_date = datetime.strptime(habit["created_date"], "%Y-%m-%d").date()
    if day < created_date:
        return False

    if habit["frequency"] == "Daily":
        return True

    selected_days = habit["days"].split(",")
    today_name = WEEKDAY_NAMES[day.weekday()]
    return today_name in selected_days


def get_scheduled_habits(day):
    habits = database.get_active_habits()
    scheduled = []

    for habit in habits:
        if habit_is_scheduled(habit, day):
            scheduled.append(habit)

    return scheduled


def habit_completion_for_day(day):
    habits = get_scheduled_habits(day)

    if len(habits) == 0:
        return 0

    completed = 0
    day_text = day.isoformat()

    for habit in habits:
        if database.habit_is_completed(habit["id"], day_text):
            completed = completed + 1

    return round((completed / len(habits)) * 100)


def academic_score_for_day(day):
    entries = database.get_academic_entries_between(day.isoformat(), day.isoformat())

    total_hours = 0
    target_hours = 0
    assignments_done = 0
    assignments_total = 0

    for entry in entries:
        total_hours = total_hours + entry["study_hours"]
        target_hours = target_hours + entry["target_hours"]
        assignments_done = assignments_done + entry["assignments_done"]
        assignments_total = assignments_total + entry["assignments_total"]

    hour_score = 0
    if target_hours > 0:
        hour_score = (total_hours / target_hours) * 100
        if hour_score > 100:
            hour_score = 100

    assignment_score = 0
    if assignments_total > 0:
        assignment_score = (assignments_done / assignments_total) * 100

    if target_hours == 0 and assignments_total == 0:
        return 0

    if target_hours == 0:
        return round(assignment_score)

    if assignments_total == 0:
        return round(hour_score)

    return round((hour_score + assignment_score) / 2)


def finance_score_for_month(day):
    start_date = day.replace(day=1)

    if day.month == 12:
        next_month = date(day.year + 1, 1, 1)
    else:
        next_month = date(day.year, day.month + 1, 1)

    end_date = next_month - timedelta(days=1)
    entries = database.get_finance_entries_between(
        start_date.isoformat(),
        end_date.isoformat()
    )

    expenses = 0
    for entry in entries:
        if entry["entry_type"] == "Expense":
            expenses = expenses + entry["amount"]

    budget_text = database.get_setting("monthly_budget", "0")
    try:
        budget = float(budget_text)
    except ValueError:
        budget = 0

    if budget <= 0:
        return 0

    if expenses <= budget:
        score = 100 - ((expenses / budget) * 30)
    else:
        overspend = expenses - budget
        score = 70 - ((overspend / budget) * 100)

    if score < 0:
        score = 0
    if score > 100:
        score = 100

    return round(score)


def calendar_score_for_day(day):
    events = database.get_events_for_date(day.isoformat())

    if len(events) == 0:
        return 0

    completed = 0
    for event in events:
        if event["completed"] == 1:
            completed = completed + 1

    return round((completed / len(events)) * 100)


def overall_score_for_day(day):
    scores = [
        habit_completion_for_day(day),
        academic_score_for_day(day),
        finance_score_for_month(day),
        calendar_score_for_day(day)
    ]

    useful_scores = []
    for score in scores:
        if score > 0:
            useful_scores.append(score)

    if len(useful_scores) == 0:
        return 0

    total = 0
    for score in useful_scores:
        total = total + score

    return round(total / len(useful_scores))


def get_total_xp():
    completions = database.get_all_habit_completions()
    total = 0

    for completion in completions:
        total = total + completion["xp_earned"]

    return total


def get_last_n_days(number_of_days):
    days = []
    today = date.today()

    for offset in range(number_of_days - 1, -1, -1):
        days.append(today - timedelta(days=offset))

    return days


def weekly_overall_values():
    labels = []
    values = []

    for day in get_last_n_days(7):
        labels.append(day.strftime("%a"))
        values.append(overall_score_for_day(day))

    return labels, values


def weekly_study_hours():
    labels = []
    values = []

    for day in get_last_n_days(7):
        entries = database.get_academic_entries_between(
            day.isoformat(),
            day.isoformat()
        )

        total = 0
        for entry in entries:
            total = total + entry["study_hours"]

        labels.append(day.strftime("%a"))
        values.append(round(total, 1))

    return labels, values


def weekly_habit_values():
    labels = []
    values = []

    for day in get_last_n_days(7):
        labels.append(day.strftime("%a"))
        values.append(habit_completion_for_day(day))

    return labels, values


def money_totals_for_month():
    today = date.today()
    start_date = today.replace(day=1)

    if today.month == 12:
        next_month = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)

    end_date = next_month - timedelta(days=1)
    entries = database.get_finance_entries_between(
        start_date.isoformat(),
        end_date.isoformat()
    )

    income = 0
    expenses = 0
    savings = 0

    for entry in entries:
        if entry["entry_type"] == "Income":
            income = income + entry["amount"]
        elif entry["entry_type"] == "Expense":
            expenses = expenses + entry["amount"]
        elif entry["entry_type"] == "Saving":
            savings = savings + entry["amount"]

    return income, expenses, savings


def habit_category_percentages(days_back=30):
    today = date.today()
    start_day = today - timedelta(days=days_back - 1)
    habits = database.get_active_habits()
    result = {}

    for habit in habits:
        category = habit["category"]
        if category not in result:
            result[category] = {"scheduled": 0, "completed": 0}

        current_day = start_day
        while current_day <= today:
            if habit_is_scheduled(habit, current_day):
                result[category]["scheduled"] = result[category]["scheduled"] + 1

                if database.habit_is_completed(habit["id"], current_day.isoformat()):
                    result[category]["completed"] = result[category]["completed"] + 1

            current_day = current_day + timedelta(days=1)

    percentages = {}
    for category in result:
        scheduled = result[category]["scheduled"]
        completed = result[category]["completed"]

        if scheduled == 0:
            percentages[category] = 0
        else:
            percentages[category] = round((completed / scheduled) * 100)

    return percentages
