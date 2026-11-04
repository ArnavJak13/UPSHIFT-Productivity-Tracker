import tkinter as tk
from datetime import date

import analytics
from ui_helpers import make_page_title, draw_line_chart, draw_bar_chart, draw_donut_chart, draw_horizontal_bars


def show(parent, theme, refresh_page=None):
    make_page_title(
        parent,
        "Statistics",
        "Visual summaries of habits, academics, finance, and calendar consistency.",
        theme
    )

    grid = tk.Frame(parent, bg=theme["bg"])
    grid.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    grid.grid_columnconfigure(0, weight=1)
    grid.grid_columnconfigure(1, weight=1)

    boxes = []
    for row in range(3):
        for column in range(2):
            box = tk.Frame(
                grid,
                bg=theme["card"],
                highlightbackground=theme["border"],
                highlightthickness=1
            )
            box.grid(row=row, column=column, padx=6, pady=6, sticky="nsew")
            boxes.append(box)

    habit_labels, habit_values = analytics.weekly_habit_values()
    draw_line_chart(boxes[0], habit_labels, habit_values, "Habit Completion Trend", theme, theme["green"])

    study_labels, study_values = analytics.weekly_study_hours()
    draw_line_chart(boxes[1], study_labels, study_values, "Daily Study Hours", theme, theme["blue"])

    income, expenses, savings = analytics.money_totals_for_month()
    draw_donut_chart(
        boxes[2],
        ["Income", "Expenses", "Savings"],
        [income, expenses, savings],
        "Money Flow This Month",
        theme,
        [theme["green"], theme["red"], theme["blue"]]
    )

    calendar_labels = []
    calendar_values = []
    for day in analytics.get_last_n_days(7):
        calendar_labels.append(day.strftime("%a"))
        calendar_values.append(analytics.calendar_score_for_day(day))

    draw_bar_chart(boxes[3], calendar_labels, calendar_values, "Calendar Consistency", theme)

    categories = analytics.habit_category_percentages(30)
    category_labels = list(categories.keys())
    category_values = list(categories.values())
    draw_horizontal_bars(boxes[4], category_labels, category_values, "Habit Consistency by Category", theme)

    today = date.today()
    today_values = [
        analytics.habit_completion_for_day(today),
        analytics.academic_score_for_day(today),
        analytics.finance_score_for_month(today),
        analytics.calendar_score_for_day(today)
    ]
    draw_donut_chart(
        boxes[5],
        ["Habits", "Academics", "Finance", "Calendar"],
        today_values,
        "Current Domain Balance",
        theme
    )
