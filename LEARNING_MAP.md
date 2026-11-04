# Beginner Learning Map

## Concepts you probably already know

The project uses these everywhere:

- variables
- strings and numbers
- lists
- dictionaries
- `if`, `elif`, `else`
- `for` loops
- functions with `def`
- `return`

## New concepts you actually need to learn

### 1. Imports

```python
import database
from datetime import date
```

An import lets one Python file use code from another file or Python module.

### 2. Tkinter widgets

The GUI is made from widgets such as:

```python
tk.Label(...)
tk.Button(...)
tk.Entry(...)
tk.Frame(...)
```

### 3. `pack()` and `grid()`

These tell Tkinter where a widget should appear.

### 4. Button commands

```python
tk.Button(..., command=save_entry)
```

When the button is clicked, Python runs the named function.

### 5. SQLite

The important commands are:

- `CREATE TABLE`
- `INSERT`
- `SELECT`
- `UPDATE`
- `DELETE`

Python sends these commands through `sqlite3`.

### 6. `try/except`

Used when user input might be wrong.

```python
try:
    amount = float(amount_entry.get())
except ValueError:
    print("Invalid amount")
```

### 7. Dates

```python
date.today()
```

The user enters and sees dates as `24/10/2026`. The database stores the same date internally as `2026-10-24` so sorting and calculations stay simple.

### 8. Nested functions

Some button functions are defined inside a page function because they need the
entries and variables on that page.

Example:

```python
def show_page():
    def save_data():
        print("Saved")
```

This is still a normal `def` function.

## What happened to OOP?

This beginner edition does not require OOP for the application structure.
That is intentional. The advanced prototype used many classes and inheritance,
but this version uses normal functions so your group can focus on the Python
concepts you currently know.
