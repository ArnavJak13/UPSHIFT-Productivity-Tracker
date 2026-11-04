"""Pinnacle Tracker beginner version.

This file starts the program and controls which page is visible.
The project intentionally avoids an OOP app class so beginners can follow the
program using normal functions and global variables.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import date

import database
from theme import get_theme
from ui import dashboard
from ui import calendar_page
from ui import academics
from ui import habits
from ui import finance
from ui import statistics
from ui import settings


root = None
content_frame = None
sidebar = None
current_page = "Dashboard"
current_theme = None
last_day_seen = date.today()


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def show_welcome():
    """Show first-launch setup when no display name has been saved."""
    clear_window()

    theme = get_theme(database.get_setting("theme", "Light"))
    root.configure(bg=theme["bg"])

    wrapper = tk.Frame(root, bg=theme["bg"])
    wrapper.pack(fill="both", expand=True)

    card = tk.Frame(
        wrapper,
        width=520,
        height=430,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(
        card,
        text="Pinnacle Tracker",
        font=("Segoe UI", 26, "bold"),
        bg=theme["card"],
        fg=theme["accent"]
    ).pack(pady=(45, 6))

    tk.Label(
        card,
        text="Track Calendar, Academics, Habits and Finance in one place.",
        font=("Segoe UI", 10),
        bg=theme["card"],
        fg=theme["muted"]
    ).pack(pady=(0, 28))

    tk.Label(card, text="What should we call you?", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=70)
    name_entry = tk.Entry(card, font=("Segoe UI", 11), bg=theme["input"], fg=theme["text"], insertbackground=theme["text"], relief="solid", bd=1)
    name_entry.pack(fill="x", padx=70, pady=(5, 14), ipady=5)

    tk.Label(card, text="Monthly budget (₹)", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=70)
    budget_entry = tk.Entry(card, font=("Segoe UI", 11), bg=theme["input"], fg=theme["text"], insertbackground=theme["text"], relief="solid", bd=1)
    budget_entry.pack(fill="x", padx=70, pady=(5, 22), ipady=5)
    budget_entry.insert(0, "5000")

    def finish_setup():
        name = name_entry.get().strip()
        budget = budget_entry.get().strip()

        if name == "":
            messagebox.showerror("Missing name", "Please enter your name.")
            return

        try:
            float(budget)
        except ValueError:
            messagebox.showerror("Invalid budget", "Budget must be a number.")
            return

        database.save_setting("display_name", name)
        database.save_setting("monthly_budget", budget)
        database.save_setting("theme", "Light")
        build_main_layout()

    tk.Button(
        card,
        text="Get Started",
        command=finish_setup,
        bg=theme["accent"],
        fg="white",
        activebackground=theme["accent"],
        activeforeground="white",
        relief="flat",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=10,
        cursor="hand2"
    ).pack()


def build_main_layout():
    """Create the sidebar and the area where pages are shown."""
    global sidebar, content_frame, current_theme

    clear_window()
    current_theme = get_theme(database.get_setting("theme", "Light"))
    root.configure(bg=current_theme["bg"])

    sidebar = tk.Frame(root, width=205, bg=current_theme["sidebar"])
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content_frame = tk.Frame(root, bg=current_theme["bg"])
    content_frame.pack(side="left", fill="both", expand=True)

    tk.Label(
        sidebar,
        text="PINNACLE",
        font=("Segoe UI", 18, "bold"),
        bg=current_theme["sidebar"],
        fg=current_theme["sidebar_text"]
    ).pack(anchor="w", padx=20, pady=(28, 3))

    display_name = database.get_setting("display_name", "User")
    tk.Label(
        sidebar,
        text="Hi, " + display_name,
        font=("Segoe UI", 9),
        bg=current_theme["sidebar"],
        fg=current_theme["sidebar_muted"]
    ).pack(anchor="w", padx=20, pady=(0, 24))

    add_nav_button("Dashboard", show_dashboard)
    add_nav_button("Calendar", show_calendar)
    add_nav_button("Academics", show_academics)
    add_nav_button("Habits", show_habits)
    add_nav_button("Finance", show_finance)
    add_nav_button("Statistics", show_statistics)
    add_nav_button("Settings", show_settings)

    show_current_page()


def add_nav_button(text, command):
    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        anchor="w",
        relief="flat",
        bd=0,
        bg=current_theme["sidebar"],
        fg=current_theme["sidebar_text"],
        activebackground=current_theme["accent"],
        activeforeground="white",
        font=("Segoe UI", 10),
        padx=18,
        pady=11,
        cursor="hand2"
    )
    button.pack(fill="x", padx=10, pady=2)


def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def show_dashboard():
    global current_page
    current_page = "Dashboard"
    clear_content()
    dashboard.show(content_frame, current_theme, refresh_current_page)


def show_calendar():
    global current_page
    current_page = "Calendar"
    clear_content()
    calendar_page.show(content_frame, current_theme, refresh_current_page)


def show_academics():
    global current_page
    current_page = "Academics"
    clear_content()
    academics.show(content_frame, current_theme, refresh_current_page)


def show_habits():
    global current_page
    current_page = "Habits"
    clear_content()
    habits.show(content_frame, current_theme, refresh_current_page)


def show_finance():
    global current_page
    current_page = "Finance"
    clear_content()
    finance.show(content_frame, current_theme, refresh_current_page)


def show_statistics():
    global current_page
    current_page = "Statistics"
    clear_content()
    statistics.show(content_frame, current_theme, refresh_current_page)


def show_settings():
    global current_page
    current_page = "Settings"
    clear_content()
    settings.show(content_frame, current_theme, refresh_current_page, change_theme)


def show_current_page():
    if current_page == "Calendar":
        show_calendar()
    elif current_page == "Academics":
        show_academics()
    elif current_page == "Habits":
        show_habits()
    elif current_page == "Finance":
        show_finance()
    elif current_page == "Statistics":
        show_statistics()
    elif current_page == "Settings":
        show_settings()
    else:
        show_dashboard()


def refresh_current_page():
    show_current_page()


def change_theme(theme_name):
    database.save_setting("theme", theme_name)
    build_main_layout()


def check_for_new_day():
    """Refresh daily information if the app stays open past midnight."""
    global last_day_seen

    today = date.today()
    if today != last_day_seen:
        last_day_seen = today
        refresh_current_page()

    root.after(60000, check_for_new_day)


def start_app():
    global root

    database.init_db()

    root = tk.Tk()
    root.title("Pinnacle Tracker")
    root.geometry("1240x820")
    root.minsize(1050, 700)

    display_name = database.get_setting("display_name", "")
    if display_name == "":
        show_welcome()
    else:
        build_main_layout()

    root.after(60000, check_for_new_day)
    root.mainloop()


if __name__ == "__main__":
    start_app()
