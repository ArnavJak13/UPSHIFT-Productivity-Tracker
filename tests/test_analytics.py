"""Very small analytics checks using plain assert statements."""

import os
import tempfile
from datetime import date

import analytics
import database


def run_analytics_tests():
    old_path = database.DB_PATH
    temp_folder = tempfile.TemporaryDirectory()
    database.DB_PATH = os.path.join(temp_folder.name, "test.db")
    database.init_db()

    daily_habit = {
        "active": 1,
        "created_date": "2026-10-01",
        "frequency": "Daily",
        "days": ""
    }
    assert analytics.habit_is_scheduled(daily_habit, date(2026, 10, 24)) is True

    selected_day_habit = {
        "active": 1,
        "created_date": "2026-10-01",
        "frequency": "Selected Days",
        "days": "Mon,Wed,Fri"
    }
    assert analytics.habit_is_scheduled(selected_day_habit, date(2026, 10, 23)) is True
    assert analytics.habit_is_scheduled(selected_day_habit, date(2026, 10, 24)) is False

    database.add_habit("Read", "Personal", 10, "Daily", "")
    habit = database.get_active_habits()[0]
    database.toggle_habit_completion(habit["id"], "2026-10-24", 10)
    assert analytics.get_total_xp() == 10

    database.DB_PATH = old_path
    temp_folder.cleanup()
    print("Analytics tests passed")


if __name__ == "__main__":
    run_analytics_tests()
