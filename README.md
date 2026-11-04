# UPSHIFT Productivity Tracker

UPSHIFT is a beginner-friendly Python desktop productivity tracker built as a Python Programming Mini Project.

It combines four tracking areas in one application:

- Calendar
- Academics
- Habits
- Finance

It also includes a Dashboard, Statistics page, Settings, and Light/Dark themes.

## Project Status

The current mini-project scope is feature complete. Remaining work is mainly final testing, review fixes, presentation preparation, and Windows deployment packaging.

## Repository Structure

```text
UPSHIFT-Productivity-Tracker/
│
├── main.py
├── run_tests.py
├── requirements.txt
├── README.md
│
├── app/
│   ├── database.py
│   ├── analytics.py
│   ├── date_helpers.py
│   ├── theme.py
│   ├── ui_helpers.py
│   └── ui/
│       ├── dashboard.py
│       ├── calendar_page.py
│       ├── academics.py
│       ├── habits.py
│       ├── finance.py
│       ├── statistics.py
│       └── settings.py
│
├── tests/
│   ├── test_database.py
│   └── test_analytics.py
│
├── docs/
│   ├── START_HERE.md
│   ├── LEARNING_MAP.md
│   ├── TEST_REPORT.md
│   └── CONTRIBUTING.md
│
└── scripts/
    └── build_windows.py
```

## Folder Guide

### `app/`

Contains the actual application code.

- `database.py`: SQLite storage and data operations
- `analytics.py`: scores, percentages, XP, and statistics
- `date_helpers.py`: display and database date conversion
- `theme.py`: Light and Dark theme colours
- `ui_helpers.py`: shared Tkinter styling and chart functions
- `ui/`: individual screens

### `tests/`

Contains automated checks for the database and analytics logic.

### `docs/`

Contains the learning guide, test report, and collaboration instructions.

### `scripts/`

Contains optional build utilities. These are not needed for normal use.

## Technology Stack

- Python
- Tkinter
- SQLite using Python's built-in `sqlite3`
- `datetime` and `calendar`
- Visual Studio Code
- GitHub

No third-party Python package is required to run the normal application.

## How to Run

Install Python 3, download or clone the repository, open the repository folder in VS Code, and run:

```text
python main.py
```

or:

```text
py main.py
```

## First Launch

On first launch, UPSHIFT asks for a display name and monthly budget. It then creates its SQLite database automatically.

## Local Data

User data is stored locally at:

```text
%LOCALAPPDATA%\PinnacleTracker\tracker.db
```

The older internal folder name is intentionally retained so existing testers continue seeing their saved data after the application was renamed to UPSHIFT.

The database file is excluded from GitHub.

## Date Format

Dates shown to the user use:

```text
DD/MM/YYYY
```

Dates are stored internally as `YYYY-MM-DD` for reliable sorting and calculations.

## Testing

Run:

```text
python run_tests.py
```

or:

```text
py run_tests.py
```

See `docs/TEST_REPORT.md` for the test summary.

## Learning the Code

Recommended order:

1. `main.py`
2. `app/database.py`
3. `app/analytics.py`
4. `app/ui/habits.py`
5. the remaining files inside `app/ui/`

More guidance is available in `docs/START_HERE.md` and `docs/LEARNING_MAP.md`.

## Main Workflow

```text
User
  ↓
Tkinter Interface
  ↓
Python Functions
  ↓
Database + Analytics
  ↓
SQLite Storage
  ↓
Dashboard + Statistics
```

## Team

- **Arnav**: core Python logic, system integration, debugging, testing, and project organisation
- **Hiren**: database and data handling
- **Rishan**: frontend and graphical user interface
- **Nandit**: analytics, progress metrics, and calculations

## Windows Build

The optional PyInstaller helper is located at:

```text
scripts/build_windows.py
```

It is only needed when preparing the final Windows executable.

## Academic Project

UPSHIFT was created as a Python Programming Mini Project. The group should understand, test, explain, and be able to modify the code used in the final submission.
