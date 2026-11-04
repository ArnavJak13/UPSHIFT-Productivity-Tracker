"""Simple SQLite functions for Pinnacle Tracker.

This file intentionally uses normal functions instead of classes so the
student code is easier to follow.
"""

import os
import sqlite3
from datetime import date


APP_FOLDER_NAME = "PinnacleTracker"


def get_database_path():
    """Return a safe database location on Windows or the current computer."""
    local_app_data = os.getenv("LOCALAPPDATA")

    if local_app_data:
        folder = os.path.join(local_app_data, APP_FOLDER_NAME)
    else:
        folder = os.path.join(os.path.expanduser("~"), ".pinnacle_tracker")

    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "tracker.db")


DB_PATH = get_database_path()


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create all tables if they do not already exist."""
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date TEXT NOT NULL,
            title TEXT NOT NULL,
            notes TEXT DEFAULT '',
            completed INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            subject TEXT NOT NULL,
            study_hours REAL DEFAULT 0,
            target_hours REAL DEFAULT 0,
            assignments_done INTEGER DEFAULT 0,
            assignments_total INTEGER DEFAULT 0,
            notes TEXT DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            xp_reward INTEGER DEFAULT 10,
            frequency TEXT DEFAULT 'Daily',
            days TEXT DEFAULT '',
            active INTEGER DEFAULT 1,
            created_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            xp_earned INTEGER DEFAULT 0,
            UNIQUE(habit_id, completion_date)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            entry_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT DEFAULT ''
        )
    """)

    connection.commit()
    connection.close()


# ---------------- SETTINGS ----------------

def get_setting(key, default_value=""):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT setting_value FROM settings WHERE setting_key = ?", (key,))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        return default_value
    return row["setting_value"]


def save_setting(key, value):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO settings (setting_key, setting_value) VALUES (?, ?)",
        (key, str(value))
    )
    connection.commit()
    connection.close()


# ---------------- CALENDAR ----------------

def add_event(event_date, title, notes=""):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO calendar_events (event_date, title, notes) VALUES (?, ?, ?)",
        (event_date, title.strip(), notes.strip())
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def get_events_for_month(year, month):
    month_text = str(month).zfill(2)
    search_text = str(year) + "-" + month_text + "-%"

    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM calendar_events WHERE event_date LIKE ? ORDER BY event_date, id",
        (search_text,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_events_for_date(event_date):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM calendar_events WHERE event_date = ? ORDER BY id",
        (event_date,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def toggle_event_completed(event_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT completed FROM calendar_events WHERE id = ?", (event_id,))
    row = cursor.fetchone()

    if row is not None:
        new_value = 0
        if row["completed"] == 0:
            new_value = 1
        cursor.execute(
            "UPDATE calendar_events SET completed = ? WHERE id = ?",
            (new_value, event_id)
        )

    connection.commit()
    connection.close()


def delete_event(event_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM calendar_events WHERE id = ?", (event_id,))
    connection.commit()
    connection.close()


# ---------------- ACADEMICS ----------------

def add_academic_entry(entry_date, subject, study_hours, target_hours,
                       assignments_done, assignments_total, notes=""):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO academics
        (entry_date, subject, study_hours, target_hours,
         assignments_done, assignments_total, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entry_date,
        subject.strip(),
        study_hours,
        target_hours,
        assignments_done,
        assignments_total,
        notes.strip()
    ))
    connection.commit()
    connection.close()


def get_academic_entries(limit=100):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM academics ORDER BY entry_date DESC, id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_academic_entries_between(start_date, end_date):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM academics
        WHERE entry_date >= ? AND entry_date <= ?
        ORDER BY entry_date, id
    """, (start_date, end_date))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def delete_academic_entry(entry_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM academics WHERE id = ?", (entry_id,))
    connection.commit()
    connection.close()


# ---------------- HABITS ----------------

def add_habit(name, category, xp_reward, frequency, days):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO habits
        (name, category, xp_reward, frequency, days, created_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name.strip(),
        category,
        xp_reward,
        frequency,
        days,
        date.today().isoformat()
    ))
    connection.commit()
    connection.close()


def get_active_habits():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM habits WHERE active = 1 ORDER BY id")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_all_habits():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM habits ORDER BY id")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def habit_is_completed(habit_id, completion_date):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM habit_completions
        WHERE habit_id = ? AND completion_date = ?
    """, (habit_id, completion_date))
    row = cursor.fetchone()
    connection.close()
    return row is not None


def toggle_habit_completion(habit_id, completion_date, xp_reward):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM habit_completions
        WHERE habit_id = ? AND completion_date = ?
    """, (habit_id, completion_date))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO habit_completions
            (habit_id, completion_date, xp_earned)
            VALUES (?, ?, ?)
        """, (habit_id, completion_date, xp_reward))
    else:
        cursor.execute("DELETE FROM habit_completions WHERE id = ?", (row["id"],))

    connection.commit()
    connection.close()


def archive_habit(habit_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE habits SET active = 0 WHERE id = ?", (habit_id,))
    connection.commit()
    connection.close()


def get_habit_completions_between(start_date, end_date):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT habit_completions.*, habits.name, habits.category
        FROM habit_completions
        JOIN habits ON habits.id = habit_completions.habit_id
        WHERE completion_date >= ? AND completion_date <= ?
        ORDER BY completion_date, habit_id
    """, (start_date, end_date))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_all_habit_completions():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT habit_completions.*, habits.name, habits.category
        FROM habit_completions
        JOIN habits ON habits.id = habit_completions.habit_id
        ORDER BY completion_date, habit_id
    """)
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


# ---------------- FINANCE ----------------

def add_finance_entry(entry_date, entry_type, category, amount, notes=""):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO finance
        (entry_date, entry_type, category, amount, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (entry_date, entry_type, category, amount, notes.strip()))
    connection.commit()
    connection.close()


def get_finance_entries(limit=100):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM finance ORDER BY entry_date DESC, id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_finance_entries_between(start_date, end_date):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM finance
        WHERE entry_date >= ? AND entry_date <= ?
        ORDER BY entry_date, id
    """, (start_date, end_date))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def delete_finance_entry(entry_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM finance WHERE id = ?", (entry_id,))
    connection.commit()
    connection.close()


# ---------------- RESET ----------------

def reset_all_data():
    connection = connect_db()
    cursor = connection.cursor()

    tables = [
        "calendar_events",
        "academics",
        "habit_completions",
        "habits",
        "finance"
    ]

    for table in tables:
        cursor.execute("DELETE FROM " + table)

    connection.commit()
    connection.close()
