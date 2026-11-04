import tkinter as tk
import calendar
from datetime import date
from tkinter import messagebox

import database
import date_helpers
from ui_helpers import make_page_title, styled_button, styled_entry


shown_year = date.today().year
shown_month = date.today().month


def show(parent, theme, refresh_page):
    global shown_year, shown_month

    make_page_title(
        parent,
        "Calendar",
        "Plan events and see event names directly inside the month view.",
        theme
    )

    top = tk.Frame(parent, bg=theme["bg"])
    top.pack(fill="x", padx=24, pady=(0, 10))

    def previous_month():
        global shown_year, shown_month
        shown_month = shown_month - 1
        if shown_month == 0:
            shown_month = 12
            shown_year = shown_year - 1
        refresh_page()

    def next_month():
        global shown_year, shown_month
        shown_month = shown_month + 1
        if shown_month == 13:
            shown_month = 1
            shown_year = shown_year + 1
        refresh_page()

    styled_button(top, "Previous", previous_month, theme, width=10).pack(side="left")

    month_name = calendar.month_name[shown_month] + " " + str(shown_year)
    tk.Label(
        top,
        text=month_name,
        font=("Segoe UI", 16, "bold"),
        bg=theme["bg"],
        fg=theme["text"]
    ).pack(side="left", expand=True)

    styled_button(top, "Next", next_month, theme, width=10).pack(side="right")

    main_area = tk.Frame(parent, bg=theme["bg"])
    main_area.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    main_area.grid_columnconfigure(0, weight=3)
    main_area.grid_columnconfigure(1, weight=2)
    main_area.grid_rowconfigure(0, weight=1)

    calendar_card = tk.Frame(
        main_area,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    calendar_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

    side_card = tk.Frame(
        main_area,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    side_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    events = database.get_events_for_month(shown_year, shown_month)
    events_by_day = {}

    for event in events:
        event_day = int(event["event_date"].split("-")[2])
        if event_day not in events_by_day:
            events_by_day[event_day] = []
        events_by_day[event_day].append(event)

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for column in range(7):
        tk.Label(
            calendar_card,
            text=weekdays[column],
            font=("Segoe UI", 9, "bold"),
            bg=theme["card"],
            fg=theme["muted"]
        ).grid(row=0, column=column, padx=2, pady=7, sticky="nsew")
        calendar_card.grid_columnconfigure(column, weight=1)

    month_rows = calendar.monthcalendar(shown_year, shown_month)

    for row_index in range(len(month_rows)):
        week = month_rows[row_index]
        calendar_card.grid_rowconfigure(row_index + 1, weight=1)

        for column_index in range(7):
            day_number = week[column_index]

            cell = tk.Frame(
                calendar_card,
                bg=theme["input"],
                highlightbackground=theme["border"],
                highlightthickness=1,
                width=100,
                height=85
            )
            cell.grid(row=row_index + 1, column=column_index, padx=2, pady=2, sticky="nsew")
            cell.grid_propagate(False)

            if day_number != 0:
                tk.Label(
                    cell,
                    text=str(day_number),
                    font=("Segoe UI", 9, "bold"),
                    bg=theme["input"],
                    fg=theme["text"]
                ).pack(anchor="nw", padx=5, pady=(4, 2))

                if day_number in events_by_day:
                    day_events = events_by_day[day_number]
                    max_to_show = 2

                    for event_index in range(min(len(day_events), max_to_show)):
                        event = day_events[event_index]
                        title = event["title"]
                        if len(title) > 15:
                            title = title[:13] + ".."

                        event_color = theme["accent"]
                        if event["completed"] == 1:
                            event_color = theme["green"]

                        tk.Label(
                            cell,
                            text="• " + title,
                            font=("Segoe UI", 8),
                            bg=theme["input"],
                            fg=event_color
                        ).pack(anchor="w", padx=5)

                    if len(day_events) > max_to_show:
                        remaining = len(day_events) - max_to_show
                        tk.Label(
                            cell,
                            text="+" + str(remaining) + " more",
                            font=("Segoe UI", 7),
                            bg=theme["input"],
                            fg=theme["muted"]
                        ).pack(anchor="w", padx=5)

    tk.Label(
        side_card,
        text="Add Event",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"]
    ).pack(anchor="w", padx=15, pady=(15, 10))

    tk.Label(side_card, text="Date (DD/MM/YYYY)", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    date_entry = styled_entry(side_card, theme, width=28)
    date_entry.pack(fill="x", padx=15, pady=(4, 10))
    date_entry.insert(0, date_helpers.today_display())

    tk.Label(side_card, text="Event name", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    title_entry = styled_entry(side_card, theme, width=28)
    title_entry.pack(fill="x", padx=15, pady=(4, 10))

    tk.Label(side_card, text="Notes", bg=theme["card"], fg=theme["text"]).pack(anchor="w", padx=15)
    notes_entry = styled_entry(side_card, theme, width=28)
    notes_entry.pack(fill="x", padx=15, pady=(4, 10))

    def save_event():
        display_date = date_entry.get().strip()
        title = title_entry.get().strip()
        notes = notes_entry.get().strip()

        if title == "":
            messagebox.showerror("Missing name", "Please enter an event name.")
            return

        try:
            event_date = date_helpers.to_storage_date(display_date)
        except ValueError:
            messagebox.showerror("Invalid date", "Use a real date in DD/MM/YYYY format.")
            return

        database.add_event(event_date, title, notes)
        messagebox.showinfo("Saved", "Event added successfully.")
        refresh_page()

    styled_button(side_card, "Add Event", save_event, theme).pack(anchor="w", padx=15, pady=(2, 18))

    tk.Label(
        side_card,
        text="Events This Month",
        font=("Segoe UI", 12, "bold"),
        bg=theme["card"],
        fg=theme["text"]
    ).pack(anchor="w", padx=15, pady=(5, 8))

    event_list = tk.Frame(side_card, bg=theme["card"])
    event_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    if len(events) == 0:
        tk.Label(
            event_list,
            text="No events for this month yet.",
            bg=theme["card"],
            fg=theme["muted"]
        ).pack(anchor="w")
    else:
        for event in events[-8:]:
            row = tk.Frame(event_list, bg=theme["card"])
            row.pack(fill="x", pady=2)

            status = "✓ " if event["completed"] == 1 else "• "
            tk.Label(
                row,
                text=status + date_helpers.to_display_date(event["event_date"]) + "  " + event["title"],
                bg=theme["card"],
                fg=theme["text"],
                font=("Segoe UI", 8)
            ).pack(side="left")

            event_id = event["id"]

            def toggle_this_event(event_id=event_id):
                database.toggle_event_completed(event_id)
                refresh_page()

            button_text = "Undo" if event["completed"] == 1 else "Done"
            styled_button(
                row,
                button_text,
                toggle_this_event,
                theme,
                theme["green"],
                width=6
            ).pack(side="right", padx=3)
