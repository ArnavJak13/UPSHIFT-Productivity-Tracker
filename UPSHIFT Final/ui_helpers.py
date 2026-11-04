"""Small reusable Tkinter helper functions.

The goal is to keep visual drawing code away from the main feature files.
Students can understand the tracker logic without first understanding every
pixel calculation used by the charts.
"""

import tkinter as tk


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def make_page_title(parent, title, subtitle, theme):
    title_label = tk.Label(
        parent,
        text=title,
        font=("Segoe UI", 24, "bold"),
        bg=theme["bg"],
        fg=theme["text"]
    )
    title_label.pack(anchor="w", padx=24, pady=(20, 2))

    subtitle_label = tk.Label(
        parent,
        text=subtitle,
        font=("Segoe UI", 10),
        bg=theme["bg"],
        fg=theme["muted"]
    )
    subtitle_label.pack(anchor="w", padx=24, pady=(0, 16))


def make_card(parent, theme, padding=14):
    frame = tk.Frame(
        parent,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    frame.pack_propagate(False)
    return frame


def make_metric_card(parent, title, value, color, theme, width=180, height=95):
    frame = tk.Frame(
        parent,
        width=width,
        height=height,
        bg=theme["card"],
        highlightbackground=theme["border"],
        highlightthickness=1
    )
    frame.pack_propagate(False)

    strip = tk.Frame(frame, width=6, bg=color)
    strip.pack(side="left", fill="y")

    inside = tk.Frame(frame, bg=theme["card"])
    inside.pack(side="left", fill="both", expand=True, padx=12, pady=12)

    tk.Label(
        inside,
        text=title,
        font=("Segoe UI", 9),
        bg=theme["card"],
        fg=theme["muted"]
    ).pack(anchor="w")

    tk.Label(
        inside,
        text=str(value),
        font=("Segoe UI", 20, "bold"),
        bg=theme["card"],
        fg=theme["text"]
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
        pady=7
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
        highlightthickness=0
    )


def labeled_entry(parent, label_text, theme, width=20):
    frame = tk.Frame(parent, bg=theme["card"])

    tk.Label(
        frame,
        text=label_text,
        font=("Segoe UI", 9, "bold"),
        bg=theme["card"],
        fg=theme["text"]
    ).pack(anchor="w", pady=(0, 4))

    entry = styled_entry(frame, theme, width)
    entry.pack(fill="x")
    return frame, entry


def draw_line_chart(parent, labels, values, title, theme, line_color=None):
    if line_color is None:
        line_color = theme["accent"]

    canvas = tk.Canvas(
        parent,
        height=220,
        bg=theme["card"],
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True, padx=10, pady=10)

    canvas.create_text(
        12, 12,
        anchor="nw",
        text=title,
        fill=theme["text"],
        font=("Segoe UI", 11, "bold")
    )

    if len(values) == 0:
        return canvas

    width = 520
    height = 160
    left = 45
    top = 40

    canvas.create_line(left, top, left, top + height, fill=theme["border"])
    canvas.create_line(left, top + height, left + width, top + height, fill=theme["border"])

    max_value = max(values)
    if max_value <= 0:
        max_value = 1

    points = []
    count = len(values)

    for index in range(count):
        if count == 1:
            x = left + width / 2
        else:
            x = left + (index * width / (count - 1))

        y = top + height - ((values[index] / max_value) * (height - 15))
        points.append((x, y))

        canvas.create_text(
            x,
            top + height + 16,
            text=labels[index],
            fill=theme["muted"],
            font=("Segoe UI", 8)
        )

    for index in range(len(points) - 1):
        x1, y1 = points[index]
        x2, y2 = points[index + 1]
        canvas.create_line(x1, y1, x2, y2, fill=line_color, width=3, smooth=True)

    for x, y in points:
        canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=line_color, outline=line_color)

    return canvas


def draw_bar_chart(parent, labels, values, title, theme, colors=None):
    canvas = tk.Canvas(
        parent,
        height=220,
        bg=theme["card"],
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True, padx=10, pady=10)

    canvas.create_text(
        12, 12,
        anchor="nw",
        text=title,
        fill=theme["text"],
        font=("Segoe UI", 11, "bold")
    )

    if len(values) == 0:
        return canvas

    if colors is None:
        colors = [theme["accent"], theme["blue"], theme["green"], theme["accent_2"]]

    left = 45
    top = 45
    chart_height = 145
    chart_width = 520
    max_value = max(values)
    if max_value <= 0:
        max_value = 1

    bar_space = chart_width / len(values)
    bar_width = bar_space * 0.55

    for index in range(len(values)):
        x1 = left + (index * bar_space) + ((bar_space - bar_width) / 2)
        x2 = x1 + bar_width
        bar_height = (values[index] / max_value) * chart_height
        y1 = top + chart_height - bar_height
        y2 = top + chart_height
        color = colors[index % len(colors)]

        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        canvas.create_text(
            (x1 + x2) / 2,
            y1 - 10,
            text=str(values[index]),
            fill=theme["text"],
            font=("Segoe UI", 8)
        )
        canvas.create_text(
            (x1 + x2) / 2,
            y2 + 16,
            text=labels[index],
            fill=theme["muted"],
            font=("Segoe UI", 8)
        )

    return canvas


def draw_donut_chart(parent, labels, values, title, theme, colors=None):
    canvas = tk.Canvas(
        parent,
        height=220,
        bg=theme["card"],
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True, padx=10, pady=10)

    canvas.create_text(
        12, 12,
        anchor="nw",
        text=title,
        fill=theme["text"],
        font=("Segoe UI", 11, "bold")
    )

    if colors is None:
        colors = [theme["accent"], theme["green"], theme["blue"], theme["accent_2"]]

    total = 0
    for value in values:
        total = total + value

    if total <= 0:
        canvas.create_text(
            140, 120,
            text="No data yet",
            fill=theme["muted"],
            font=("Segoe UI", 10)
        )
        return canvas

    x1 = 40
    y1 = 50
    x2 = 180
    y2 = 190
    start_angle = 0

    for index in range(len(values)):
        angle = (values[index] / total) * 360
        canvas.create_arc(
            x1, y1, x2, y2,
            start=start_angle,
            extent=angle,
            fill=colors[index % len(colors)],
            outline=theme["card"]
        )
        start_angle = start_angle + angle

    canvas.create_oval(75, 85, 145, 155, fill=theme["card"], outline=theme["card"])

    legend_y = 65
    for index in range(len(labels)):
        color = colors[index % len(colors)]
        canvas.create_rectangle(230, legend_y, 242, legend_y + 12, fill=color, outline="")
        canvas.create_text(
            250, legend_y + 6,
            anchor="w",
            text=labels[index] + ": " + str(round(values[index], 1)),
            fill=theme["text"],
            font=("Segoe UI", 9)
        )
        legend_y = legend_y + 28

    return canvas


def draw_horizontal_bars(parent, labels, values, title, theme):
    canvas = tk.Canvas(
        parent,
        height=240,
        bg=theme["card"],
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True, padx=10, pady=10)

    canvas.create_text(
        12, 12,
        anchor="nw",
        text=title,
        fill=theme["text"],
        font=("Segoe UI", 11, "bold")
    )

    if len(values) == 0:
        canvas.create_text(
            20, 60,
            anchor="w",
            text="No habit category data yet",
            fill=theme["muted"]
        )
        return canvas

    colors = [theme["accent"], theme["blue"], theme["green"], theme["accent_2"], theme["yellow"]]

    y = 55
    for index in range(len(values)):
        value = values[index]
        bar_width = value * 3.6
        color = colors[index % len(colors)]

        canvas.create_text(15, y + 10, anchor="w", text=labels[index], fill=theme["text"])
        canvas.create_rectangle(130, y, 130 + bar_width, y + 22, fill=color, outline="")
        canvas.create_text(500, y + 11, anchor="e", text=str(value) + "%", fill=theme["muted"])
        y = y + 35

    return canvas
