import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from app import Expenses, new_db



class ExpensesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.expenses = []
        self.init_ui()

    def init_ui(self):
        # self.exdb = Expenses(new_db)
        # self.frequency_options = [i[1] for i in self.indb.showData('frequency_table')]
        # self.category_options = [i[1] for i in self.indb.showData('category_table')]

        # Configure the style for the Treeview
        treeStyle = ttk.Style(self)
        treeStyle.theme_use("default")
        treeStyle.configure("Treeview", 
                background="white", 
                foreground="black", 
                rowheight=25, 
                fieldbackground="white")
        treeStyle.map("Treeview", 
                background=[('selected', '#0078D7')],  # Change selection color here
                foreground=[('selected', 'white')])
        # Styling for the Treeview heading
        treeStyle.configure("Treeview.Heading", 
                font=("Courier", 13, 'italic'), 
                background="#D3D3D3", 
                foreground="black")
        treeStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        
        # Setting 'gridlines' to 'both' to display grid lines in the Treeview
        treeStyle.configure("Treeview", gridlines="both", borderwidth=1)

        # Define StringVars
        self.expense_description = tk.StringVar()
        self.expense_amount = tk.StringVar()
        self.expense_category = tk.StringVar()
        self.expense_date = tk.StringVar()
        self.frequency = tk.StringVar()

        tk.Label(self, text="Καταχώρηση εξόδων:", font=("Helvetica", 30)).grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        
        # Περιγραφή εξόδου
        
        tk.Label(self, text="Περιγραφή:", font=("Helvetica", 20)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        tk.Entry(self, textvariable=self.expense_description, font=("Courier", 20)).grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Vertical Separator
        ttk.Separator(self, orient='vertical').grid(row=2, column=2, rowspan=6, sticky='ns')

        # Ποσό
        tk.Label(self, text="Ποσό:", font=("Helvetica", 20)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        tk.Entry(self, textvariable=self.expense_amount, font=("Courier", 20)).grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Κατηγορία
        tk.Label(self, text="Κατηγορία:", font=("Helvetica", 20)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        ttk.Combobox(self, textvariable=self.expense_category, font=("Courier", 20), values=["Food", "Transport", "Housing"]).grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Ημερομηνία
        tk.Label(self, text="Ημερομηνία (dd-mm-yyyy):", font=("Helvetica", 20)).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.expense_date, font=("Courier", 20)).grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Συχνότητα
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.frequency, font=("Courier", 20)).grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        # Submit Button
        ttk.Button(self, text="Πρόσθεσε έξοδο", style='info.TButton', command=self.add_expense).grid(row=7, column=0, columnspan=2, pady=20)

        # Expenses Table
        self.tree = ttk.Treeview(self, columns=('Description', 'Amount', 'Category', 'Date', 'Frequency'), show='headings')
        self.tree.heading('Description', text='Περιγραφή')
        self.tree.heading('Amount', text='Ποσό σε ευρώ')
        self.tree.heading('Category', text='Κατηγορία')
        self.tree.heading('Date', text='Ημερομηνία')
        self.tree.heading('Frequency', text='Συχνότητα')
        self.tree.grid(row=2, column=3, rowspan=6, padx=10, pady=10, sticky='nsew')
        self.grid_columnconfigure(3, weight=1)  # Allows the table to expand
        self.grid_rowconfigure(2, weight=1)     # Distributes extra vertical space to the treeview

    def correct_amount(self):
        try:
            amount = float(self.expense_amount.get())  # Try converting amount to float
            return amount
        except ValueError:
            messagebox.showerror("Σφάλμα", "Έχετε εισάγει μη έγκυρο ποσό.")
            self.delete_last_entry()
            return None  # Or handle it some other way
        
    def add_expense(self):
        expense_data = {
            'Description': self.expense_description.get(),
            'Amount': self.expense_amount.get(),
            'Category': self.expense_category.get(),
            'Date': self.expense_date.get(),
            'Frequency': self.frequency.get()
        }
        self.expenses.append(expense_data)  # Add to the list of entries
        self.update_table()  # Update the table view

    def update_table(self):
        # Clear the current contents of the table
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Insert new data
        for exp in self.expenses:
            self.tree.insert('', 'end', values=(exp['Description'], exp['Amount'], exp['Category'], exp['Date'], exp['Frequency']))