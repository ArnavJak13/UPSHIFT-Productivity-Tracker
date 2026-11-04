# START HERE

If the advanced prototype looked confusing, start with this file order.

## Day 1: Understand how the program starts

Open `main.py`.

Only focus on these functions first:

- `start_app()`
- `show_welcome()`
- `build_main_layout()`
- `show_dashboard()`
- `show_habits()`

Do not try to understand every Tkinter option such as fonts, padding, or colors.

## Day 2: Understand saving data

Open `database.py`.

Start with only:

- `connect_db()`
- `init_db()`
- `save_setting()`
- `add_habit()`
- `get_active_habits()`
- `toggle_habit_completion()`

Once these make sense, the Calendar, Academics, and Finance database functions
work using the same idea.

## Day 3: Understand calculations

Open `analytics.py`.

Start with:

- `habit_is_scheduled()`
- `get_scheduled_habits()`
- `habit_completion_for_day()`
- `get_total_xp()`

These are mostly loops, conditions, lists, and normal functions.

## Day 4: Understand one complete screen

Open `ui/habits.py`.

Follow this order:

1. The form widgets are created.
2. `save_habit()` reads the form.
3. `if` statements validate it.
4. `database.add_habit()` saves it.
5. A `for` loop displays today's habits.
6. A button calls `database.toggle_habit_completion()`.

Once you understand Habits, the other screens follow similar patterns.

## Ignore this until later

`ui_helpers.py` is mostly styling and chart drawing. It contains more coordinate
math because graphs have to be drawn on a Tkinter Canvas. You do not need to
start there to understand how the tracker stores and processes data.

## Important project change

The advanced prototype used many OOP classes. This beginner version has **no
classes in the application code**. It uses normal functions instead.
