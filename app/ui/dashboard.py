import tkinter as tk
from datetime import date

from app import analytics
from app import database
from app.ui_helpers import make_page_title, make_metric_card, draw_line_chart, draw_bar_chart, draw_donut_chart


def show(parent, theme, refresh_page=None):
    make_page_title(
        parent,
        "Dashboard",
        "A quick view of your progress across the four tracker areas.",
        theme
    )

    today = date.today()
    habit_score = analytics.habit_completion_for_day(today)
    academic_score = analytics.academic_score_for_day(today)
    calendar_score = analytics.calendar_score_for_day(today)
    finance_score = analytics.finance_score_for_month(today)
    overall_score = analytics.overall_score_for_day(today)
    total_xp = analytics.get_total_xp()

    cards = tk.Frame(parent, bg=theme["bg"])
    cards.pack(fill="x", padx=24, pady=(0, 16))

    values = [
        ("Overall", str(overall_score) + "%", theme["accent"]),
        ("Habits Today", str(habit_score) + "%", theme["green"]),
        ("Academics Today", str(academic_score) + "%", theme["blue"]),
        ("Finance", str(finance_score) + "%", theme["yellow"]),
        ("Calendar Today", str(calendar_score) + "%", theme["accent_2"]),
        ("Total XP", total_xp, theme["red"])
    ]

    for index in range(len(values)):
        title, value, color = values[index]
        card = make_metric_card(cards, title, value, color, theme, width=165, height=90)
        card.grid(row=index // 3, column=index % 3, padx=6, pady=6, sticky="nsew")
        cards.grid_columnconfigure(index % 3, weight=1)

    charts = tk.Frame(parent, bg=theme["bg"])
    charts.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    charts.grid_columnconfigure(0, weight=1)
    charts.grid_columnconfigure(1, weight=1)

    left = tk.Frame(charts, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1)
    left.grid(row=0, column=0, padx=(0, 7), pady=6, sticky="nsew")

    right = tk.Frame(charts, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1)
    right.grid(row=0, column=1, padx=(7, 0), pady=6, sticky="nsew")

    bottom = tk.Frame(charts, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1)
    bottom.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky="nsew")

    labels, overall_values = analytics.weekly_overall_values()
    draw_line_chart(left, labels, overall_values, "7 Day Overall Progress", theme, theme["accent"])

    donut_labels = ["Habits", "Academics", "Finance", "Calendar"]
    donut_values = [habit_score, academic_score, finance_score, calendar_score]
    draw_donut_chart(right, donut_labels, donut_values, "Today's Balance", theme)

    study_labels, study_values = analytics.weekly_study_hours()
    draw_bar_chart(bottom, study_labels, study_values, "Study Hours This Week", theme)
