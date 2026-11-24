
import tkinter as tk

from gui.components import (
    NAVY,
    NAVY_LIGHT,
    BACKGROUND,
    WHITE,
    TEXT,
    GREY
)

from gui.pages import (
    show_dashboard,
    show_add_expense,
    show_all_expenses,
    show_analytics,
    show_budget,
    show_search
)


class Dashboard:

    def __init__(self, root):

        self.root = root

        self.create_sidebar()
        self.create_main_area()

        self.show_page("Dashboard")


    # SIDEBAR

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=NAVY,
            width=225
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="◆ SMART EXPENSE",
            bg=NAVY,
            fg=WHITE,
            font=("Arial", 16, "bold")
        ).pack(pady=30)

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            bg=NAVY,
            fg="#9DAAC0",
            font=("Arial", 9, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=10
        )

        menu_items = [
            ("▦", "Dashboard"),
            ("＋", "Add Expense"),
            ("▤", "All Expenses"),
            ("◉", "Monthly Analytics"),
            ("▣", "Budget Management"),
            ("⌕", "Search Expenses")
        ]

        self.nav_buttons = {}

        for icon, name in menu_items:

            button = tk.Button(
                self.sidebar,
                text=f"  {icon}    {name}",
                font=("Arial", 11),
                bg=NAVY,
                fg=WHITE,
                activebackground=NAVY_LIGHT,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                anchor="w",
                padx=15,
                pady=14,
                cursor="hand2",
                command=lambda page=name: self.show_page(page)
            )

            button.pack(
                fill="x",
                padx=10,
                pady=3
            )

            self.nav_buttons[name] = button


    # MAIN CONTENT AREA

    def create_main_area(self):

        self.main_area = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Header
        self.header = tk.Frame(
            self.main_area,
            bg=WHITE,
            height=75
        )

        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.page_title = tk.Label(
            self.header,
            text="Dashboard",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 20, "bold")
        )

        self.page_title.pack(
            side="left",
            padx=30,
            pady=20
        )

        tk.Label(
            self.header,
            text="Personal Finance Manager",
            bg=WHITE,
            fg=GREY,
            font=("Arial", 10)
        ).pack(
            side="right",
            padx=30
        )

        # Page container
        self.content = tk.Frame(
            self.main_area,
            bg=BACKGROUND
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )


    # NAVIGATION

    def show_page(self, page):

        self.page_title.config(text=page)

        for name, button in self.nav_buttons.items():

            if name == page:
                button.config(bg=NAVY_LIGHT)
            else:
                button.config(bg=NAVY)

        # Clear old screen
        for widget in self.content.winfo_children():
            widget.destroy()

        # Page mapping
        pages = {
            "Dashboard": show_dashboard,
            "Add Expense": show_add_expense,
            "All Expenses": show_all_expenses,
            "Monthly Analytics": show_analytics,
            "Budget Management": show_budget,
            "Search Expenses": show_search
        }

        selected_page = pages.get(page)

        if selected_page:
            selected_page(self.content, self)
