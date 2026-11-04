# Contributing to UPSHIFT

This repository is used by a student project team. Keep changes small, understandable, and easy to review.

## Before Editing

1. Pull or download the latest version of the repository.
2. Run `main.py` once and confirm the application works.
3. Run `python run_tests.py` or `py run_tests.py`.
4. Edit only the files needed for your task.

## Main Areas

- `main.py`: application startup, navigation, and integration
- `app/database.py`: SQLite tables and data operations
- `app/analytics.py`: scores, percentages, and statistics calculations
- `app/ui/`: individual application screens
- `app/ui_helpers.py`: shared visual helpers and chart drawing
- `tests/`: automated checks

## Commit Rules

Use one commit for one meaningful change.

Good examples:

```text
Fix calendar date validation
Improve finance input checks
Update habit completion calculation
Polish statistics page labels
```

Avoid vague commit messages such as:

```text
changes
final
final2
stuff
```

## Files That Must Not Be Committed

Do not commit:

- `tracker.db`
- `__pycache__/`
- `*.pyc`
- `.vscode/`
- virtual environments
- `build/`
- `dist/`

The repository's `.gitignore` already blocks these.

## Before Sharing a Change

1. Run the application.
2. Test the screen or function you changed.
3. Run the automated tests.
4. Make sure you can explain the code you changed.
5. Commit with a clear message.
