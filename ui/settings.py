import tkinter as tk
from tkinter import messagebox

import database
from ui_helpers import make_page_title, styled_button, styled_entry


def show(parent, theme, refresh_page, change_theme):
    make_page_title(
        parent,
        "Settings",
        "Change your profile, monthly budget, appearance, or reset tracker data.",
        theme
    )

    card = tk.Frame(
        parent,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    card.pack(fill="x", padx=24, pady=(0, 18))

    tk.Label(card, text="Profile", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=18, pady=(18, 10))

    tk.Label(card, text="Display name", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=18)
    name_entry = styled_entry(card, theme, width=30)
    name_entry.pack(anchor="w", padx=18, pady=(3, 10))
    name_entry.insert(0, database.get_setting("display_name", ""))

    tk.Label(card, text="Monthly budget", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=18)
    budget_entry = styled_entry(card, theme, width=30)
    budget_entry.pack(anchor="w", padx=18, pady=(3, 10))
    budget_entry.insert(0, database.get_setting("monthly_budget", "0"))

    def save_profile():
        name = name_entry.get().strip()
        budget = budget_entry.get().strip()

        if name == "":
            messagebox.showerror("Missing name", "Display name cannot be empty.")
            return

        try:
            float(budget)
        except ValueError:
            messagebox.showerror("Invalid budget", "Budget must be a number.")
            return

        database.save_setting("display_name", name)
        database.save_setting("monthly_budget", budget)
        messagebox.showinfo("Saved", "Settings saved.")

    styled_button(card, "Save Profile", save_profile, theme).pack(anchor="w", padx=18, pady=(0, 18))

    appearance = tk.Frame(
        parent,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    appearance.pack(fill="x", padx=24, pady=(0, 18))

    tk.Label(appearance, text="Appearance", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=18, pady=(18, 10))

    theme_var = tk.StringVar(value=database.get_setting("theme", "Light"))
    theme_menu = tk.OptionMenu(appearance, theme_var, "Light", "Dark")
    theme_menu.config(bg=theme["input"], fg=theme["text"], relief="flat", highlightthickness=0, width=15)
    theme_menu.pack(anchor="w", padx=18, pady=(0, 10))

    def apply_theme():
        database.save_setting("theme", theme_var.get())
        change_theme(theme_var.get())

    styled_button(appearance, "Apply Theme", apply_theme, theme).pack(anchor="w", padx=18, pady=(0, 18))

    danger = tk.Frame(
        parent,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    danger.pack(fill="x", padx=24, pady=(0, 18))

    tk.Label(danger, text="Reset Tracker Data", font=("Segoe UI", 14, "bold"), bg=theme["card"], fg=theme["red"]).pack(anchor="w", padx=18, pady=(18, 8))
    tk.Label(danger, text="This removes Calendar, Academics, Habits, and Finance records.", bg=theme["card"], fg=theme["muted"]).pack(anchor="w", padx=18, pady=(0, 10))

    def reset_data():
        answer = messagebox.askyesno("Reset tracker", "Delete all tracker records?")
        if answer:
            database.reset_all_data()
            messagebox.showinfo("Reset complete", "Tracker data has been cleared.")
            refresh_page()

    styled_button(danger, "Reset All Data", reset_data, theme, theme["red"], width=16).pack(anchor="w", padx=18, pady=(0, 18))
