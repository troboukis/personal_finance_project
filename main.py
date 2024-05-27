import tkinter as tk
import ttkbootstrap as bttk
from ttkbootstrap import Style
import datetime
from income_expenses import IncomeExpensesFrame 
from app import *
import random

# new_db = "/Users/troboukis/Code/EAP/PLHPRO/final-project/FINANCE-DATABASE/new_db.db"
def current_date(show_full_date = False):
    # Return the current date as a string
    if show_full_date:
        return datetime.datetime.now().strftime("%b %d %Y, %H:%M")
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d")

def on_enter_frame(frame):
    # Define actions to take when a frame is entered
    print(f"Entering {frame.winfo_name()}")

def show_frame(frame):
    frame.tkraise()

def main():
    root = bttk.Window(themename='solar')
    root.title("Διαχείριση προσωπικών οικονομικών")
    root.geometry("1366x768")

    style = Style()
    style.configure('W.TButton', font=('Roboto', 20, 'bold'), padding=20)

    # Creating frames for each section
    home_frame = tk.Frame(root)
    income_expenses_frame = IncomeExpensesFrame(root)
    analysis_frame = tk.Frame(root)

    frames = [home_frame, income_expenses_frame, analysis_frame]
    for frame in frames:
        frame.grid(row=0, column=0, sticky='nsew')

    # Configuring grid layout on root
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    show_full_date = True
    # Add Date Label to Each Frame using grid
    date_label_format = ("Courier", 12)
    for i, frame in enumerate(frames):
        tk.Label(frame, text=current_date(True), font=date_label_format)\
            .grid(row=0, column=0, sticky='w', padx=10, pady=10)

    # Home Frame Widgets
    tk.Label(home_frame, text="Διαχείριση προσωπικών οικονομικών", font=("Helvetica", 35), background="#FFDEAD", foreground="#000000").grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=50)
    # default separator style
    separator = bttk.Separator(home_frame, orient='horizontal')
    separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(170, 90))
    tk.Label(home_frame, text="Ομάδα Δ", font=("Helvetica", 25), background="#FFDEAD", foreground="#000000").grid(row=2, column=0, columnspan=3, sticky='ew', padx=0, pady=0)
    tk.Label(home_frame, text="Θανάσης Τρομπούκης (συντονιστής), Αλέξανδρος Ρουμελιωτάκης, Νίκος Ταμπουρατζής, Γιώργος Παπαδόπουλος, Γιώργος Τσιώκος", font=("Helvetica", 15), background="#FFDEAD", foreground="#000000").grid(row=3, column=0, columnspan=3, sticky='ew', padx=0, pady=0)

    bttk.Button(home_frame, text='Έσοδα - Έξοδα', style='primary.TButton', command=lambda: show_frame(income_expenses_frame))\
        .grid(row=4, column=0, padx=20, pady=40, sticky='ew')
    bttk.Button(home_frame, text='Ανάλυση', style='primary.TButton', command=lambda: show_frame(analysis_frame))\
        .grid(row=4, column=1, padx=20, pady=20, sticky='ew')

    home_frame.grid_columnconfigure((0, 1), weight=1, uniform="group1")
    home_frame.grid_rowconfigure(1, weight=1)

    # Analysis Frame Widgets
    tk.Label(analysis_frame, text="Ανάλυση", font=("Helvetica", 35)).grid(row=1, column=0, sticky='ew', padx=10, pady=200)
    bttk.Button(analysis_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame)).grid(row=10, column=0, sticky='ew')
    

    # Start on the Home Frame
    show_frame(home_frame)
    root.mainloop()

if __name__ == "__main__":
    with DatabaseConnection(new_db) as db:
        
        db.initializeTable(freq_sql, 'frequency_table', 'freq_id', 'name', 0, 'Μηνιαίο')
        db.initializeTable(freq_sql, 'frequency_table', 'freq_id', 'name', 1, 'Ετήσιο')
        db.initializeTable(freq_sql, 'frequency_table', 'freq_id', 'name', 2, 'Έκτακτο')

        db.initializeTable(type_sql, 'type_table', 'type_id', 'name', 0, 'Έξοδο')
        db.initializeTable(type_sql, 'type_table', 'type_id', 'name', 1, 'Έσοδο')

        db.create_table(category_sql)
        db.create_table(income_sql)
        db.create_table(expenses_sql)

        tables = db.get_tables()

    # Καταχώρηση βασικών κατηγοριών

    dbin = Income(new_db)
    for income in income_list+expenses_list:
        dbin.InsertCategory(income)

    income_examples = [{"date": "2023-04-01", "name": "Μισθός Απριλίου", "category": "Μισθός", "amount": 1200},{"date": "2023-04-03", "name": "Ενοίκιο ακινήτου", "category": "Ενοίκια", "amount": 500},{"date": "2023-04-05", "name": "Πώληση προϊόντων", "category": "Πωλήσεις", "amount": 300},{"date": "2023-04-07", "name": "Τόκοι καταθέσεων", "category": "Τόκοι", "amount": 150},{"date": "2023-04-10", "name": "Δικαιώματα εκδόσεων", "category": "Δικαιώματα", "amount": 200},{"date": "2023-04-12", "name": "Κέρδη από μετοχές", "category": "Μετοχές", "amount": 250},{"date": "2023-04-15", "name": "Αποζημίωση ασφάλισης", "category": "Αποζημιώσεις", "amount": 1000},{"date": "2023-04-18", "name": "Συνταξιοδότηση", "category": "Συντάξεις", "amount": 800},{"date": "2023-04-20", "name": "Παροχές ασφαλιστικού ταμείου", "category": "Παροχές", "amount": 450},{"date": "2023-04-22", "name": "Επιδότηση επιχείρησης", "category": "Επιδοτήσεις", "amount": 600},{"date": "2023-04-25", "name": "Εισόδημα από freelance δουλειά", "category": "Freelance", "amount": 1200},{"date": "2023-04-27", "name": "Έσοδα από διαφημίσεις", "category": "Διαφημίσεις", "amount": 300},{"date": "2023-04-29", "name": "Έσοδα από εκμίσθωση εξοπλισμού", "category": "Εκμισθώσεις", "amount": 700},{"date": "2023-05-01", "name": "Μπόνους επίτευξης στόχων", "category": "Μπόνους", "amount": 500},{"date": "2023-05-03", "name": "Έσοδα από οργάνωση εκδηλώσεων", "category": "Εκδηλώσεις", "amount": 400}]

     # Καταχώρηση ψεύτικων εσόδων εάν δεν υπάρχουν
    if len(dbin.showData('income'))<1:
        for i in income_examples:
            dbin.InsertIncome(i['name'], 
                            i['amount'], 
                            return_index(i['category'], dbin.showData('category_table', dataframe=False)), 
                            i['date'], 
                            random.randint(0, 2))

    main()