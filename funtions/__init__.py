"""
functions package.

Re-exports everything so the rest of the project can simply do:

    import functions as fn
    fn.add_expense("2026-11-24", "Food", 150, "Dinner")
"""

from .storage import load_data, save_data, DATA_FILE
from .expense_manager import (
    CATEGORIES,
    validate_date,
    validate_amount,
    validate_category,
    validate_month,
    current_month,
    today,
    add_expense,
    get_all_expenses,
    get_expense,
    edit_expense,
    delete_expense,
    search_by_category,
    search_by_date_range,
    get_budget,
    set_budget,
    get_month_expenses,
    monthly_summary,
    highest_category,
    check_budget,
)
