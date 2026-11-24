"""
functions package - all the logic (no input/print) for the Smart Expense Tracker.

The GUI (gui/dashboard.py) or main.py just calls these functions.
Data is stored in data/expenses.json.
"""

import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "expenses.json")

DATE_FORMAT = "%Y-%m-%d"
MONTH_FORMAT = "%Y-%m"
CATEGORIES = ["Food", "Travel", "Rent", "Entertainment", "Education", "Other"]


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------
def load_data():
    """Read the JSON file and return {'budget_limit': float, 'expenses': list}."""
    default = {"budget_limit": 0.0, "expenses": []}
    if not os.path.exists(DATA_FILE):
        return default
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return default
    data.setdefault("budget_limit", 0.0)
    data.setdefault("expenses", [])
    return data


def save_data(data):
    """Write the data dictionary to the JSON file (creates the folder if needed)."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def validate_date(date_text):
    """Return the date as 'YYYY-MM-DD' or raise ValueError."""
    try:
        return datetime.strptime(str(date_text).strip(), DATE_FORMAT).strftime(DATE_FORMAT)
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format, e.g. 2026-11-24.")


def validate_amount(amount):
    """Return the amount as a positive float (2 decimals) or raise ValueError."""
    try:
        value = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.")
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(value, 2)


def validate_category(category):
    """Return a cleaned category name or raise ValueError if blank."""
    category = str(category).strip()
    if not category:
        raise ValueError("Please choose a category.")
    for known in CATEGORIES:
        if category.lower() == known.lower():
            return known
    return category.title()  # allow custom categories


def validate_month(month_text):
    """Return the month as 'YYYY-MM' or raise ValueError."""
    try:
        return datetime.strptime(str(month_text).strip(), MONTH_FORMAT).strftime(MONTH_FORMAT)
    except ValueError:
        raise ValueError("Month must be in YYYY-MM format, e.g. 2026-11.")


def current_month():
    """Return this month as 'YYYY-MM'."""
    return datetime.now().strftime(MONTH_FORMAT)


def today():
    """Return today's date as 'YYYY-MM-DD'."""
    return datetime.now().strftime(DATE_FORMAT)


# ---------------------------------------------------------------------------
# Add / View / Edit / Delete
# ---------------------------------------------------------------------------
def _next_id(expenses):
    return max((e["id"] for e in expenses), default=0) + 1


def add_expense(date_text, category, amount, description=""):
    """Validate and add a new expense. Returns the new expense dictionary."""
    expense_date = validate_date(date_text)
    category = validate_category(category)
    amount = validate_amount(amount)

    data = load_data()
    expense = {
        "id": _next_id(data["expenses"]),
        "date": expense_date,
        "category": category,
        "amount": amount,
        "description": str(description).strip(),
    }
    data["expenses"].append(expense)
    save_data(data)
    return expense


def get_all_expenses():
    """Return all expenses sorted by date (newest first)."""
    expenses = load_data()["expenses"]
    return sorted(expenses, key=lambda e: (e["date"], e["id"]), reverse=True)


def get_expense(expense_id):
    """Return one expense by id, or None if it does not exist."""
    for e in load_data()["expenses"]:
        if e["id"] == expense_id:
            return e
    return None


def edit_expense(expense_id, date_text=None, category=None, amount=None, description=None):
    """
    Update the given fields of an expense (fields left as None are unchanged).
    Returns the updated expense, or raises ValueError if the id is not found.
    """
    data = load_data()
    for e in data["expenses"]:
        if e["id"] == expense_id:
            if date_text is not None:
                e["date"] = validate_date(date_text)
            if category is not None:
                e["category"] = validate_category(category)
            if amount is not None:
                e["amount"] = validate_amount(amount)
            if description is not None:
                e["description"] = str(description).strip()
            save_data(data)
            return e
    raise ValueError(f"No expense found with ID {expense_id}.")


def delete_expense(expense_id):
    """Delete an expense by id. Returns True if deleted, False if not found."""
    data = load_data()
    before = len(data["expenses"])
    data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
    if len(data["expenses"]) == before:
        return False
    save_data(data)
    return True


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
def search_by_category(category):
    """Return all expenses in the given category (case-insensitive)."""
    category = str(category).strip().lower()
    return [e for e in get_all_expenses() if e["category"].lower() == category]


def search_by_date_range(start_date, end_date):
    """Return expenses between start_date and end_date (both inclusive)."""
    start = validate_date(start_date)
    end = validate_date(end_date)
    if start > end:
        start, end = end, start
    return [e for e in get_all_expenses() if start <= e["date"] <= end]


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------
def get_budget():
    """Return the monthly budget limit (0 means no limit set)."""
    return load_data()["budget_limit"]


def set_budget(limit):
    """Save a new monthly budget limit."""
    limit = validate_amount(limit)
    data = load_data()
    data["budget_limit"] = limit
    save_data(data)
    return limit


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------
def get_month_expenses(month):
    """Return all expenses whose date falls in the month 'YYYY-MM'."""
    month = validate_month(month)
    return [e for e in get_all_expenses() if e["date"].startswith(month)]


def monthly_summary(month=None):
    """
    Total spending per category for a month.
    Returns a dict: {category: total}, sorted from highest to lowest.
    """
    month = validate_month(month) if month else current_month()
    totals = {}
    for e in get_month_expenses(month):
        totals[e["category"]] = round(totals.get(e["category"], 0) + e["amount"], 2)
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def highest_category(month=None):
    """Return (category, total) for the highest spending category, or None."""
    totals = monthly_summary(month)
    if not totals:
        return None
    category = max(totals, key=totals.get)
    return category, totals[category]


def check_budget(month=None):
    """
    Compare the month's total with the budget limit.
    Returns a dict:
      {
        'month': 'YYYY-MM', 'total': float, 'limit': float,
        'exceeded': bool, 'difference': float,   # + over budget / - remaining
        'message': str
      }
    """
    month = validate_month(month) if month else current_month()
    total = round(sum(monthly_summary(month).values()), 2)
    limit = get_budget()

    if limit <= 0:
        message = "No budget limit set."
        exceeded = False
        difference = 0.0
    elif total > limit:
        exceeded = True
        difference = round(total - limit, 2)
        message = (f"WARNING: You spent {total:.2f} in {month}, "
                   f"which exceeds your budget of {limit:.2f} by {difference:.2f}!")
    else:
        exceeded = False
        difference = round(total - limit, 2)  # negative = remaining
        message = (f"Within budget. Spent {total:.2f} of {limit:.2f} "
                   f"({limit - total:.2f} remaining).")

    return {
        "month": month,
        "total": total,
        "limit": limit,
        "exceeded": exceeded,
        "difference": difference,
        "message": message,
    }
