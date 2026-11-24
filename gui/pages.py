
import tkinter as tk
from tkinter import ttk, messagebox

import functions as fn

from gui.components import (
    create_heading,
    create_card,
    create_field,
    create_button,
    create_table,
    WHITE,
    BACKGROUND,
    TEXT,
    GREY,
    BLUE,
    GREEN,
    ORANGE,
    RED
)


# -----------------------------------------
# COMMON HELPER FUNCTIONS
# -----------------------------------------

def format_money(amount):

    return f"₹{float(amount):,.2f}"


def show_error(title, error):

    messagebox.showerror(
        title,
        str(error)
    )


# -----------------------------------------
# DASHBOARD PAGE
# -----------------------------------------

def show_dashboard(parent, app):

    create_heading(
        parent,
        "Welcome back!",
        "Here's your financial overview."
    )

    # Get actual backend data
    records = fn.get_all_expenses()

    month = fn.current_month()

    summary = fn.monthly_summary(month)

    highest = fn.highest_category(month)

    budget_status = fn.check_budget(month)

    total_expenses = sum(
        float(item["amount"])
        for item in records
    )

    monthly_total = budget_status["total"]

    budget_limit = budget_status["limit"]

    remaining = budget_limit - monthly_total

    highest_name = highest[0] if highest else "None"

    # Summary cards
    cards_frame = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    cards_frame.pack(fill="x")

    card_data = [
        ("Total Expenses", format_money(total_expenses), BLUE),
        ("This Month", format_money(monthly_total), GREEN),
        ("Highest Category", highest_name, ORANGE),
        ("Remaining Budget", format_money(remaining),
         RED if remaining < 0 else GREEN)
    ]

    for title, value, color in card_data:

        create_card(
            cards_frame,
            title,
            value,
            color
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

    # Budget warning
    if budget_status["exceeded"]:

        tk.Label(
            parent,
            text=budget_status["message"],
            bg="#FDE8E8",
            fg=RED,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=10
        ).pack(fill="x", pady=15)

    # Recent transactions
    tk.Label(
        parent,
        text="Recent Transactions",
        bg=BACKGROUND,
        fg=TEXT,
        font=("Arial", 15, "bold")
    ).pack(
        anchor="w",
        pady=(25, 12)
    )

    create_table(
        parent,
        records[:5],
        height=5
    )


# -----------------------------------------
# ADD EXPENSE PAGE
# -----------------------------------------

def show_add_expense(parent, app):

    create_heading(
        parent,
        "Add New Expense",
        "Enter the details of your transaction."
    )

    form = tk.Frame(
        parent,
        bg=WHITE,
        padx=30,
        pady=20
    )

    form.pack(
        fill="x",
        pady=10
    )

    amount = create_field(
        form,
        "Amount (₹)"
    )

    tk.Label(
        form,
        text="Category",
        bg=WHITE,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(
        anchor="w",
        pady=(12, 5)
    )

    category = ttk.Combobox(
        form,
        values=fn.CATEGORIES,
        state="readonly",
        font=("Arial", 11)
    )

    category.pack(
        fill="x",
        ipady=7
    )

    expense_date = create_field(
        form,
        "Date (YYYY-MM-DD)",
        fn.today()
    )

    description = create_field(
        form,
        "Description"
    )

    def save_expense():

        try:

            # Backend validates all inputs
            expense = fn.add_expense(
                expense_date.get(),
                category.get(),
                amount.get(),
                description.get()
            )

            messagebox.showinfo(
                "Success",
                f"Expense #{expense['id']} added successfully!"
            )

            app.show_page("Dashboard")

        except ValueError as error:

            show_error("Invalid Input", error)

        except Exception as error:

            show_error("Error", error)

    create_button(
        form,
        "Save Expense",
        save_expense
    ).pack(
        anchor="w",
        pady=20
    )


# -----------------------------------------
# ALL EXPENSES PAGE
# -----------------------------------------

def show_all_expenses(parent, app):

    create_heading(
        parent,
        "All Expenses",
        "View, edit and delete your transactions."
    )

    records = fn.get_all_expenses()

    table = create_table(
        parent,
        records,
        height=10
    )

    buttons = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    buttons.pack(
        fill="x",
        pady=15
    )

    # Get selected expense ID
    def get_selected_id():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense first."
            )

            return None

        return int(selected[0])

    # DELETE EXPENSE
    def delete_selected():

        expense_id = get_selected_id()

        if expense_id is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if confirm:

            try:

                deleted = fn.delete_expense(expense_id)

                if deleted:

                    messagebox.showinfo(
                        "Deleted",
                        "Expense deleted successfully."
                    )

                else:

                    messagebox.showwarning(
                        "Not Found",
                        "Expense ID was not found."
                    )

                app.show_page("All Expenses")

            except Exception as error:

                show_error("Delete Error", error)

    # EDIT EXPENSE
    def edit_selected():

        expense_id = get_selected_id()

        if expense_id is None:
            return

        try:

            expense = fn.get_expense(expense_id)

            if expense is None:

                messagebox.showwarning(
                    "Not Found",
                    "Expense does not exist."
                )

                return

            edit_window = tk.Toplevel(parent)

            edit_window.title("Edit Expense")
            edit_window.geometry("420x520")
            edit_window.configure(bg=WHITE)

            edit_window.transient(parent.winfo_toplevel())
            edit_window.grab_set()

            form = tk.Frame(
                edit_window,
                bg=WHITE,
                padx=25,
                pady=20
            )

            form.pack(
                fill="both",
                expand=True
            )

            tk.Label(
                form,
                text=f"Edit Expense #{expense_id}",
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 17, "bold")
            ).pack(anchor="w", pady=10)

            edit_date = create_field(
                form,
                "Date (YYYY-MM-DD)",
                expense["date"]
            )

            tk.Label(
                form,
                text="Category",
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(10, 5))

            edit_category = ttk.Combobox(
                form,
                values=fn.CATEGORIES,
                font=("Arial", 11)
            )

            edit_category.set(expense["category"])

            edit_category.pack(
                fill="x",
                ipady=7
            )

            edit_amount = create_field(
                form,
                "Amount (₹)",
                str(expense["amount"])
            )

            edit_description = create_field(
                form,
                "Description",
                expense["description"]
            )

            def save_changes():

                try:

                    fn.edit_expense(
                        expense_id,
                        date_text=edit_date.get(),
                        category=edit_category.get(),
                        amount=edit_amount.get(),
                        description=edit_description.get()
                    )

                    messagebox.showinfo(
                        "Success",
                        "Expense updated successfully!",
                        parent=edit_window
                    )

                    edit_window.destroy()

                    app.show_page("All Expenses")

                except ValueError as error:

                    show_error("Invalid Input", error)

                except Exception as error:

                    show_error("Edit Error", error)

            create_button(
                form,
                "Save Changes",
                save_changes
            ).pack(
                anchor="w",
                pady=20
            )

        except Exception as error:

            show_error("Error", error)

    create_button(
        buttons,
        "Edit Selected",
        edit_selected,
        BLUE
    ).pack(
        side="left",
        padx=5
    )

    create_button(
        buttons,
        "Delete Selected",
        delete_selected,
        RED
    ).pack(
        side="left",
        padx=5
    )


# -----------------------------------------
# MONTHLY ANALYTICS PAGE
# -----------------------------------------

def show_analytics(parent, app):

    create_heading(
        parent,
        "Monthly Analytics",
        "View category-wise spending and spending patterns."
    )

    month_frame = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    month_frame.pack(
        fill="x",
        pady=10
    )

    tk.Label(
        month_frame,
        text="Month (YYYY-MM):",
        bg=BACKGROUND,
        fg=TEXT
    ).pack(
        side="left",
        padx=5
    )

    month_entry = tk.Entry(
        month_frame,
        font=("Arial", 11)
    )

    month_entry.insert(
        0,
        fn.current_month()
    )

    month_entry.pack(
        side="left",
        padx=5
    )

    result_frame = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    result_frame.pack(
        fill="both",
        expand=True
    )

    def load_analytics():

        for widget in result_frame.winfo_children():
            widget.destroy()

        try:

            month = fn.validate_month(month_entry.get())

            # Backend calculations
            summary = fn.monthly_summary(month)

            highest = fn.highest_category(month)

            if not summary:

                tk.Label(
                    result_frame,
                    text="No expenses found for this month.",
                    bg=BACKGROUND,
                    fg=GREY,
                    font=("Arial", 12)
                ).pack(pady=30)

                return

            total = sum(summary.values())

            highest_text = (
                f"{highest[0]} - {format_money(highest[1])}"
                if highest else "None"
            )

            tk.Label(
                result_frame,
                text=f"Monthly Total: {format_money(total)}",
                bg=BACKGROUND,
                fg=TEXT,
                font=("Arial", 17, "bold")
            ).pack(
                anchor="w",
                pady=8
            )

            tk.Label(
                result_frame,
                text=f"Highest Spending Category: {highest_text}",
                bg=BACKGROUND,
                fg=ORANGE,
                font=("Arial", 12, "bold")
            ).pack(
                anchor="w",
                pady=5
            )

            chart_frame = tk.Frame(
                result_frame,
                bg=BACKGROUND
            )

            chart_frame.pack(
                fill="both",
                expand=True
            )

            colors = [
                BLUE,
                GREEN,
                ORANGE,
                RED,
                "#9875D5",
                "#20A6A6"
            ]

            # PIE CHART
            pie_frame = tk.Frame(
                chart_frame,
                bg=WHITE,
                padx=10,
                pady=10
            )

            pie_frame.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            tk.Label(
                pie_frame,
                text="Expense Distribution",
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 12, "bold")
            ).pack(anchor="w")

            pie = tk.Canvas(
                pie_frame,
                width=280,
                height=270,
                bg=WHITE,
                highlightthickness=0
            )

            pie.pack()

            start_angle = 0

            for index, (category, amount) in enumerate(summary.items()):

                extent = float(amount) / total * 360

                pie.create_arc(
                    30, 10, 250, 230,
                    start=start_angle,
                    extent=extent,
                    fill=colors[index % len(colors)],
                    outline=WHITE,
                    width=2
                )

                start_angle += extent

                tk.Label(
                    pie_frame,
                    text=f"{category}: {format_money(amount)}",
                    bg=WHITE,
                    fg=TEXT,
                    font=("Arial", 9)
                ).pack(anchor="w")

            # BAR CHART
            bar_frame = tk.Frame(
                chart_frame,
                bg=WHITE,
                padx=10,
                pady=10
            )

            bar_frame.pack(
                side="right",
                fill="both",
                expand=True,
                padx=5
            )

            tk.Label(
                bar_frame,
                text="Category-wise Spending",
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 12, "bold")
            ).pack(anchor="w")

            bar = tk.Canvas(
                bar_frame,
                width=350,
                height=320,
                bg=WHITE,
                highlightthickness=0
            )

            bar.pack()

            max_amount = max(summary.values())

            for index, (category, amount) in enumerate(summary.items()):

                y = 20 + index * 45

                bar_width = float(amount) / max_amount * 160

                bar.create_text(
                    5,
                    y + 10,
                    text=category,
                    anchor="w",
                    fill=TEXT
                )

                bar.create_rectangle(
                    105,
                    y,
                    105 + bar_width,
                    y + 22,
                    fill=colors[index % len(colors)],
                    outline=""
                )

                bar.create_text(
                    115 + bar_width,
                    y + 10,
                    text=f"₹{amount:,.0f}",
                    anchor="w",
                    fill=TEXT
                )

        except ValueError as error:

            show_error("Invalid Month", error)

        except Exception as error:

            show_error("Analytics Error", error)

    create_button(
        month_frame,
        "Generate Report",
        load_analytics
    ).pack(
        side="left",
        padx=10
    )

    load_analytics()


# -----------------------------------------
# BUDGET MANAGEMENT PAGE
# -----------------------------------------

def show_budget(parent, app):

    create_heading(
        parent,
        "Budget Management",
        "Set your monthly spending limit and monitor expenses."
    )

    budget_frame = tk.Frame(
        parent,
        bg=WHITE,
        padx=25,
        pady=25
    )

    budget_frame.pack(
        fill="x",
        pady=10
    )

    current_budget = fn.get_budget()

    budget_entry = create_field(
        budget_frame,
        "Monthly Budget Limit (₹)",
        str(current_budget) if current_budget > 0 else ""
    )

    def save_budget():

        try:

            limit = fn.set_budget(
                budget_entry.get()
            )

            messagebox.showinfo(
                "Success",
                f"Budget saved: {format_money(limit)}"
            )

            app.show_page("Budget Management")

        except ValueError as error:

            show_error("Invalid Budget", error)

        except Exception as error:

            show_error("Budget Error", error)

    create_button(
        budget_frame,
        "Save Monthly Budget",
        save_budget
    ).pack(
        anchor="w",
        pady=15
    )

    # CURRENT MONTH BUDGET STATUS
    month = fn.current_month()

    status = fn.check_budget(month)

    limit = status["limit"]
    total = status["total"]

    tk.Label(
        parent,
        text=f"Budget Status - {month}",
        bg=BACKGROUND,
        fg=TEXT,
        font=("Arial", 15, "bold")
    ).pack(
        anchor="w",
        pady=15
    )

    tk.Label(
        parent,
        text=f"Budget Limit: {format_money(limit)}",
        bg=BACKGROUND,
        fg=TEXT,
        font=("Arial", 12)
    ).pack(anchor="w")

    tk.Label(
        parent,
        text=f"Total Spent: {format_money(total)}",
        bg=BACKGROUND,
        fg=TEXT,
        font=("Arial", 12)
    ).pack(anchor="w", pady=5)

    if limit > 0:

        percentage = total / limit * 100

        progress = ttk.Progressbar(
            parent,
            maximum=100,
            value=min(percentage, 100)
        )

        progress.pack(
            fill="x",
            pady=15
        )

        if status["exceeded"]:

            tk.Label(
                parent,
                text=status["message"],
                bg="#FDE8E8",
                fg=RED,
                font=("Arial", 10, "bold"),
                padx=12,
                pady=10,
                wraplength=650,
                justify="left"
            ).pack(fill="x")

        else:

            tk.Label(
                parent,
                text=f"{percentage:.1f}% used | "
                     f"{format_money(-status['difference'])} remaining",
                bg=BACKGROUND,
                fg=GREEN,
                font=("Arial", 12, "bold")
            ).pack(anchor="w")

    else:

        tk.Label(
            parent,
            text="No budget limit has been set.",
            bg=BACKGROUND,
            fg=ORANGE,
            font=("Arial", 11)
        ).pack(anchor="w", pady=10)


# -----------------------------------------
# SEARCH EXPENSES PAGE
# -----------------------------------------

def show_search(parent, app):

    create_heading(
        parent,
        "Search Expenses",
        "Find transactions by category or date range."
    )

    search_frame = tk.Frame(
        parent,
        bg=WHITE,
        padx=20,
        pady=20
    )

    search_frame.pack(
        fill="x",
        pady=10
    )

    tk.Label(
        search_frame,
        text="Start Date (YYYY-MM-DD)",
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=0,
        column=0,
        padx=8,
        sticky="w"
    )

    start_entry = tk.Entry(
        search_frame,
        font=("Arial", 10)
    )

    start_entry.grid(
        row=1,
        column=0,
        padx=8,
        pady=8,
        ipady=6
    )

    tk.Label(
        search_frame,
        text="End Date (YYYY-MM-DD)",
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=0,
        column=1,
        padx=8,
        sticky="w"
    )

    end_entry = tk.Entry(
        search_frame,
        font=("Arial", 10)
    )

    end_entry.grid(
        row=1,
        column=1,
        padx=8,
        pady=8,
        ipady=6
    )

    tk.Label(
        search_frame,
        text="Category",
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=0,
        column=2,
        padx=8,
        sticky="w"
    )

    category = ttk.Combobox(
        search_frame,
        values=["All"] + fn.CATEGORIES,
        state="readonly",
        font=("Arial", 10)
    )

    category.set("All")

    category.grid(
        row=1,
        column=2,
        padx=8,
        pady=8
    )

    result_frame = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    result_frame.pack(
        fill="both",
        expand=True
    )

    def perform_search():

        for widget in result_frame.winfo_children():
            widget.destroy()

        start = start_entry.get().strip()
        end = end_entry.get().strip()

        selected_category = category.get()

        try:

            # Both dates are required together
            if bool(start) != bool(end):

                messagebox.showerror(
                    "Date Range",
                    "Please enter both start and end dates."
                )

                return

            # Search by date range
            if start and end:

                start = fn.validate_date(start)
                end = fn.validate_date(end)

                records = fn.search_by_date_range(
                    start,
                    end
                )

            # Search by category
            elif selected_category != "All":

                records = fn.search_by_category(
                    selected_category
                )

            # No filters
            else:

                records = fn.get_all_expenses()

            # Apply category filter along with date filter
            if selected_category != "All":

                records = [
                    expense
                    for expense in records
                    if expense["category"].lower()
                    == selected_category.lower()
                ]

            if records:

                create_table(
                    result_frame,
                    records,
                    height=10
                )

            else:

                tk.Label(
                    result_frame,
                    text="No matching expenses found.",
                    bg=BACKGROUND,
                    fg=GREY,
                    font=("Arial", 12)
                ).pack(pady=25)

        except ValueError as error:

            show_error("Invalid Search", error)

        except Exception as error:

            show_error("Search Error", error)

    create_button(
        search_frame,
        "Search",
        perform_search
    ).grid(
        row=1,
        column=3,
        padx=10
    )
