import tkinter as tk
from datetime import date
from tkinter import messagebox

import analytics
import database
import date_helpers
from ui_helpers import make_page_title, make_metric_card, styled_button, styled_entry


def show(parent, theme, refresh_page):
    make_page_title(
        parent,
        "Finance",
        "Track expenses, income, savings, and your monthly budget.",
        theme
    )

    income, expenses, savings = analytics.money_totals_for_month()
    budget_text = database.get_setting("monthly_budget", "0")

    try:
        budget = float(budget_text)
    except ValueError:
        budget = 0

    remaining = budget - expenses

    metrics = tk.Frame(parent, bg=theme["bg"])
    metrics.pack(fill="x", padx=24, pady=(0, 12))

    values = [
        ("Income", "₹" + str(round(income, 2)), theme["green"]),
        ("Expenses", "₹" + str(round(expenses, 2)), theme["red"]),
        ("Savings", "₹" + str(round(savings, 2)), theme["blue"]),
        ("Budget Left", "₹" + str(round(remaining, 2)), theme["yellow"])
    ]

    for index in range(len(values)):
        title, value, color = values[index]
        card = make_metric_card(metrics, title, value, color, theme, width=175, height=90)
        card.grid(row=0, column=index, padx=5, sticky="nsew")
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

    tk.Label(form, text="Add Finance Entry", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    tk.Label(form, text="Date (DD/MM/YYYY)", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    date_entry = styled_entry(form, theme)
    date_entry.pack(fill="x", padx=15, pady=(3, 8))
    date_entry.insert(0, date_helpers.today_display())

    tk.Label(form, text="Type", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    type_var = tk.StringVar(value="Expense")
    type_menu = tk.OptionMenu(form, type_var, "Expense", "Income", "Saving")
    type_menu.config(bg=theme["input"], fg=theme["text"], relief="flat", highlightthickness=0)
    type_menu.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="Category", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    category_entry = styled_entry(form, theme)
    category_entry.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="Amount", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    amount_entry = styled_entry(form, theme)
    amount_entry.pack(fill="x", padx=15, pady=(3, 8))

    tk.Label(form, text="Notes", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    notes_entry = styled_entry(form, theme)
    notes_entry.pack(fill="x", padx=15, pady=(3, 8))

    def save_entry():
        try:
            display_date = date_entry.get().strip()
            entry_date = date_helpers.to_storage_date(display_date)
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Check the date and amount.")
            return

        category = category_entry.get().strip()
        if category == "":
            messagebox.showerror("Missing category", "Please enter a category.")
            return

        database.add_finance_entry(
            entry_date,
            type_var.get(),
            category,
            amount,
            notes_entry.get().strip()
        )
        refresh_page()

    styled_button(form, "Save Entry", save_entry, theme).pack(anchor="w", padx=15, pady=(5, 15))

    tk.Label(history, text="Recent Finance History", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    entries = database.get_finance_entries(14)
    if len(entries) == 0:
        tk.Label(history, text="No finance entries yet.", bg=theme["card"], fg=theme["muted"]).pack(anchor="w", padx=15)
    else:
        for entry in entries:
            color = theme["red"]
            if entry["entry_type"] == "Income":
                color = theme["green"]
            elif entry["entry_type"] == "Saving":
                color = theme["blue"]

            text = (
                date_helpers.to_display_date(entry["entry_date"]) + "  |  " + entry["entry_type"] +
                "  |  " + entry["category"] + "  |  ₹" + str(round(entry["amount"], 2))
            )
            tk.Label(history, text=text, bg=theme["card"], fg=color, font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=4)
