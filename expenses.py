# expenses.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class ExpensesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        # Define StringVars
        self.expense_amount = tk.StringVar()
        self.expense_category = tk.StringVar()
        self.expense_date = tk.StringVar()

        # Amount Entry
        tk.Label(self, text="Ποσό:", font=("Helvetica", 20)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.expense_amount, font=("Helvetica", 20)).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Category Combobox
        tk.Label(self, text="Category:", font=("Helvetica", 20)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Combobox(self, textvariable=self.expense_category, font=("Helvetica", 20), values=["Food", "Transport", "Housing"]).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Date Entry
        tk.Label(self, text="Date (dd-mm-yyyy):", font=("Helvetica", 20)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.expense_date, font=("Helvetica", 20)).grid(row=2, column=1, padx=10, pady=10, sticky="ew")


        # Submit Button
        ttk.Button(self, text="Add Expense", style='info.TButton', command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=20)

    def add_expense(self):
        amount = self.expense_amount.get()
        category = self.expense_category.get()
        date = self.expense_date.get()
        # Add logic to store the expense
        print(f"Added expense: Amount={amount}, Category={category}, Date={date}")
