# R_FILE_UI
import calendar
import tkinter as tk
from datetime import date
from tkinter import messagebox

from app import analytics
from app import database
from app import date_helpers


DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
shown_year = date.today().year
shown_month = date.today().month

LIGHT = {
    "name": "Light",
    "bg": "#F5F7FB",
    "sidebar": "#172033",
    "sidebar_text": "#F8FAFC",
    "sidebar_muted": "#A7B0C0",
    "card": "#FFFFFF",
    "text": "#1D2433",
    "muted": "#667085",
    "border": "#E2E8F0",
    "accent": "#6C63FF",
    "accent_2": "#FF7A59",
    "green": "#25A97A",
    "blue": "#3B82F6",
    "yellow": "#E0A514",
    "red": "#E05260",
    "input": "#F8FAFC",
}

DARK = {
    "name": "Dark",
    "bg": "#10131A",
    "sidebar": "#171B24",
    "sidebar_text": "#F8FAFC",
    "sidebar_muted": "#98A2B3",
    "card": "#1C212C",
    "text": "#F4F6FA",
    "muted": "#A6ADBB",
    "border": "#2C3442",
    "accent": "#8B83FF",
    "accent_2": "#FF8B6A",
    "green": "#40C693",
    "blue": "#63A4FF",
    "yellow": "#F2C14E",
    "red": "#FF6B78",
    "input": "#242A36",
}


def get_theme(name):
    if name == "Dark":
        return DARK
    return LIGHT


def make_page_title(parent, title, subtitle, theme):
    tk.Label(
        parent,
        text=title,
        font=("Segoe UI", 24, "bold"),
        bg=theme["bg"],
        fg=theme["text"],
    ).pack(anchor="w", padx=24, pady=(20, 2))
    tk.Label(
        parent,
        text=subtitle,
        font=("Segoe UI", 10),
        bg=theme["bg"],
        fg=theme["muted"],
    ).pack(anchor="w", padx=24, pady=(0, 16))


def make_metric_card(parent, title, value, color, theme, width=180, height=95):
    frame = tk.Frame(
        parent,
        width=width,
        height=height,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1,
    )
    frame.pack_propagate(False)
    tk.Frame(frame, width=6, bg=color).pack(side="left", fill="y")
    inside = tk.Frame(frame, bg=theme["card"])
    inside.pack(side="left", fill="both", expand=True, padx=12, pady=12)
    tk.Label(
        inside,
        text=title,
        font=("Segoe UI", 9),
        bg=theme["card"],
        fg=theme["muted"],
    ).pack(anchor="w")
    tk.Label(
        inside,
        text=str(value),
        font=("Segoe UI", 20, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", pady=(3, 0))
    return frame


def styled_button(parent, text, command, theme, color=None, width=14):
    if color is None:
        color = theme["accent"]
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        relief="flat",
        bd=0,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        font=("Segoe UI", 9, "bold"),
        cursor="hand2",
        padx=8,
        pady=7,
    )


def styled_entry(parent, theme, width=20):
    return tk.Entry(
        parent,
        width=width,
        font=("Segoe UI", 10),
        bg=theme["input"],
        fg=theme["text"],
        insertbackground=theme["text"],
        relief="solid",
        bd=1,
        highlightthickness=0,
    )


def _card_frame(parent, theme, row, col, padx=(0, 0), pady=6, colspan=1):
    frame = tk.Frame(
        parent,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1,
    )
    frame.grid(
        row=row,
        column=col,
        columnspan=colspan,
        padx=padx,
        pady=pady,
        sticky="nsew",
    )
    return frame


def _new_canvas(parent, theme, title, height=220):
    canvas = tk.Canvas(
        parent,
        height=height,
        bg=theme["card"],
        highlightthickness=0,
    )
    canvas.pack(fill="both", expand=True, padx=10, pady=10)
    canvas.create_text(
        12,
        12,
        anchor="nw",
        text=title,
        fill=theme["text"],
        font=("Segoe UI", 11, "bold"),
    )
    return canvas


def draw_line_chart(parent, labels, values, title, theme, line_color=None):
    if line_color is None:
        line_color = theme["accent"]
    canvas = _new_canvas(parent, theme, title)
    if not values:
        return canvas

    width = 520
    height = 160
    left = 45
    top = 40
    canvas.create_line(left, top, left, top + height, fill=theme["border"])
    canvas.create_line(
        left, top + height, left + width, top + height, fill=theme["border"]
    )

    max_val = max(values)
    if max_val <= 0:
        max_val = 1

    count = len(values)
    points = []
    for i in range(count):
        if count == 1:
            x = left + width / 2
        else:
            x = left + i * width / (count - 1)
        ratio = values[i] / max_val
        y = top + height - (ratio * (height - 15))
        points.append((x, y))

    for i, (x, y) in enumerate(points):
        canvas.create_text(
            x,
            top + height + 16,
            text=labels[i],
            fill=theme["muted"],
            font=("Segoe UI", 8),
        )
        canvas.create_oval(
            x - 4,
            y - 4,
            x + 4,
            y + 4,
            fill=line_color,
            outline=line_color,
        )
        if i < len(points) - 1:
            nx, ny = points[i + 1]
            canvas.create_line(
                x, y, nx, ny, fill=line_color, width=3, smooth=True
            )
    return canvas


def draw_bar_chart(parent, labels, values, title, theme, colors=None):
    canvas = _new_canvas(parent, theme, title)
    if not values:
        return canvas

    if colors is None:
        colors = [
            theme["accent"],
            theme["blue"],
            theme["green"],
            theme["accent_2"],
        ]

    left = 45
    top = 45
    chart_h = 145
    chart_w = 520
    max_val = max(values)
    if max_val <= 0:
        max_val = 1

    space = chart_w / len(values)
    bar_w = space * 0.55

    for i, val in enumerate(values):
        x1 = left + i * space + (space - bar_w) / 2
        x2 = x1 + bar_w
        bh = (val / max_val) * chart_h
        y1 = top + chart_h - bh
        y2 = top + chart_h
        color = colors[i % len(colors)]
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        canvas.create_text(
            (x1 + x2) / 2,
            y1 - 10,
            text=str(val),
            fill=theme["text"],
            font=("Segoe UI", 8),
        )
        canvas.create_text(
            (x1 + x2) / 2,
            y2 + 16,
            text=labels[i],
            fill=theme["muted"],
            font=("Segoe UI", 8),
        )
    return canvas


def draw_donut_chart(parent, labels, values, title, theme, colors=None):
    canvas = _new_canvas(parent, theme, title)
    if colors is None:
        colors = [
            theme["accent"],
            theme["green"],
            theme["blue"],
            theme["accent_2"],
        ]

    total = sum(values)
    if total <= 0:
        canvas.create_text(
            140,
            120,
            text="No data yet",
            fill=theme["muted"],
            font=("Segoe UI", 10),
        )
        return canvas

    angle_start = 0
    for i, val in enumerate(values):
        extent = (val / total) * 360
        color = colors[i % len(colors)]
        canvas.create_arc(
            40,
            50,
            180,
            190,
            start=angle_start,
            extent=extent,
            fill=color,
            outline=theme["card"],
        )
        angle_start += extent

    canvas.create_oval(
        75, 85, 145, 155, fill=theme["card"], outline=theme["card"]
    )

    legend_y = 65
    for i, label in enumerate(labels):
        color = colors[i % len(colors)]
        canvas.create_rectangle(
            230, legend_y, 242, legend_y + 12, fill=color, outline=""
        )
        text = f"{label}: {round(values[i], 1)}"
        canvas.create_text(
            250,
            legend_y + 6,
            anchor="w",
            text=text,
            fill=theme["text"],
            font=("Segoe UI", 9),
        )
        legend_y += 28
    return canvas


def draw_horizontal_bars(parent, labels, values, title, theme):
    canvas = _new_canvas(parent, theme, title, height=240)
    if not values:
        canvas.create_text(
            20,
            60,
            anchor="w",
            text="No habit category data yet",
            fill=theme["muted"],
        )
        return canvas

    colors = [
        theme["accent"],
        theme["blue"],
        theme["green"],
        theme["accent_2"],
        theme["yellow"],
    ]
    y = 55
    for i, val in enumerate(values):
        color = colors[i % len(colors)]
        canvas.create_text(15, y + 10, anchor="w", text=labels[i], fill=theme["text"])
        canvas.create_rectangle(
            130, y, 130 + val * 3.6, y + 22, fill=color, outline=""
        )
        canvas.create_text(
            500, y + 11, anchor="e", text=f"{val}%", fill=theme["muted"]
        )
        y += 35
    return canvas


def _add_labeled_entry(parent, label, theme, default=""):
    tk.Label(parent, text=label, bg=theme["card"], fg=theme["text"]).pack(
        anchor="w", padx=15
    )
    entry = styled_entry(parent, theme, width=28)
    entry.pack(fill="x", padx=15, pady=(3, 8))
    if default:
        entry.insert(0, default)
    return entry


def _add_option_menu(parent, label, variable, options, theme):
    tk.Label(parent, text=label, bg=theme["card"], fg=theme["text"]).pack(
        anchor="w", padx=15
    )
    menu = tk.OptionMenu(parent, variable, *options)
    menu.config(
        bg=theme["input"],
        fg=theme["text"],
        relief="flat",
        highlightthickness=0,
    )
    menu.pack(fill="x", padx=15, pady=(3, 8))


def show_dashboard(parent, theme, refresh_page=None):
    make_page_title(
        parent,
        "Dashboard",
        "A quick view of your progress across the four tracker areas.",
        theme,
    )
    today = date.today()
    h_score = analytics.habit_completion_for_day(today)
    a_score = analytics.academic_score_for_day(today)
    c_score = analytics.calendar_score_for_day(today)
    f_score = analytics.finance_score_for_month(today)
    o_score = analytics.overall_score_for_day(today)

    cards = tk.Frame(parent, bg=theme["bg"])
    cards.pack(fill="x", padx=24, pady=(0, 16))
    items = [
        ("Overall", f"{o_score}%", theme["accent"]),
        ("Habits Today", f"{h_score}%", theme["green"]),
        ("Academics Today", f"{a_score}%", theme["blue"]),
        ("Finance", f"{f_score}%", theme["yellow"]),
        ("Calendar Today", f"{c_score}%", theme["accent_2"]),
        ("Total XP", analytics.get_total_xp(), theme["red"]),
    ]
    for i, (title, val, col) in enumerate(items):
        card = make_metric_card(
            cards, title, val, col, theme, width=165, height=90
        )
        card.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="nsew")
        cards.grid_columnconfigure(i % 3, weight=1)

    charts = tk.Frame(parent, bg=theme["bg"])
    charts.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    charts.grid_columnconfigure(0, weight=1)
    charts.grid_columnconfigure(1, weight=1)

    left = _card_frame(charts, theme, 0, 0, padx=(0, 7))
    right = _card_frame(charts, theme, 0, 1, padx=(7, 0))
    bottom = _card_frame(charts, theme, 1, 0, pady=(8, 0), colspan=2)

    labels, vals = analytics.weekly_overall_values()
    draw_line_chart(
        left, labels, vals, "7 Day Overall Progress", theme, theme["accent"]
    )
    draw_donut_chart(
        right,
        ["Habits", "Academics", "Finance", "Calendar"],
        [h_score, a_score, f_score, c_score],
        "Today's Balance",
        theme,
    )
    s_labels, s_vals = analytics.weekly_study_hours()
    draw_bar_chart(bottom, s_labels, s_vals, "Study Hours This Week", theme)


def _group_events_by_day(events):
    by_day = {}
    for ev in events:
        day_num = int(ev["event_date"].split("-")[2])
        by_day.setdefault(day_num, []).append(ev)
    return by_day


def _draw_month_grid(cal_card, year, month, by_day, theme):
    for col, day_name in enumerate(DAY_NAMES):
        tk.Label(
            cal_card,
            text=day_name,
            font=("Segoe UI", 9, "bold"),
            bg=theme["card"],
            fg=theme["muted"],
        ).grid(row=0, column=col, padx=2, pady=7, sticky="nsew")
        cal_card.grid_columnconfigure(col, weight=1)

    for r_idx, week in enumerate(calendar.monthcalendar(year, month)):
        cal_card.grid_rowconfigure(r_idx + 1, weight=1)
        for c_idx, d_num in enumerate(week):
            cell = tk.Frame(
                cal_card,
                bg=theme["input"],
                highlightbackground=theme["border"],
                highlightthickness=1,
                width=100,
                height=85,
            )
            cell.grid(
                row=r_idx + 1, column=c_idx, padx=2, pady=2, sticky="nsew"
            )
            cell.grid_propagate(False)
            if d_num:
                tk.Label(
                    cell,
                    text=str(d_num),
                    font=("Segoe UI", 9, "bold"),
                    bg=theme["input"],
                    fg=theme["text"],
                ).pack(anchor="nw", padx=5, pady=(4, 2))
                day_evs = by_day.get(d_num, [])
                for ev in day_evs[:2]:
                    title = ev["title"]
                    if len(title) > 15:
                        title = title[:13] + ".."
                    if ev["completed"] == 1:
                        col = theme["green"]
                    else:
                        col = theme["accent"]
                    tk.Label(
                        cell,
                        text=f"• {title}",
                        font=("Segoe UI", 8),
                        bg=theme["input"],
                        fg=col,
                    ).pack(anchor="w", padx=5)
                if len(day_evs) > 2:
                    tk.Label(
                        cell,
                        text=f"+{len(day_evs) - 2} more",
                        font=("Segoe UI", 7),
                        bg=theme["input"],
                        fg=theme["muted"],
                    ).pack(anchor="w", padx=5)


def show_calendar(parent, theme, refresh_page):
    global shown_year, shown_month
    make_page_title(
        parent,
        "Calendar",
        "Plan events and see event names directly inside the month view.",
        theme,
    )

    top = tk.Frame(parent, bg=theme["bg"])
    top.pack(fill="x", padx=24, pady=(0, 10))

    def move_month(delta):
        global shown_year, shown_month
        shown_month += delta
        if shown_month < 1:
            shown_month = 12
            shown_year -= 1
        elif shown_month > 12:
            shown_month = 1
            shown_year += 1
        refresh_page()

    styled_button(
        top, "Previous", lambda: move_month(-1), theme, width=10
    ).pack(side="left")
    tk.Label(
        top,
        text=f"{calendar.month_name[shown_month]} {shown_year}",
        font=("Segoe UI", 16, "bold"),
        bg=theme["bg"],
        fg=theme["text"],
    ).pack(side="left", expand=True)
    styled_button(top, "Next", lambda: move_month(1), theme, width=10).pack(
        side="right"
    )

    body = tk.Frame(parent, bg=theme["bg"])
    body.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    body.grid_columnconfigure(0, weight=3)
    body.grid_columnconfigure(1, weight=2)
    body.grid_rowconfigure(0, weight=1)

    cal_card = _card_frame(body, theme, 0, 0, padx=(0, 8), pady=0)
    side_card = _card_frame(body, theme, 0, 1, padx=(8, 0), pady=0)

    events = database.get_events_for_month(shown_year, shown_month)
    _draw_month_grid(
        cal_card, shown_year, shown_month, _group_events_by_day(events), theme
    )

    tk.Label(
        side_card,
        text="Add Event",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))
    date_entry = _add_labeled_entry(
        side_card, "Date (DD/MM/YYYY)", theme, date_helpers.today_display()
    )
    title_entry = _add_labeled_entry(side_card, "Event name", theme)
    notes_entry = _add_labeled_entry(side_card, "Notes", theme)

    def save_event():
        title = title_entry.get().strip()
        if not title:
            messagebox.showerror("Missing name", "Please enter an event name.")
            return
        try:
            ev_date = date_helpers.to_storage_date(date_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid date", "Use a real date in DD/MM/YYYY format."
            )
            return
        database.add_event(ev_date, title, notes_entry.get().strip())
        messagebox.showinfo("Saved", "Event added successfully.")
        refresh_page()

    styled_button(side_card, "Add Event", save_event, theme).pack(
        anchor="w", padx=15, pady=(2, 18)
    )
    tk.Label(
        side_card,
        text="Events This Month",
        font=("Segoe UI", 12, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(5, 8))

    ev_list = tk.Frame(side_card, bg=theme["card"])
    ev_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    if not events:
        tk.Label(
            ev_list,
            text="No events for this month yet.",
            bg=theme["card"],
            fg=theme["muted"],
        ).pack(anchor="w")
        return

    for ev in events[-8:]:
        row = tk.Frame(ev_list, bg=theme["card"])
        row.pack(fill="x", pady=2)
        if ev["completed"] == 1:
            status = "✓ "
            btn_txt = "Undo"
        else:
            status = "• "
            btn_txt = "Done"
        d_str = date_helpers.to_display_date(ev["event_date"])
        tk.Label(
            row,
            text=f"{status}{d_str}  {ev['title']}",
            bg=theme["card"],
            fg=theme["text"],
            font=("Segoe UI", 8),
        ).pack(side="left")
        eid = ev["id"]

        def toggle_ev(event_id=eid):
            database.toggle_event_completed(event_id)
            refresh_page()

        styled_button(
            row, btn_txt, toggle_ev, theme, theme["green"], width=6
        ).pack(side="right", padx=3)


def show_academics(parent, theme, refresh_page):
    make_page_title(
        parent,
        "Academics",
        "Log study time and assignments. Today changes automatically with the real date.",
        theme,
    )
    today_iso = date.today().isoformat()
    entries_today = database.get_academic_entries_between(today_iso, today_iso)

    study = sum(e["study_hours"] for e in entries_today)
    target = sum(e["target_hours"] for e in entries_today)
    done = sum(e["assignments_done"] for e in entries_today)
    total = sum(e["assignments_total"] for e in entries_today)

    metrics = tk.Frame(parent, bg=theme["bg"])
    metrics.pack(fill="x", padx=24, pady=(0, 12))
    summary = [
        ("Study Today", f"{round(study, 1)} h", theme["blue"]),
        ("Target Today", f"{round(target, 1)} h", theme["accent"]),
        ("Assignments", f"{done}/{total}", theme["green"]),
    ]
    for i, (t, v, c) in enumerate(summary):
        card = make_metric_card(
            metrics, t, v, c, theme, width=210, height=90
        )
        card.grid(row=0, column=i, padx=6, sticky="nsew")
        metrics.grid_columnconfigure(i, weight=1)

    body = tk.Frame(parent, bg=theme["bg"])
    body.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    body.grid_columnconfigure(0, weight=2)
    body.grid_columnconfigure(1, weight=3)
    body.grid_rowconfigure(0, weight=1)

    form = _card_frame(body, theme, 0, 0, padx=(0, 8), pady=0)
    history = _card_frame(body, theme, 0, 1, padx=(8, 0), pady=0)

    tk.Label(
        form,
        text="Add Academic Entry",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))

    labels = [
        "Date (DD/MM/YYYY)",
        "Subject",
        "Study Hours",
        "Target Hours",
        "Assignments Done",
        "Assignments Total",
        "Notes",
    ]
    fields = []
    for name in labels:
        default = date_helpers.today_display() if name.startswith("Date") else ""
        fields.append(_add_labeled_entry(form, name, theme, default))

    def save():
        try:
            d_iso = date_helpers.to_storage_date(fields[0].get().strip())
            subj = fields[1].get().strip()
            sh = float(fields[2].get() or 0)
            th = float(fields[3].get() or 0)
            ad = int(fields[4].get() or 0)
            at = int(fields[5].get() or 0)
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Check the date and number fields."
            )
            return
        if not subj:
            messagebox.showerror("Missing subject", "Please enter a subject.")
            return
        database.add_academic_entry(
            d_iso, subj, sh, th, ad, at, fields[6].get().strip()
        )
        refresh_page()

    styled_button(form, "Save Entry", save, theme).pack(
        anchor="w", padx=15, pady=(3, 15)
    )
    tk.Label(
        history,
        text="Recent Academic History",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))

    recent = database.get_academic_entries(12)
    if not recent:
        tk.Label(
            history,
            text="No academic entries yet.",
            bg=theme["card"],
            fg=theme["muted"],
        ).pack(anchor="w", padx=15)
        return

    for e in recent:
        d_str = date_helpers.to_display_date(e["entry_date"])
        line = (
            f"{d_str}  |  {e['subject']}  |  "
            f"{e['study_hours']}h / {e['target_hours']}h  |  "
            f"Assignments {e['assignments_done']}/{e['assignments_total']}"
        )
        tk.Label(
            history,
            text=line,
            bg=theme["card"],
            fg=theme["text"],
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x", padx=15, pady=4)


def show_habits(parent, theme, refresh_page):
    make_page_title(
        parent,
        "Habits",
        "Create scheduled habits, complete today's habits, and earn XP.",
        theme,
    )
    today = date.today()
    today_iso = today.isoformat()
    scheduled = analytics.get_scheduled_habits(today)
    done_count = sum(
        1 for h in scheduled if database.habit_is_completed(h["id"], today_iso)
    )

    metrics = tk.Frame(parent, bg=theme["bg"])
    metrics.pack(fill="x", padx=24, pady=(0, 12))
    summary = [
        ("Today's Habits", f"{done_count}/{len(scheduled)}", theme["green"]),
        (
            "Completion",
            f"{analytics.habit_completion_for_day(today)}%",
            theme["accent"],
        ),
        ("Total XP", analytics.get_total_xp(), theme["yellow"]),
    ]
    for i, (t, v, c) in enumerate(summary):
        card = make_metric_card(
            metrics, t, v, c, theme, width=210, height=90
        )
        card.grid(row=0, column=i, padx=6, sticky="nsew")
        metrics.grid_columnconfigure(i, weight=1)

    body = tk.Frame(parent, bg=theme["bg"])
    body.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    body.grid_columnconfigure(0, weight=2)
    body.grid_columnconfigure(1, weight=3)
    body.grid_rowconfigure(0, weight=1)

    form = _card_frame(body, theme, 0, 0, padx=(0, 8), pady=0)
    today_card = _card_frame(body, theme, 0, 1, padx=(8, 0), pady=0)

    tk.Label(
        form,
        text="Create Habit",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))
    name_entry = _add_labeled_entry(form, "Habit name", theme)

    cat_var = tk.StringVar(value="Personal")
    xp_var = tk.StringVar(value="10")
    freq_var = tk.StringVar(value="Daily")
    _add_option_menu(
        form,
        "Category",
        cat_var,
        ["Personal", "Health", "Fitness", "Academics", "Other"],
        theme,
    )
    _add_option_menu(
        form, "XP Reward", xp_var, ["5", "10", "15", "20"], theme
    )
    _add_option_menu(
        form, "Frequency", freq_var, ["Daily", "Selected Days"], theme
    )

    tk.Label(
        form,
        text="Days (used for Selected Days)",
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(4, 4))
    days_frame = tk.Frame(form, bg=theme["card"])
    days_frame.pack(fill="x", padx=15, pady=(0, 10))
    day_vars = []
    for d_name in DAY_NAMES:
        v = tk.IntVar(value=0)
        tk.Checkbutton(
            days_frame,
            text=d_name,
            variable=v,
            bg=theme["card"],
            fg=theme["text"],
            selectcolor=theme["input"],
            activebackground=theme["card"],
            activeforeground=theme["text"],
        ).pack(side="left")
        day_vars.append(v)

    def create():
        name = name_entry.get().strip()
        freq = freq_var.get()
        picked = [
            DAY_NAMES[i] for i, v in enumerate(day_vars) if v.get() == 1
        ]
        if not name:
            messagebox.showerror("Missing name", "Please enter a habit name.")
            return
        if freq == "Selected Days" and not picked:
            messagebox.showerror("Missing days", "Select at least one day.")
            return
        database.add_habit(
            name, cat_var.get(), int(xp_var.get()), freq, ",".join(picked)
        )
        refresh_page()

    styled_button(form, "Create Habit", create, theme).pack(
        anchor="w", padx=15, pady=(2, 15)
    )
    tk.Label(
        today_card,
        text="Today's Habits",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))

    if not scheduled:
        tk.Label(
            today_card,
            text="No habits are scheduled for today.",
            bg=theme["card"],
            fg=theme["muted"],
        ).pack(anchor="w", padx=15)
        return

    for h in scheduled:
        row = tk.Frame(today_card, bg=theme["input"])
        row.pack(fill="x", padx=15, pady=4)
        done = database.habit_is_completed(h["id"], today_iso)
        icon = "✓" if done else "○"
        tk.Label(
            row,
            text=f"{icon}  {h['name']}",
            font=("Segoe UI", 10, "bold"),
            bg=theme["input"],
            fg=theme["text"],
        ).pack(side="left", padx=10, pady=10)
        tk.Label(
            row,
            text=f"{h['category']}  •  {h['xp_reward']} XP",
            bg=theme["input"],
            fg=theme["muted"],
        ).pack(side="left", padx=8)

        hid = h["id"]
        hxp = h["xp_reward"]

        def toggle_h(habit_id=hid, xp=hxp):
            database.toggle_habit_completion(habit_id, today_iso, xp)
            refresh_page()

        btn_txt = "Undo" if done else "Complete"
        btn_col = theme["muted"] if done else theme["green"]
        styled_button(row, btn_txt, toggle_h, theme, btn_col, width=9).pack(
            side="right", padx=8, pady=6
        )


def show_finance(parent, theme, refresh_page):
    make_page_title(
        parent,
        "Finance",
        "Track expenses, income, savings, and your monthly budget.",
        theme,
    )
    income, expenses, savings = analytics.money_totals_for_month()
    try:
        budget = float(database.get_setting("monthly_budget", "0"))
    except ValueError:
        budget = 0.0

    metrics = tk.Frame(parent, bg=theme["bg"])
    metrics.pack(fill="x", padx=24, pady=(0, 12))
    summary = [
        ("Income", f"₹{round(income, 2)}", theme["green"]),
        ("Expenses", f"₹{round(expenses, 2)}", theme["red"]),
        ("Savings", f"₹{round(savings, 2)}", theme["blue"]),
        ("Budget Left", f"₹{round(budget - expenses, 2)}", theme["yellow"]),
    ]
    for i, (t, v, c) in enumerate(summary):
        card = make_metric_card(
            metrics, t, v, c, theme, width=175, height=90
        )
        card.grid(row=0, column=i, padx=5, sticky="nsew")
        metrics.grid_columnconfigure(i, weight=1)

    body = tk.Frame(parent, bg=theme["bg"])
    body.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    body.grid_columnconfigure(0, weight=2)
    body.grid_columnconfigure(1, weight=3)
    body.grid_rowconfigure(0, weight=1)

    form = _card_frame(body, theme, 0, 0, padx=(0, 8), pady=0)
    history = _card_frame(body, theme, 0, 1, padx=(8, 0), pady=0)

    tk.Label(
        form,
        text="Add Finance Entry",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))
    date_entry = _add_labeled_entry(
        form, "Date (DD/MM/YYYY)", theme, date_helpers.today_display()
    )

    type_var = tk.StringVar(value="Expense")
    _add_option_menu(
        form, "Type", type_var, ["Expense", "Income", "Saving"], theme
    )

    category_entry = _add_labeled_entry(form, "Category", theme)
    amount_entry = _add_labeled_entry(form, "Amount", theme)
    notes_entry = _add_labeled_entry(form, "Notes", theme)

    def save():
        try:
            d_iso = date_helpers.to_storage_date(date_entry.get().strip())
            amt = float(amount_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Check the date and amount."
            )
            return
        cat = category_entry.get().strip()
        if not cat:
            messagebox.showerror(
                "Missing category", "Please enter a category."
            )
            return
        database.add_finance_entry(
            d_iso, type_var.get(), cat, amt, notes_entry.get().strip()
        )
        refresh_page()

    styled_button(form, "Save Entry", save, theme).pack(
        anchor="w", padx=15, pady=(5, 15)
    )
    tk.Label(
        history,
        text="Recent Finance History",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=15, pady=(15, 10))

    recent = database.get_finance_entries(14)
    if not recent:
        tk.Label(
            history,
            text="No finance entries yet.",
            bg=theme["card"],
            fg=theme["muted"],
        ).pack(anchor="w", padx=15)
        return

    for e in recent:
        if e["entry_type"] == "Income":
            col = theme["green"]
        elif e["entry_type"] == "Saving":
            col = theme["blue"]
        else:
            col = theme["red"]
        d_str = date_helpers.to_display_date(e["entry_date"])
        amt_str = f"₹{round(e['amount'], 2)}"
        line = f"{d_str}  |  {e['entry_type']}  |  {e['category']}  |  {amt_str}"
        tk.Label(
            history,
            text=line,
            bg=theme["card"],
            fg=col,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=15, pady=4)


def show_statistics(parent, theme, refresh_page=None):
    make_page_title(
        parent,
        "Statistics",
        "Visual summaries of habits, academics, finance, and calendar consistency.",
        theme,
    )
    grid = tk.Frame(parent, bg=theme["bg"])
    grid.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    grid.grid_columnconfigure(0, weight=1)
    grid.grid_columnconfigure(1, weight=1)

    boxes = []
    for r in range(3):
        for c in range(2):
            boxes.append(_card_frame(grid, theme, r, c, padx=6))

    h_lbl, h_val = analytics.weekly_habit_values()
    draw_line_chart(
        boxes[0], h_lbl, h_val, "Habit Completion Trend", theme, theme["green"]
    )

    s_lbl, s_val = analytics.weekly_study_hours()
    draw_line_chart(
        boxes[1], s_lbl, s_val, "Daily Study Hours", theme, theme["blue"]
    )

    inc, exp, sav = analytics.money_totals_for_month()
    draw_donut_chart(
        boxes[2],
        ["Income", "Expenses", "Savings"],
        [inc, exp, sav],
        "Money Flow This Month",
        theme,
        [theme["green"], theme["red"], theme["blue"]],
    )

    days = analytics.get_last_n_days(7)
    cal_lbl = [d.strftime("%a") for d in days]
    cal_val = [analytics.calendar_score_for_day(d) for d in days]
    draw_bar_chart(
        boxes[3], cal_lbl, cal_val, "Calendar Consistency", theme
    )

    cats = analytics.habit_category_percentages(30)
    draw_horizontal_bars(
        boxes[4],
        list(cats.keys()),
        list(cats.values()),
        "Habit Consistency by Category",
        theme,
    )

    today = date.today()
    bal_vals = [
        analytics.habit_completion_for_day(today),
        analytics.academic_score_for_day(today),
        analytics.finance_score_for_month(today),
        analytics.calendar_score_for_day(today),
    ]
    draw_donut_chart(
        boxes[5],
        ["Habits", "Academics", "Finance", "Calendar"],
        bal_vals,
        "Current Domain Balance",
        theme,
    )


def _settings_box(parent, theme):
    box = tk.Frame(
        parent,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1,
    )
    box.pack(fill="x", padx=24, pady=(0, 18))
    return box


def show_settings(parent, theme, refresh_page, change_theme):
    make_page_title(
        parent,
        "Settings",
        "Change your profile, monthly budget, appearance, or reset tracker data.",
        theme,
    )

    prof = _settings_box(parent, theme)
    tk.Label(
        prof,
        text="Profile",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=18, pady=(18, 10))
    name_entry = _add_labeled_entry(
        prof, "Display name", theme, database.get_setting("display_name", "")
    )
    budget_entry = _add_labeled_entry(
        prof,
        "Monthly budget",
        theme,
        database.get_setting("monthly_budget", "0"),
    )

    def save_prof():
        name = name_entry.get().strip()
        budget = budget_entry.get().strip()
        if not name:
            messagebox.showerror(
                "Missing name", "Display name cannot be empty."
            )
            return
        try:
            float(budget)
        except ValueError:
            messagebox.showerror(
                "Invalid budget", "Budget must be a number."
            )
            return
        database.save_setting("display_name", name)
        database.save_setting("monthly_budget", budget)
        messagebox.showinfo("Saved", "Settings saved.")

    styled_button(prof, "Save Profile", save_prof, theme).pack(
        anchor="w", padx=18, pady=(0, 18)
    )

    app_card = _settings_box(parent, theme)
    tk.Label(
        app_card,
        text="Appearance",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["text"],
    ).pack(anchor="w", padx=18, pady=(18, 10))
    theme_var = tk.StringVar(value=database.get_setting("theme", "Light"))
    _add_option_menu(app_card, "Theme", theme_var, ["Light", "Dark"], theme)
    styled_button(
        app_card,
        "Apply Theme",
        lambda: change_theme(theme_var.get()),
        theme,
    ).pack(anchor="w", padx=18, pady=(0, 18))

    danger = _settings_box(parent, theme)
    tk.Label(
        danger,
        text="Reset Tracker Data",
        font=("Segoe UI", 14, "bold"),
        bg=theme["card"],
        fg=theme["red"],
    ).pack(anchor="w", padx=18, pady=(18, 8))
    tk.Label(
        danger,
        text="This removes Calendar, Academics, Habits, and Finance records.",
        bg=theme["card"],
        fg=theme["muted"],
    ).pack(anchor="w", padx=18, pady=(0, 10))

    def reset():
        if messagebox.askyesno("Reset tracker", "Delete all tracker records?"):
            database.reset_all_data()
            messagebox.showinfo(
                "Reset complete", "Tracker data has been cleared."
            )
            refresh_page()

    styled_button(
        danger, "Reset All Data", reset, theme, theme["red"], width=16
    ).pack(anchor="w", padx=18, pady=(0, 18))


dashboard = type("Page", (), {"show": staticmethod(show_dashboard)})
calendar_page = type("Page", (), {"show": staticmethod(show_calendar)})
academics = type("Page", (), {"show": staticmethod(show_academics)})
habits = type("Page", (), {"show": staticmethod(show_habits)})
finance = type("Page", (), {"show": staticmethod(show_finance)})
statistics = type("Page", (), {"show": staticmethod(show_statistics)})
settings = type("Page", (), {"show": staticmethod(show_settings)})
