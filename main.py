
import tkinter as tk
from gui.dashboard import Dashboard


root = tk.Tk()

root.title("Smart Expense Tracker")
root.geometry("1200x750")
root.minsize(1000, 650)

root.configure(bg="#F4F6FA")

app = Dashboard(root)

root.mainloop()
