# UPSHIFT — Personal Productivity Tracker

UPSHIFT is a Python desktop application designed to help users track and review important areas of their daily life in one place.

The project currently focuses on four main tracking domains:

- Calendar
- Academics
- Habits
- Finance

It also includes a Dashboard, Statistics page, and Settings page so the user can view progress, analyse consistency, and personalise the application.

## Project Purpose

People often use different notebooks, apps, or spreadsheets to manage their studies, habits, finances, and schedules. This makes it difficult to get one clear view of overall progress.

UPSHIFT brings these areas together into one local desktop application and converts stored data into simple scores, summaries, and visual statistics.

## Main Features

### Dashboard

The Dashboard gives a quick overview of the user's recent progress across the different modules.

It includes:

- Overall progress
- Habit completion
- Academic progress
- Finance status
- Calendar consistency
- XP information
- Visual graphs and summaries

### Calendar

The Calendar module allows users to:

- Add events for specific dates
- View event names directly on calendar dates
- Mark events as completed
- View daily information from other modules
- Navigate between months

Dates are displayed in DD/MM/YYYY format.

### Academics

The Academics module allows users to:

- Record study hours
- Set target study hours
- Track assignments
- Add subjects and notes
- Review academic history
- Measure daily academic progress

Old academic records remain saved when a new day begins.

### Habits

The Habits module allows users to:

- Create habits
- Assign categories
- Select XP rewards
- Choose daily or selected weekday schedules
- Mark habits as complete
- Track current streaks
- Track longest streaks
- Archive habits
- Measure habit consistency

Habit completions are stored separately by date so historical progress can be calculated correctly.

### Finance

The Finance module allows users to:

- Record expenses
- Record income
- Record savings
- Use transaction categories
- Set a monthly budget
- Review transaction history
- Measure monthly finance performance

### Statistics

The Statistics page converts stored data into visual progress information.

It includes multiple graph types such as:

- Line graphs
- Area graphs
- Bar graphs
- Horizontal bar graphs
- Donut charts

Statistics can be viewed over different time periods.

### Settings

The Settings page allows users to:

- Change display name
- Change monthly budget
- Switch between Light and Dark mode
- Choose a default page
- Export a JSON backup
- Reset local tracker data

## Technology Stack

- Python
- Tkinter for the graphical user interface
- SQLite through Python's built-in sqlite3 module
- datetime and calendar for date handling
- JSON for backup export
- GitHub for version control and collaboration
- Visual Studio Code for development

The current application does not require NumPy, Pandas, Matplotlib, or other external Python packages to run.

## Basic Application Workflow

```text
User
  ↓
Tkinter Interface
  ↓
Python Functions
  ↓
Database / Analytics
  ↓
SQLite Storage
  ↓
Dashboard and Statistics
```

The application starts from `main.py`.

## Project Structure

```text
UPSHIFT/
│
├── main.py
├── database.py
├── analytics.py
├── date_helpers.py
├── theme.py
├── ui_helpers.py
├── run_tests.py
│
├── ui/
│   ├── dashboard.py
│   ├── calendar_page.py
│   ├── academics.py
│   ├── habits.py
│   ├── finance.py
│   ├── statistics.py
│   └── settings.py
│
└── tests/
```

## How to Run

### 1. Install Python

Install Python 3 on Windows.

Check the installation using:

```bash
python --version
```

or:

```bash
py --version
```

### 2. Download the Project

Clone this repository or download it as a ZIP file.

### 3. Open the Project Folder

Open the complete project folder in Visual Studio Code.

### 4. Run the Application

Run:

```bash
python main.py
```

If `python` does not work on your computer, try:

```bash
py main.py
```

The application will create its local SQLite database automatically on first launch.

## Local Data Storage

UPSHIFT stores each user's personal data locally on their Windows computer.

The database is stored in:

```text
%LOCALAPPDATA%\PinnacleTracker\tracker.db
```

The local database should not be uploaded to GitHub.

## Testing

The project includes automated tests.

Run:

```bash
python run_tests.py
```

or:

```bash
py run_tests.py
```

## Team

This mini project was developed by:

- Arnav — Core Python logic, system integration, debugging, testing, and project organisation
- Hiren — Database and data handling
- Rishan — Frontend and graphical user interface
- Nandit — Analytics, progress metrics, and calculations

## Current Status

The main application is feature complete for the current mini project scope.

Current work mainly involves:

- Testing
- Bug fixing
- Code understanding
- Presentation preparation
- Final deployment preparation

## Future Improvements

Possible future improvements include:

- Windows installer
- Notifications and reminders
- More advanced analytics
- Data import and export
- Additional productivity modules
- Optional cloud synchronisation
- Improved accessibility

## Academic Project

UPSHIFT was created as a Python Programming Mini Project.

The project is intentionally written using understandable Python concepts so that the team can study, explain, test, and modify the code during evaluation and viva.
