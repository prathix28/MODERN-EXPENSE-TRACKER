"""
storage.py - File I/O only.

Reads and writes data/expenses.json. Nothing else in the project
touches the file directly.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "expenses.json")


def load_data():
    """Return {'budget_limit': float, 'expenses': list} from the JSON file."""
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
