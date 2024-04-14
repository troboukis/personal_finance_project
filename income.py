import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from app import *

class IncomeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.incomes = []
        self.init_ui()

    def init_ui(self):
        # Configure the style for the Treeview
        style = ttk.Style(self)
        treeStyle = ttk.Style(self)
        treeStyle.theme_use("default")
        treeStyle.configure("Treeview", 
                background="white", 
                foreground="black", 
                rowheight=5, 
                fieldbackground="white")
        treeStyle.map("Treeview", 
                background=[('selected', '#0078D7')],  # Change selection color here
                foreground=[('selected', 'white')])
        # Styling for the Treeview heading
        treeStyle.configure("Treeview.Heading", 
                font=("Helvetica", 13, 'italic'), 
                background="#D3D3D3", 
                foreground="black")
        treeStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        
        # Setting 'gridlines' to 'both' to display grid lines in the Treeview
        treeStyle.configure("Treeview", gridlines="both", borderwidth=1)

        # Define StringVars
        self.income_description = tk.StringVar()
        self.income_amount = tk.StringVar()
        self.income_category = tk.StringVar()
        self.income_date = tk.StringVar()
        self.frequency = tk.StringVar()

        tk.Label(self, text="Καταχώρηση εσόδων:", font=("Helvetica", 30)).grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        # Περιγραφή εσόδου
        tk.Label(self, text="Περιγραφή:", font=("Helvetica", 20)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.income_description, font=("Courier", 20)).grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Ποσό
        tk.Label(self, text="Ποσό:", font=("Helvetica", 20)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.income_amount, font=("Courier", 20)).grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Κατηγορία
        tk.Label(self, text="Κατηγορία:", font=("Helvetica", 20)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        ttk.Combobox(self, textvariable=self.income_category, font=("Courier", 20), values=["Food", "Transport", "Housing"]).grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Ημερομηνία
        tk.Label(self, text="Ημερομηνία (dd-mm-yyyy):", font=("Helvetica", 20)).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.income_date, font=("Courier", 20)).grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Συχνότητα
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.frequency, font=("Courier", 20)).grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        # Submit Button
        ttk.Button(self, text="Πρόσθεσε έσοδο", style='info.TButton', command=self.add_income).grid(row=7, column=0, columnspan=2, pady=20)

         # # Vertical Separator
        ttk.Separator(self, orient='vertical').grid(row=2, column=2, rowspan=6, sticky='ns')

        # income Table
        self.tree = ttk.Treeview(self, columns=('Description', 'Amount', 'Category', 'Date', 'Frequency'), show='headings')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Frequency', text='Frequency')
        self.tree.grid(row=2, column=3, rowspan=6, padx=10, pady=10, sticky='nsew')
        self.grid_columnconfigure(3, weight=1)  # Allows the table to expand
        self.grid_rowconfigure(2, weight=1)     # Distributes extra vertical space to the treeview

    def get_income_details(self):
        try:
            self.income_amount = float(self.income_amount.get())  # Try converting amount to float
        except ValueError:
            print("Invalid amount entered. Please enter a numeric value.")
            return None  # Or handle it some other way

        return {
            'description': self.income_description.get(),
            'amount': self.income_amount,
            'category': self.income_category.get(), 
            'date': self.income_date.get(),
            'frequency': self.frequency.get() 
        }

    def add_income(self):
        indb = Income(new_db)
        categories = indb.showData('category_table', dataframe=False)
        income_data = {
            'Description': self.income_description.get(),
            'Amount': self.income_amount.get(),
            'Category': self.income_category.get(),
            'Date': self.income_date.get(),
            'Frequency': self.frequency.get()
        }
        self.incomes.append(income_data)  # Add to the list of entries
        self.update_table()  # Update the table view
        indb.InsertIncome(
            income_data['Description'], 
            income_data['Amount'], 
            return_category_index(income_data['Category'], categories), 
            income_data['Date'], 
            0)


    def update_table(self):
        # Clear the current contents of the table
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Insert new data
        for exp in self.incomes:
            self.tree.insert('', 'end', values=(exp['Description'], exp['Amount'], exp['Category'], exp['Date'], exp['Frequency']))