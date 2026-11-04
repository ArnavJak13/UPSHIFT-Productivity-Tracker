"""Simple date conversion functions used by the user interface."""

from datetime import date


def to_storage_date(display_date):
    """Convert DD/MM/YYYY into YYYY-MM-DD for the database."""
    parts = display_date.split("/")

    if len(parts) != 3:
        raise ValueError("Date must use DD/MM/YYYY format")

    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])

    real_date = date(year, month, day)
    return real_date.isoformat()


def to_display_date(storage_date):
    """Convert YYYY-MM-DD from the database into DD/MM/YYYY."""
    parts = storage_date.split("-")

    if len(parts) != 3:
        return storage_date

    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])

    real_date = date(year, month, day)
    return real_date.strftime("%d/%m/%Y")


def today_display():
    """Return today's date in DD/MM/YYYY format."""
    return date.today().strftime("%d/%m/%Y")
