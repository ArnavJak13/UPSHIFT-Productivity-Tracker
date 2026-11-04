import tkinter as tk
from datetime import date
from tkinter import messagebox

import analytics
import database
from ui_helpers import make_page_title, make_metric_card, styled_button, styled_entry


DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def show(parent, theme, refresh_page):
    make_page_title(
        parent,
        "Habits",
        "Create scheduled habits, complete today's habits, and earn XP.",
        theme
    )

    today = date.today()
    today_text = today.isoformat()
    scheduled_habits = analytics.get_scheduled_habits(today)
    completed_count = 0

    for habit in scheduled_habits:
        if database.habit_is_completed(habit["id"], today_text):
            completed_count = completed_count + 1

    metrics = tk.Frame(parent, bg=theme["bg"])
    metrics.pack(fill="x", padx=24, pady=(0, 12))

    completion_text = str(completed_count) + "/" + str(len(scheduled_habits))
    cards = [
        ("Today's Habits", completion_text, theme["green"]),
        ("Completion", str(analytics.habit_completion_for_day(today)) + "%", theme["accent"]),
        ("Total XP", analytics.get_total_xp(), theme["yellow"])
    ]

    for index in range(len(cards)):
        title, value, color = cards[index]
        card = make_metric_card(metrics, title, value, color, theme, width=210, height=90)
        card.grid(row=0, column=index, padx=6, sticky="nsew")
        metrics.grid_columnconfigure(index, weight=1)

    body = tk.Frame(parent, bg=theme["bg"])
    body.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    body.grid_columnconfigure(0, weight=2)
    body.grid_columnconfigure(1, weight=3)
    body.grid_rowconfigure(0, weight=1)

    form = tk.Frame(body, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1)
    form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

    today_card = tk.Frame(body, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1)
    today_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    tk.Label(form, text="Create Habit", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    tk.Label(form, text="Habit name", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    name_entry = styled_entry(form, theme)
    name_entry.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="Category", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    category_var = tk.StringVar(value="Personal")
    category_menu = tk.OptionMenu(form, category_var, "Personal", "Health", "Fitness", "Academics", "Other")
    category_menu.config(bg=theme["input"], fg=theme["text"], relief="flat", highlightthickness=0)
    category_menu.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="XP Reward", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    xp_var = tk.StringVar(value="10")
    xp_menu = tk.OptionMenu(form, xp_var, "5", "10", "15", "20")
    xp_menu.config(bg=theme["input"], fg=theme["text"], relief="flat", highlightthickness=0)
    xp_menu.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="Frequency", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    frequency_var = tk.StringVar(value="Daily")
    frequency_menu = tk.OptionMenu(form, frequency_var, "Daily", "Selected Days")
    frequency_menu.config(bg=theme["input"], fg=theme["text"], relief="flat", highlightthickness=0)
    frequency_menu.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="Days (used for Selected Days)", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(4, 4))

    days_frame = tk.Frame(form, bg=theme["card"])
    days_frame.pack(fill="x", padx=15, pady=(0, 10))
    day_variables = []

    for day_name in DAY_NAMES:
        variable = tk.IntVar(value=0)
        checkbox = tk.Checkbutton(
            days_frame,
            text=day_name,
            variable=variable,
            bg=theme["card"],
            fg=theme["text"],
            selectcolor=theme["input"],
            activebackground=theme["card"],
            activeforeground=theme["text"]
        )
        checkbox.pack(side="left")
        day_variables.append(variable)

    def save_habit():
        name = name_entry.get().strip()
        frequency = frequency_var.get()
        selected_days = []

        for index in range(len(DAY_NAMES)):
            if day_variables[index].get() == 1:
                selected_days.append(DAY_NAMES[index])

        if name == "":
            messagebox.showerror("Missing name", "Please enter a habit name.")
            return

        if frequency == "Selected Days" and len(selected_days) == 0:
            messagebox.showerror("Missing days", "Select at least one day.")
            return

        days_text = ",".join(selected_days)
        database.add_habit(
            name,
            category_var.get(),
            int(xp_var.get()),
            frequency,
            days_text
        )
        refresh_page()

    styled_button(form, "Create Habit", save_habit, theme).pack(anchor="w", padx=15, pady=(2, 15))

    tk.Label(today_card, text="Today's Habits", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    if len(scheduled_habits) == 0:
        tk.Label(today_card, text="No habits are scheduled for today.", bg=theme["card"], fg=theme["muted"]).pack(anchor="w", padx=15)
    else:
        for habit in scheduled_habits:
            row = tk.Frame(today_card, bg=theme["input"])
            row.pack(fill="x", padx=15, pady=4)

            completed = database.habit_is_completed(habit["id"], today_text)
            status = "✓" if completed else "○"

            tk.Label(
                row,
                text=status + "  " + habit["name"],
                font=("Segoe UI", 10, "bold"),
                bg=theme["input"],
                fg=theme["text"]
            ).pack(side="left", padx=10, pady=10)

            tk.Label(
                row,
                text=habit["category"] + "  •  " + str(habit["xp_reward"]) + " XP",
                bg=theme["input"],
                fg=theme["muted"]
            ).pack(side="left", padx=8)

            habit_id = habit["id"]
            habit_xp = habit["xp_reward"]

            def toggle_this_habit(habit_id=habit_id, habit_xp=habit_xp):
                database.toggle_habit_completion(habit_id, today_text, habit_xp)
                refresh_page()

            button_text = "Undo" if completed else "Complete"
            button_color = theme["muted"] if completed else theme["green"]
            styled_button(row, button_text, toggle_this_habit, theme, button_color, width=9).pack(side="right", padx=8, pady=6)
