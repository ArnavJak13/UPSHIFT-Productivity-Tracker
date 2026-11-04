import tkinter as tk
from datetime import date
from tkinter import messagebox

import database
import date_helpers
from ui_helpers import make_page_title, make_metric_card, styled_button, styled_entry


def show(parent, theme, refresh_page):
    make_page_title(
        parent,
        "Academics",
        "Log study time and assignments. Today changes automatically with the real date.",
        theme
    )

    today_text = date.today().isoformat()
    today_display = date_helpers.today_display()
    today_entries = database.get_academic_entries_between(today_text, today_text)

    study_today = 0
    target_today = 0
    assignments_done = 0
    assignments_total = 0

    for entry in today_entries:
        study_today = study_today + entry["study_hours"]
        target_today = target_today + entry["target_hours"]
        assignments_done = assignments_done + entry["assignments_done"]
        assignments_total = assignments_total + entry["assignments_total"]

    metrics = tk.Frame(parent, bg=theme["bg"])
    metrics.pack(fill="x", padx=24, pady=(0, 12))

    values = [
        ("Study Today", str(round(study_today, 1)) + " h", theme["blue"]),
        ("Target Today", str(round(target_today, 1)) + " h", theme["accent"]),
        ("Assignments", str(assignments_done) + "/" + str(assignments_total), theme["green"])
    ]

    for index in range(len(values)):
        title, value, color = values[index]
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

    history = tk.Frame(body, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1)
    history.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    tk.Label(form, text="Add Academic Entry", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    fields = []
    field_names = ["Date (DD/MM/YYYY)", "Subject", "Study Hours", "Target Hours", "Assignments Done", "Assignments Total", "Notes"]

    for field_name in field_names:
        tk.Label(form, text=field_name, bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
        entry = styled_entry(form, theme, width=28)
        entry.pack(fill="x", padx=15, pady=(3, 8))
        fields.append(entry)

    fields[0].insert(0, today_display)

    def save_entry():
        try:
            display_date = fields[0].get().strip()
            subject = fields[1].get().strip()
            study_hours = float(fields[2].get() or 0)
            target_hours = float(fields[3].get() or 0)
            done = int(fields[4].get() or 0)
            total = int(fields[5].get() or 0)
            notes = fields[6].get().strip()

            entry_date = date_helpers.to_storage_date(display_date)
        except ValueError:
            messagebox.showerror("Invalid input", "Check the date and number fields.")
            return

        if subject == "":
            messagebox.showerror("Missing subject", "Please enter a subject.")
            return

        database.add_academic_entry(
            entry_date,
            subject,
            study_hours,
            target_hours,
            done,
            total,
            notes
        )
        refresh_page()

    styled_button(form, "Save Entry", save_entry, theme).pack(anchor="w", padx=15, pady=(3, 15))

    tk.Label(history, text="Recent Academic History", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    entries = database.get_academic_entries(12)

    if len(entries) == 0:
        tk.Label(history, text="No academic entries yet.", bg=theme["card"], fg=theme["muted"]).pack(anchor="w", padx=15)
    else:
        for entry in entries:
            line = (
                date_helpers.to_display_date(entry["entry_date"]) + "  |  " + entry["subject"] +
                "  |  " + str(entry["study_hours"]) + "h / " + str(entry["target_hours"]) + "h" +
                "  |  Assignments " + str(entry["assignments_done"]) + "/" + str(entry["assignments_total"])
            )
            tk.Label(
                history,
                text=line,
                bg=theme["card"],
                fg=theme["text"],
                font=("Segoe UI", 9),
                anchor="w"
            ).pack(fill="x", padx=15, pady=4)
