"""Very small database checks using plain assert statements."""

import os
import tempfile

from app import database


def run_database_tests():
    old_path = database.DB_PATH
    temp_folder = tempfile.TemporaryDirectory()
    database.DB_PATH = os.path.join(temp_folder.name, "test.db")
    database.init_db()

    database.save_setting("display_name", "Arnav")
    assert database.get_setting("display_name") == "Arnav"

    database.add_habit("Read", "Personal", 10, "Daily", "")
    habit = database.get_active_habits()[0]
    database.toggle_habit_completion(habit["id"], "2026-10-24", 10)

    assert database.habit_is_completed(habit["id"], "2026-10-24") is True
    assert database.habit_is_completed(habit["id"], "2026-10-25") is False

    database.add_event("2026-10-30", "Project Demo", "")
    events = database.get_events_for_date("2026-10-30")
    assert events[0]["title"] == "Project Demo"

    database.DB_PATH = old_path
    temp_folder.cleanup()
    print("Database tests passed")


if __name__ == "__main__":
    run_database_tests()
