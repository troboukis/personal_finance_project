import tkinter as tk
from tkinter import ttk
from app import *
from tkinter import messagebox
import datetime

def current_date(show_full_date = False):
    # Return the current date as a string
    if show_full_date:
        return datetime.datetime.now().strftime("%b %d %Y, %H:%M")
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d")

class IncomeExpensesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.incomes = []
        self.expenses = []

        # Variables to track checkbutton states
        self.show_income = tk.BooleanVar(value=False)
        self.show_expenses = tk.BooleanVar(value=False)

        self.init_ui()
        self.update_table()


    def init_ui(self):
        self.indb = Income(new_db)
        self.frequency_options = [i[1] for i in self.indb.showData('frequency_table')]
        self.category_options = [i[1] for i in self.indb.showData('category_table')]

        self.grid_columnconfigure(0, minsize=200)  # Smaller fixed minimum size for column 1
        self.grid_columnconfigure(1, minsize=100)  # Smaller fixed minimum size for column 2
        self.grid_columnconfigure(2, weight=1)

        # Configure the style for the Treeview
        treeStyle = ttk.Style(self)
        treeStyle.theme_use("default")
        treeStyle.configure("Treeview", 
                background="white", 
                foreground="black", 
                rowheight=25,  # Adjusted row height
                fieldbackground="white")
        
        treeStyle.map("Treeview", 
                background=[('selected', '#dadada')],
                foreground=[('selected', 'white')])
        
        treeStyle.configure("Treeview.Heading", 
                font=("Courier", 13, 'italic'), 
                background="#D3D3D3", 
                foreground="black")
        
        treeStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Define StringVars
        self.description = tk.StringVar()
        self.amount = tk.StringVar()
        self.category = tk.StringVar()
        self.category.set(self.category_options[-1])
        
        self.date = tk.StringVar()
        self.date.set(current_date())

        self.frequency = tk.StringVar()
        self.frequency.set(self.frequency_options[2])
        

        # UI Components
        self.tree = ttk.Treeview(self, columns=('Date', 'Description', 'Amount', 'Frequency', 'Category'), show='headings')

        # --------------------------------ΕΣΟΔΑ - ΕΞΟΔΑ ΚΟΥΜΠΙΑ--------------------
        # tk.Label(self, text="Καταχώρηση εσόδων:", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        income_cb = tk.Checkbutton(self, text='Έσοδα', font=("Helvetica", 16),
                                   variable=self.show_income, onvalue=True, offvalue=False,
                                   command= self.toggle_expenses_off)
        income_cb.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        income_cb.select()

        # Checkbutton for showing expenses
        expenses_cb = tk.Checkbutton(self, text='Έξοδα', font=("Helvetica", 16),
                                     variable=self.show_expenses, onvalue=True, offvalue=False,
                                     command=self.toggle_income_off)
        expenses_cb.grid(row=1, column=1, padx=10, pady=10, sticky="w")
       
        # --------------------------------ΠΕΡΙΓΡΑΦΗ-----------------------
        tk.Label(self, text="Περιγραφή:", font=("Helvetica", 20)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.description, font=("Courier", 20)).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # --------------------------------ΠΟΣΟ----------------------------
        tk.Label(self, text="Ποσό:", font=("Helvetica", 20)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.amount, font=("Courier", 20)).grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # --------------------------------ΚΑΤΗΓΟΡΙΑ-----------------------
        tk.Label(self, text="Κατηγορία:", font=("Helvetica", 20)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        ttk.Combobox(self, textvariable=self.category, font=("Courier", 20), values=self.category_options).grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        # --------------------------------ΗΜΕΡΟΜΗΝΙΑ-----------------------
        tk.Label(self, text="Ημερομηνία (dd-mm-yyyy):", font=("Helvetica", 20)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.date, font=("Courier", 20)).grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        # --------------------------------ΣΥΧΝΟΤΗΤΑ------------------------
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        ttk.Combobox(self, textvariable=self.frequency, font=("Courier", 20), values=self.frequency_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        
        # --------------------------------ΚΟΥΜΠΙ ΠΡΟΣΘΕΣΕ ΕΣΟΔΟ------------------------------
        style = ttk.Style(self)
        style.configure('success.TButton', font=('Helvetica', 16), background='green', foreground='white')
        self.action_button = ttk.Button(self, style='success.TButton')
        self.action_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        
        #---------------------------------------Treeview---------------------------------------
        self.tree.heading('Date', text='Ημερομηνία')
        self.tree.heading('Description', text='Περιγραφή')
        self.tree.heading('Amount', text='Ποσό σε ευρώ')
        self.tree.heading('Category', text='Κατηγορία')
        self.tree.heading('Frequency', text='Συχνότητα')

        # Centering column text
        self.tree.column('Description', anchor='center', width=250)
        self.tree.column('Amount', anchor='center', width=140)
        self.tree.column('Category', anchor='center', width=180)
        self.tree.column('Date', anchor='center', width=140)
        self.tree.column('Frequency', anchor='center', width=100)

        self.tree.grid(row=1, column=2, rowspan=6, padx=10, pady=10, sticky='nsew')

        # Scrollbars for Treeview
        vscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hscroll = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
        vscroll.grid(row=1, column=3, rowspan=6, sticky='ns')
        hscroll.grid(row=7, column=2, sticky='ew')

        # Grid configuration for resizing
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(1, weight=1)



    def correct_amount(self):
        try:
            amount = float(self.amount.get())  # Try converting amount to float
            return amount
        except ValueError:
            messagebox.showerror("Σφάλμα", "Έχετε εισάγει μη έγκυρο ποσό.")
            self.delete_last_entry()
            return None  # Or handle it some other way

    def add_income(self):
        income_data = {
            'Description': self.description.get(),
            'Amount': self.correct_amount(),
            'Category': self.category.get(),
            'Date': self.date.get(),
            'Frequency': self.frequency.get()
        }
        category_id = return_index(income_data['Category'], self.indb.showData('category_table'))
        frequency_id = return_index(income_data['Frequency'], self.indb.showData('frequency_table'))
        print(f"category_id = {category_id}")
        self.incomes.append(income_data)  # Add to the list of entries
        
        self.indb.InsertIncome(
            income_data['Description'], 
            income_data['Amount'], 
            category_id, 
            income_data['Date'], 
            frequency_id)
        self.update_table()  # Update the table view

    def add_expense(self):
        expense_data = {
            'Description': self.description.get(),
            'Amount': self.correct_amount(),
            'Category': self.category.get(),
            'Date': self.date.get(),
            'Frequency': self.frequency.get()
        }
        category_id = return_index(expense_data['Category'], self.indb.showData('category_table'))
        frequency_id = return_index(expense_data['Frequency'], self.indb.showData('frequency_table'))
        print(f"category_id = {category_id}")
        self.expenses.append(expense_data)  # Add to the list of entries
        
        self.indb.InsertExpense(
            expense_data['Description'], 
            expense_data['Amount'], 
            category_id, 
            expense_data['Date'], 
            frequency_id)
        self.update_table()  # Update the table view

    def update_table(self):
        # Clear the current contents of the table
        for i in self.tree.get_children():
            self.tree.delete(i)

        if self.show_income.get():
            self.action_button.config(text="Πρόσθεσε έσοδο", command=self.add_income)
            income_entries = self.indb.printData("income")
            for entry in income_entries:
                self.tree.insert('', 'end', values=(entry[1], entry[2], entry[3], entry[7], entry[9]))

        elif self.show_expenses.get():
            self.action_button.config(text="Πρόσθεσε έξοδο", command=self.add_expense)
            expense_entries = self.indb.printData("expenses")
            for entry in expense_entries:
                self.tree.insert('', 'end', values=(entry[1], entry[2], entry[3], entry[7], entry[9]))
        else:
            self.action_button.config(text="Καμία ενέργεια", command=lambda: None)
    
    def delete_last_entry(self):
        print(self.tree.get_children())
        # for i in self.tree.get_children():
        #     self.tree.delete(i)

    def toggle_expenses_off(self):
        # This method is called when the income checkbox is clicked
        if self.show_income.get() == True:
            self.show_expenses.set(False)  # Uncheck expenses
        self.update_table()

    def toggle_income_off(self):
        # This method is called when the expenses checkbox is clicked
        if self.show_expenses.get() == True:
            self.show_income.set(False)  # Uncheck income
        self.update_table()
