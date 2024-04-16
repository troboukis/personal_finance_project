import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from app import *
from tkinter import messagebox

class IncomeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.incomes = []
        self.init_ui()
        self.update_table()

    def init_ui(self):
        self.indb = Income(new_db)
        self.frequency_options = [i[1] for i in self.indb.showData('frequency_table')]
        self.category_options = [i[1] for i in self.indb.showData('category_table')]

        self.grid_columnconfigure(0, minsize=100)  # Smaller fixed minimum size for column 1
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
                background=[('selected', '#0078D7')],
                foreground=[('selected', 'white')])
        treeStyle.configure("Treeview.Heading", 
                font=("Courier", 13, 'italic'), 
                background="#D3D3D3", 
                foreground="black")
        treeStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Define StringVars
        self.income_description = tk.StringVar()
        self.income_amount = tk.StringVar()
        self.income_category = tk.StringVar()
        self.income_date = tk.StringVar()
        self.frequency = tk.StringVar()

        # UI Components
        tk.Label(self, text="Καταχώρηση εσόδων:", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        tk.Label(self, text="Περιγραφή:", font=("Helvetica", 20)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        tk.Entry(self, textvariable=self.income_description, font=("Courier", 20)).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        tk.Label(self, text="Ποσό:", font=("Helvetica", 20)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        tk.Entry(self, textvariable=self.income_amount, font=("Courier", 20)).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        tk.Label(self, text="Κατηγορία:", font=("Helvetica", 20)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        ttk.Combobox(self, textvariable=self.income_category, font=("Courier", 20), values=self.category_options).grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        tk.Label(self, text="Ημερομηνία (dd-mm-yyyy):", font=("Helvetica", 20)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        
        tk.Entry(self, textvariable=self.income_date, font=("Courier", 20)).grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        
        ttk.Combobox(self, textvariable=self.frequency, font=("Courier", 20), values=self.frequency_options).grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Button(self, text="Πρόσθεσε έσοδο", command=self.add_income).grid(row=6, column=0, columnspan=2, pady=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=('Date', 'Description', 'Amount', 'Frequency', 'Category'), show='headings')
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
            amount = float(self.income_amount.get())  # Try converting amount to float
            return amount
        except ValueError:
            messagebox.showerror("Σφάλμα", "Έχετε εισάγει μη έγκυρο ποσό.")
            self.delete_last_entry()
            return None  # Or handle it some other way

    def add_income(self):
        income_data = {
            'Description': self.income_description.get(),
            'Amount': self.correct_amount(),
            'Category': self.income_category.get(),
            'Date': self.income_date.get(),
            'Frequency': self.frequency.get()
        }
        category_id = return_index(income_data['Category'], self.indb.showData('category_table'))
        frequency_id = return_index(income_data['Frequency'], self.indb.showData('frequency_table'))
        print(f"category_id = {category_id}")
        self.incomes.append(income_data)  # Add to the list of entries
        self.update_table()  # Update the table view
        self.indb.InsertIncome(
            income_data['Description'], 
            income_data['Amount'], 
            category_id, 
            income_data['Date'], 
            frequency_id)

    def update_table(self):
        # Clear the current contents of the table
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Insert new data
        # for exp in self.incomes:
        #     self.tree.insert('', 'end', values=(exp['Description'], exp['Amount'], exp['Category'], exp['Date'], exp['Frequency']))
        # Fetch new data from the database
        income_entries = self.indb.showData('income')
        for entry in income_entries:
            print(entry)
            self.tree.insert('', 'end', values=entry[1:])
    
    def delete_last_entry(self):
        print(self.tree.get_children())
        # for i in self.tree.get_children():
        #     self.tree.delete(i)