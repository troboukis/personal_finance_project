import tkinter as tk
from tkinter import ttk
import ttkbootstrap as bttk
from app import *
from tkinter import messagebox
import datetime
from tkinter import PhotoImage, Menu
from tkinter.filedialog import asksaveasfilename
from openpyxl.workbook import Workbook
from charts import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CalendarFinance import *

class IncomeExpensesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


        self.last_item = None  # Attribute to store the ID of the last clicked item

        self.incomes = []
        self.expenses = []

        # Variables to track checkbutton states
        self.show_income = tk.BooleanVar(value=False)
        self.show_expenses = tk.BooleanVar(value=False)

        self.canvas = None

        self.init_ui()
        self.update_table()
    
    def open_calendar(self):
        CalendarPopup(self, self.date)

    def init_ui(self):
        self.indb = Income(new_db)
        self.db = DatabaseConnection(new_db)
        

        self.frequency_options = [i[1] for i in self.indb.showData('frequency_table')]
        self.income_category_options = [i[1] for i in self.indb.showData('category_table') if i[2] == 1]
        self.expense_category_options = [i[1] for i in self.indb.showData('category_table') if i[2] == 0]

        self.grid_columnconfigure(0, minsize=100)  # Smaller fixed minimum size for column 1
        self.grid_columnconfigure(1, minsize=200)  # Smaller fixed minimum size for column 2
        self.grid_columnconfigure(2, minsize=300)

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
        self.category.set(self.income_category_options[-1])

        self.date = tk.StringVar()
        self.date.set(current_date())

        self.frequency = tk.StringVar()
        self.frequency.set(self.frequency_options[2])

        # UI Components
        self.tree = ttk.Treeview(self, columns=('Date', 'Description', 'Amount', 'Frequency', 'Category'),
                                 show='headings')

        # --------------------------------ΕΣΟΔΑ - ΕΞΟΔΑ ΚΟΥΜΠΙΑ--------------------
        # tk.Label(self, text="Καταχώρηση εσόδων:", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.income_cb = tk.Checkbutton(self, text='Έσοδα', font=("Helvetica", 16),
                                        variable=self.show_income, onvalue=True, offvalue=False,
                                        command=self.toggle_expenses_off)
        self.income_cb.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.income_cb.select()

        # Checkbutton for showing expenses
        self.expenses_cb = tk.Checkbutton(self, text='Έξοδα', font=("Helvetica", 16),
                                          variable=self.show_expenses, onvalue=True, offvalue=False,
                                          command=self.toggle_income_off)
        self.expenses_cb.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # --------------------------------ΚΟΥΜΠΙ SETTINGS---------------------------
        self.settings_button = ttk.Menubutton(self, text='⚙️ Μενού επιλογών', direction='below')
        self.settings_button.grid(row=0, column=1, sticky='e')
        # self.settings_button.place(x=300, y=30)

        # Create the dropdown menu
        self.settings_menu = Menu(self.settings_button, tearoff=0)
        self.settings_button['menu'] = self.settings_menu

        self.settings_menu.add_command(label="Εισαγωγή κατηγορίας", command=self.UserAddCategory)
        self.settings_menu.add_command(label="Διαγραφή κατηγορίας", command=self.UserDeleteCategory)
        self.settings_menu.add_command(label="Εξαγωγή σε excel", command=self.export_to_excel)

        # --------------------------------ΕΠΙΣΤΡΟΦΗ ΑΡΧΙΚΗ ΣΕΛΙΔΑ----------------------
        # sto main.py

        # --------------------------------ΚΟΥΜΠΙ ΔΙΑΓΡΑΦΗ---------------------------
        # Configure the delete button
        self.delete_button = ttk.Button(self, text='🗑', style='danger.TButton', command=self.delete_selection)
        self.delete_button.grid(row=9, column=1, pady=10, sticky="nsew")  # Adjust grid parameters as needed

        self.delete_button.grid_remove()  # Start with the button hidden

        # Style for the delete button
        style = ttk.Style(self)
        style.configure('danger.TButton', font=('Helvetica', 16), background='red', foreground='white')

        # --------------------------------ΠΕΡΙΓΡΑΦΗ-----------------------
        tk.Label(self, text="Περιγραφή:", font=("Helvetica", 20)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.description, font=("Courier", 20)).grid(row=4, column=1, padx=10, pady=5,
                                                                                 sticky="ew")

        # --------------------------------ΠΟΣΟ----------------------------
        tk.Label(self, text="Ποσό:", font=("Helvetica", 20)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.amount, font=("Courier", 20)).grid(row=5, column=1, padx=10, pady=5,
                                                                            sticky="ew")

        # --------------------------------ΚΑΤΗΓΟΡΙΑ-----------------------
        tk.Label(self, text="Κατηγορία:", font=("Helvetica", 20)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        if self.show_income.get():
            ttk.Combobox(self, textvariable=self.category, font=("Courier", 20),
                         values=self.income_category_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        else:
            ttk.Combobox(self, textvariable=self.category, font=("Courier", 20),
                         values=self.expense_category_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # --------------------------------ΗΜΕΡΟΜΗΝΙΑ-----------------------
        tk.Label(self, text="Ημερομηνία (dd-mm-yyyy):", font=("Helvetica", 20)).grid(row=7, column=0, padx=10, pady=5,
                                                                                     sticky="w")
        # tk.Entry(self, textvariable=self.date, font=("Courier", 20)).grid(row=7, column=1, padx=10, pady=5, sticky="ew")
        self.date_button = ttk.Button(self, textvariable=self.date, command=self.open_calendar)
        self.date_button.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        # --------------------------------ΣΥΧΝΟΤΗΤΑ------------------------
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=8, column=0, padx=10, pady=5, sticky="w")
        ttk.Combobox(self, textvariable=self.frequency, font=("Courier", 20), values=self.frequency_options).grid(row=8,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=5,
                                                                                                                  sticky="ew")
        
        # -----------ΓΡΑΦΗΜΑ------
        self.embed_donut_chart(self.db.get_all_data())

        # --------------------------------ΚΟΥΜΠΙ ΠΡΟΣΘΕΣΕ ΕΣΟΔΟ------------------------------
        style = ttk.Style(self)
        style.configure('success.TButton', font=('Helvetica', 16), background='green', foreground='white')
        self.action_button = ttk.Button(self, style='success.TButton')
        self.action_button.grid(row=9, column=0, columnspan=2, pady=10, sticky="nsew")
        

        # ---------------------------------------Treeview---------------------------------------
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

        self.tree.grid(row=1, column=2, rowspan=9, padx=10, pady=10, sticky='nsew')

        # Scrollbars for Treeview
        vscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hscroll = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
        vscroll.grid(row=1, column=3, rowspan=9, sticky='ns')
        hscroll.grid(row=10, column=2, sticky='ew')

        # Grid configuration for resizing
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ON SELECT

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Δημιουργούμε δύο μεταβλητές που ορίζουν: α) σε τι mode είμαστε. Είμαστε σε edit mode ή όχι? β) ποιο είναι το selected item από το treeview?

        self.edit_mode = False
        self.current_item = None
    
    #-------------------------------------ΓΡΑΦΗΜΑ---------------------------------

    def embed_donut_chart(self, data):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        figure = plot_donut_chart(data)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, rowspan=2, columnspan=2, padx=10, pady=10)


    def on_select(self, event):
        current_selected_item = self.tree.selection()

        # Check if the currently selected item was already selected before
        if current_selected_item == self.last_item:
            # Deselect and reset the last_item
            self.tree.selection_remove(current_selected_item)
            self.last_item = None
            self.clear_input()  # Clear the form or reset the UI as necessary
        else:
            # Update the form only if a new item is selected
            if current_selected_item:
                item = self.tree.item(current_selected_item)
                data = item['values']
                self.original_data = {
                    'Date': data[0],
                    'Description': data[1],
                    'Amount': data[2],
                    'Frequency': data[3],
                    'Category': data[4]
                }
                self.description.set(data[1])
                self.amount.set(data[2])
                self.date.set(data[0])
                self.category.set(data[4])
                self.frequency.set(data[3])

            # Store the currently selected item as the last item
            self.last_item = current_selected_item

            # Handle the toggle edit mode based on type
            if self.show_income.get() and current_selected_item:
                self.toggle_edit_mode(True, current_selected_item, income_flag=True)
            elif self.show_expenses.get() and current_selected_item:
                self.toggle_edit_mode(True, current_selected_item, income_flag=False)

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

        self.incomes.append(income_data)  # Add to the list of entries

        self.indb.InsertIncome(
            income_data['Description'],
            income_data['Amount'],
            category_id,
            income_data['Date'],
            frequency_id)
        self.update_table()  # Update the table view
        self.clear_input()

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

        self.expenses.append(expense_data)  # Add to the list of entries

        self.indb.InsertExpense(
            expense_data['Description'],
            expense_data['Amount'],
            category_id,
            expense_data['Date'],
            frequency_id)
        self.update_table()  # Update the table view
        self.clear_input()

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

    def toggle_expenses_off(self):
        # This method is called when the income checkbox is clicked
        if self.show_income.get() == True:
            self.show_expenses.set(False)  # Uncheck expenses
            self.category.set(self.income_category_options[-1])
            ttk.Combobox(self, textvariable=self.category, font=("Courier", 20),
                         values=self.income_category_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.update_table()

    def toggle_income_off(self):
        # This method is called when the expenses checkbox is clicked
        if self.show_expenses.get() == True:
            self.show_income.set(False)  # Uncheck income
            self.category.set(self.expense_category_options[-1])
            ttk.Combobox(self, textvariable=self.category, font=("Courier", 20),
                         values=self.expense_category_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.update_table()

    def toggle_edit_mode(self, edit, item_id=None, income_flag=None):
        self.edit_mode = edit
        self.current_item = item_id

        if income_flag:
            if edit:
                self.action_button.config(text="Ενημέρωση", command=self.update_income)
                self.action_button.grid(columnspan=1)
                self.delete_button.grid()  # Show the delete button when in edit mode
            else:
                self.clear_input()
                # self.action_button.config(text="Πρόσθεσε έσοδο", command=self.add_income)  # Default action
                # self.action_button.grid(columnspan=2)
                # self.delete_button.grid_remove()  # Hide the delete button when not in edit mode
        else:
            if edit:
                self.action_button.config(text="Ενημέρωση", command=self.update_expense)
                self.action_button.grid(columnspan=1)
                self.delete_button.grid()
            else:
                # self.action_button.config(text="Πρόσθεσε έξοδο", command=self.add_expense)
                # self.delete_button.grid_remove()
                self.clear_input()

    def clear_input(self):
        self.description.set("")
        self.amount.set("")
        self.date.set(current_date())
        self.frequency.set(self.frequency_options[2])

        self.tree.selection_remove(self.tree.selection())
        self.delete_button.grid_remove()
        self.action_button.grid(row=9, column=0, columnspan=2, pady=10, sticky="nsew")
        self.update_table()
        self.embed_donut_chart(self.db.get_all_data())

    def update_income(self):
        original_description = self.original_data['Description']
        original_amount = self.original_data['Amount']
        original_date = self.original_data['Date']
        original_frequency = self.original_data['Frequency']
        

        new_description = self.description.get()
        new_amount = self.correct_amount()
        new_date = self.date.get()
        new_frequency = self.frequency.get()
        new_category = self.category.get()

        income_id = self.indb.GetID(original_description, original_date, original_amount)

        self.indb.UpdateIncome(new_description, new_date, new_amount, unstuck_frequency(new_frequency),self.indb.GetCategoryIndex(new_category), income_id[0])
        # Reset UI components
        self.clear_input()  # This clears inputs and deselects the Treeview

    def delete_selection(self):
        if self.show_income.get():
            original_description = self.original_data['Description']
            original_amount = self.original_data['Amount']
            original_date = self.original_data['Date']

            income_id = self.indb.GetID(original_description, original_date, original_amount)
            self.indb.DeleteIncome(income_id[0])
            self.clear_input()
        elif self.show_income.get() == False:
            original_description = self.original_data['Description']
            original_amount = self.original_data['Amount']
            original_date = self.original_data['Date']

            expenses_id = self.indb.GetExpensesID(original_description, original_date, original_amount)
            self.indb.DeleteExpense(expenses_id[0])
            self.clear_input()

    def update_expense(self):
        original_description = self.original_data['Description']
        original_amount = self.original_data['Amount']
        original_date = self.original_data['Date']
        # original_frequency = self.original_data['Frequency']

        new_description = self.description.get()
        new_amount = self.correct_amount()
        new_date = self.date.get()
        new_frequency = self.frequency.get()
        new_category = self.category.get()
        
        
        expenses_id = self.indb.GetExpensesID(original_description, original_date, original_amount)
        self.indb.UpdateExpenses(new_description, new_date, new_amount, unstuck_frequency(new_frequency), self.indb.GetCategoryIndex(new_category), expenses_id[0])

        # Reset UI components
        self.clear_input()  # This clears inputs and deselects the Treeview

    def export_to_excel(self):

        # Έλεγχος αν έχει επιλεγεί κάτι για εξαγωγή
        if not self.show_income.get() and not self.show_expenses.get():
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ επιλέξτε έσοδα ή έξοδα για εξαγωγή.")
            return

            # Συνδυάζουμε τα έσοδα και τα έξοδα σε ένα DataFrame
        combined_data = []
        income_entries = self.indb.printData("income")
        for entry in income_entries:
            combined_data.append({
                'Date': entry[1],
                'Description': entry[2],
                'Amount': entry[3],
                'Frequency': entry[7],
                'Category': entry[9],
                'Type': 'Income'
            })

        expense_entries = self.indb.printData("expenses")
        for entry in expense_entries:
            combined_data.append({
                'Date': entry[1],
                'Description': entry[2],
                'Amount': entry[3],
                'Frequency': entry[7],
                'Category': entry[9],
                'Type': 'Expense'
            })

            # Δημιουργία DataFrame από τα δεδομένα
        df = pd.DataFrame(combined_data)

        # Ζητάμε από τον χρήστη να επιλέξει τοποθεσία και όνομα αρχείου για την αποθήκευση
        file_path = asksaveasfilename(defaultextension=".xlsx",
                                      filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

        if file_path:
            # Αποθήκευση του DataFrame σε αρχείο Excel
            df.to_excel(file_path, index=False)

            # Εμφάνιση μηνύματος επιτυχίας
            messagebox.showinfo("Επιτυχία", f"Τα δεδομένα εξήχθησαν επιτυχώς στο αρχείο {file_path}")
        else:
            # Εμφάνιση μηνύματος ακύρωσης
            messagebox.showwarning("Ακύρωση", "Η εξαγωγή ακυρώθηκε")
    
    def UserAddCategory(self):
        self.category_types = {
            "Έσοδο":1,
            "Έξοδο":0
        }

        add_category_window = tk.Toplevel(self)
        add_category_window.title("Προσθήκη Κατηγορίας")

        tk.Label(add_category_window, text="Όνομα Κατηγορίας:", font=("Helvetica", 16)).grid(row=0, column=0, padx=10,
                                                                                            pady=10)
        self.category_name_entry = tk.Entry(add_category_window, font=("Helvetica", 16))
        self.category_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_category_window, text="Τύπος Κατηγορίας:", font=("Helvetica", 16)).grid(row=1, column=0, padx=10,
                                                                                            pady=10)
        self.category_type_var = tk.StringVar()
        self.category_type_var.set(list(self.category_types.keys())[0])


        ttk.Combobox(add_category_window, textvariable=self.category_type_var, values=["Έσοδο", "Έξοδο"],
                    font=("Helvetica", 16)).grid(row=1, column=1, padx=10, pady=10)
        
        save_button = ttk.Button(add_category_window, text="Αποθήκευση", command=self.UserSaveCategory, style='success.TButton')
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def UserSaveCategory(self):
        category_name_entry = self.category_name_entry.get()
        category_type_entry = self.category_type_var.get()
        
        # Retrieve existing categories with their types
        existing_categories = self.indb.showData('category_table', dataframe=False)
        
        # Check if a category with the same name and type already exists
        for cat in existing_categories:
            if cat[1] == category_name_entry and cat[2] == self.category_types[category_type_entry]:
                messagebox.showwarning("Προειδοποίηση", "H κατηγορία υπάρχει ήδη")
                return
        
        # If not found, add the new category
        result = self.indb.AddCategory(category_name_entry, self.category_types[category_type_entry])
        
        # Show success message
        if "προστέθηκε επιτυχώς" in result:
            messagebox.showinfo("Επιτυχία", result)
            self.update_front_end
        else:
            messagebox.showerror("Σφάλμα", result)

    
    def UserDeleteCategory(self):
        delete_category_window = tk.Toplevel(self)
        delete_category_window.title("Διαγραφή Κατηγορίας")
        existing_categories = self.indb.showData('category_table', dataframe=False)

        # Extract category names and types
        category_names = [cat[1] for cat in existing_categories]
        category_types = {1: 'Έσοδο', 0: 'Έξοδο'}

        tk.Label(delete_category_window, text="Επιλογή Κατηγορίας:", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=10)
        self.category_name_var = tk.StringVar()
        ttk.Combobox(delete_category_window, textvariable=self.category_name_var, values=category_names, font=("Helvetica", 16)).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(delete_category_window, text="Τύπος Κατηγορίας:", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10)
        self.category_type_var = tk.StringVar()
        ttk.Combobox(delete_category_window, textvariable=self.category_type_var, values=list(category_types.values()), font=("Helvetica", 16)).grid(row=1, column=1, padx=10, pady=10)

        delete_button = ttk.Button(delete_category_window, text="Διαγραφή", command=lambda: self.UserRemoveCategory(delete_category_window), style='danger.TButton')
        delete_button.grid(row=2, column=0, columnspan=2, pady=10)


        
    def UserRemoveCategory(self, delete_category_window):
        category_name = self.category_name_var.get()
        category_type_str = self.category_type_var.get()
        
        # Map category type string to integer
        category_types = {'Έσοδο': 1, 'Έξοδο': 0}
        category_type = category_types[category_type_str]
        
        existing_categories = self.indb.showData('category_table', dataframe=False)
        
        # Check if category exists with the specified type
        category_exists = any(cat[1] == category_name and cat[2] == category_type for cat in existing_categories)
        
        if not category_exists:
            messagebox.showwarning("Προειδοποίηση", "Η κατηγορία δεν μπορεί να διαγραφεί διότι δεν υπάρχει.")
            return
        
        # Attempt to delete the category
        result = self.indb.DeleteCategory(category_name, category_type)
        
        # Show result message
        if "διαγράφηκε επιτυχώς" in result:
            messagebox.showinfo("Επιτυχία", result)
            self.update_front_end()
        else:
            messagebox.showerror("Σφάλμα", result)
    
    def update_front_end(self):
        self.income_category_options = [i[1] for i in self.indb.showData('category_table') if i[2] == 1]
        self.expense_category_options = [i[1] for i in self.indb.showData('category_table') if i[2] == 0]
        if self.show_expenses.get() == True:
            self.category.set(self.expense_category_options[-1])
            ttk.Combobox(self, textvariable=self.category, font=("Courier", 20),
                         values=self.expense_category_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        else:
            self.category.set(self.income_category_options[-1])
            ttk.Combobox(self, textvariable=self.category, font=("Courier", 20),
                         values=self.income_category_options).grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        print("update front end RUN")
        