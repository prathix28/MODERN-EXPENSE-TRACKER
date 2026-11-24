
import tkinter as tk
from tkinter import ttk


# COLOUR SETTINGS

NAVY = "#1E2A44"
NAVY_LIGHT = "#344767"
BACKGROUND = "#F4F6FA"
WHITE = "#FFFFFF"
TEXT = "#25324A"
GREY = "#788397"
BLUE = "#4776E6"
GREEN = "#16A36A"
ORANGE = "#F0A43A"
RED = "#E05252"


# PAGE HEADING

def create_heading(parent, title, subtitle=""):

    tk.Label(
        parent,
        text=title,
        bg=BACKGROUND,
        fg=TEXT,
        font=("Arial", 19, "bold")
    ).pack(anchor="w")

    if subtitle:
        tk.Label(
            parent,
            text=subtitle,
            bg=BACKGROUND,
            fg=GREY,
            font=("Arial", 10)
        ).pack(anchor="w", pady=(5, 15))


# SUMMARY CARD

def create_card(parent, title, value, color=BLUE):

    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=18,
        pady=18,
        highlightbackground="#E5E9F0",
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        bg=WHITE,
        fg=GREY,
        font=("Arial", 10)
    ).pack(anchor="w")

    tk.Label(
        card,
        text=value,
        bg=WHITE,
        fg=color,
        font=("Arial", 20, "bold")
    ).pack(anchor="w", pady=12)

    return card


# INPUT FIELD

def create_field(parent, label, default=""):

    frame = tk.Frame(parent, bg=WHITE)
    frame.pack(fill="x", pady=8)

    tk.Label(
        frame,
        text=label,
        bg=WHITE,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    entry = tk.Entry(
        frame,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    entry.pack(fill="x", ipady=8)

    if default:
        entry.insert(0, default)

    return entry


# BUTTON

def create_button(parent, text, command, color=BLUE):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=NAVY_LIGHT,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        cursor="hand2"
    )


# TRANSACTION TABLE

def create_table(parent, records=None, height=8):

    frame = tk.Frame(parent, bg=WHITE)

    columns = (
        "ID",
        "Date",
        "Category",
        "Description",
        "Amount"
    )

    style = ttk.Style()

    style.configure(
        "Treeview",
        rowheight=34,
        font=("Arial", 10),
        background=WHITE,
        foreground=TEXT,
        fieldbackground=WHITE
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold")
    )

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=height
    )

    widths = {
        "ID": 50,
        "Date": 120,
        "Category": 130,
        "Description": 220,
        "Amount": 120
    }

    for column in columns:

        table.heading(column, text=column)

        table.column(
            column,
            width=widths[column],
            anchor="center"
        )

    if records:

        for record in records:

            table.insert(
                "",
                "end",
                iid=str(record["id"]),
                values=(
                    record["id"],
                    record["date"],
                    record["category"],
                    record["description"],
                    f"₹{float(record ['amount']):,.2f}"
                )
            )

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    frame.pack(
        fill="both",
        expand=True
    )

    return table
