# UPSHIFT Productivity Tracker

UPSHIFT is a beginner-friendly Python desktop application that brings four everyday tracking areas into one place:

- Calendar
- Academics
- Habits
- Finance

It also includes a Dashboard, Statistics page, and Settings page so users can review progress instead of keeping information scattered across separate notebooks, spreadsheets, or apps.

## Project Status

The current mini-project scope is feature complete.

The remaining work before academic submission is mainly:

- final testing
- bug fixes found during review
- presentation preparation
- final Windows deployment packaging

## Core Features

### Dashboard

Shows an overview of recent progress, including habit completion, academic performance, finance status, calendar consistency, XP, and visual summaries.

### Calendar

Users can add dated events, view event names on calendar dates, mark events as completed, and move between months.

All dates shown to the user use **DD/MM/YYYY** format.

### Academics

Users can record subjects, study hours, target hours, assignments, and notes. Historical academic entries remain stored and can be used in progress calculations.

### Habits

Users can create daily or selected-weekday habits, assign categories and XP rewards, mark habits as complete, and track consistency over time.

Habit completion is stored separately by date so historical progress can be calculated correctly.

### Finance

Users can record income, expenses, and savings, organise entries by category, set a monthly budget, and review finance performance.

### Statistics

The Statistics page turns stored data into visual summaries using line charts, bar charts, horizontal bars, and donut charts drawn with Tkinter Canvas.

### Settings

Users can:

- change their display name
- change their monthly budget
- switch between Light and Dark mode
- reset tracker records

## Technology Stack

- Python
- Tkinter for the desktop GUI
- SQLite through Python's built-in `sqlite3` module
- `datetime` and `calendar` for date handling
- Visual Studio Code for development
- GitHub for version control and collaboration

The running application does not require NumPy, Pandas, Matplotlib, HTML, CSS, or JavaScript.

## Application Workflow

```text
User
  ↓
Tkinter Interface
  ↓
Python Functions
  ↓
Database and Analytics
  ↓
SQLite Storage
  ↓
Dashboard and Statistics
```

## Project Structure

```text
UPSHIFT-Productivity-Tracker/
│
├── main.py
├── database.py
├── analytics.py
├── date_helpers.py
├── theme.py
├── ui_helpers.py
├── run_tests.py
├── build_windows.py
├── requirements.txt
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── calendar_page.py
│   ├── academics.py
│   ├── habits.py
│   ├── finance.py
│   ├── statistics.py
│   └── settings.py
│
├── tests/
│   ├── __init__.py
│   ├── test_analytics.py
│   └── test_database.py
│
├── START_HERE.md
├── LEARNING_MAP.md
└── TEST_REPORT.md
```

## How to Run

### 1. Install Python

Install Python 3 on Windows and check it with:

```text
python --version
```

If your system uses the Python launcher, use:

```text
py --version
```

### 2. Clone or Download the Repository

You can clone the repository with Git or use GitHub's **Code > Download ZIP** option.

### 3. Open the Project Folder

Open the repository folder in Visual Studio Code.

### 4. Start the Application

Run:

```text
python main.py
```

or:

```text
py main.py
```

The app creates its SQLite database automatically on first launch.

## Local Data Storage

User data is stored locally and is not committed to GitHub.

For compatibility with earlier development versions, the current database location remains:

```text
%LOCALAPPDATA%\PinnacleTracker\tracker.db
```

The folder name is kept internally so existing testers do not lose access to their saved data after the project branding changed to UPSHIFT.

## Testing

Run the included test suite with:

```text
python run_tests.py
```

or:

```text
py run_tests.py
```

See `TEST_REPORT.md` for the checks performed during the beginner-version rewrite.

## Windows Executable

The source project runs directly with Python.

An optional helper file, `build_windows.py`, is included for later Windows executable packaging with PyInstaller. PyInstaller is not required to run the normal Python version.

## Team

- **Arnav**: core Python logic, system integration, debugging, testing, and project organisation
- **Hiren**: database and data handling
- **Rishan**: frontend and graphical user interface
- **Nandit**: analytics, progress metrics, and calculations

## Learning and Viva Preparation

This version intentionally avoids unnecessary advanced Python patterns so the group can read and explain the application.

Start with:

1. `main.py`
2. `database.py`
3. `analytics.py`
4. one page inside `ui/`

See `START_HERE.md` and `LEARNING_MAP.md` for a guided study order.

## Future Improvements

Possible extensions after the academic submission include:

- reminders and notifications
- additional productivity modules
- richer data export and import
- optional cloud synchronisation
- improved accessibility
- installer-based Windows deployment

## Academic Project

UPSHIFT was created as a Python Programming Mini Project. The code should be read, tested, understood, and explained by the team during review and viva.
