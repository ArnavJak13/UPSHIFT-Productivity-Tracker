# Pinnacle Tracker Beginner Edition

A student-friendly Python desktop tracker for:

- Calendar
- Academics
- Habits
- Finance
- Dashboard
- Statistics
- Settings

## Run the project

Open this folder in VS Code and run:

```text
python main.py
```

If Windows uses the Python launcher instead, run:

```text
py main.py
```

## Technology

The running application uses only Python standard-library modules:

- `tkinter` for the desktop interface
- `sqlite3` for local data storage
- `datetime` and `calendar` for dates
- `os` for the database folder

No NumPy, Pandas, Matplotlib, HTML, CSS, or JavaScript is needed.

## Why this edition exists

This edition deliberately avoids advanced programming patterns so first-year
students can understand and explain it in a viva.

It does **not** use:

- application classes
- page inheritance
- advanced type hints
- context managers for the database
- list comprehensions in the main logic
- a custom GUI framework

The code mainly uses variables, strings, lists, dictionaries, loops,
`if/elif/else`, normal functions, `try/except`, imports, basic SQL, and Tkinter.

## Learn the files in this order

1. `main.py`
2. `database.py`
3. `analytics.py`
4. `ui/habits.py`
5. `ui/academics.py`
6. `ui/finance.py`
7. `ui/calendar_page.py`
8. `ui/dashboard.py`
9. `ui/statistics.py`
10. `ui/settings.py`
11. `ui_helpers.py`

`ui_helpers.py` contains most of the chart drawing and styling code. It is okay
to study that later because it mostly controls appearance rather than the core
tracker logic.

## Important

Do not submit code you cannot explain. Read each module, run it, change small
things yourself, and make sure every group member understands the part they
present in the viva.


## Date format

All dates shown to the user use **DD/MM/YYYY**. The SQLite database stores dates internally as **YYYY-MM-DD** for reliable sorting and calculations.
