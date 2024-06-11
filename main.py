import tkinter as tk
from tkinter import ttk
import ttkbootstrap as bttk
from ttkbootstrap import Style
import datetime
from income_expenses import IncomeExpensesFrame 
from app import *
import random
from analysis import FinanceAnalysis

def current_date(show_full_date = False):
    # Επιστροφή της τρέχουσας ημερομηνίας ως συμβολοσειρά
    if show_full_date:
        return datetime.datetime.now().strftime("%b %d %Y, %H:%M")
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d")

def show_frame(frame):
    frame.tkraise()

def main():
    root = bttk.Window(themename='solar')
    root.title("Διαχείριση προσωπικών οικονομικών")
    root.geometry("1366x768")

    style = Style()
    style.configure('W.TButton', font=('Roboto', 20, 'bold'), padding=20)
    

    # Δημιουργία πλαισίων για κάθε τμήμα του προγράμματος
    home_frame = tk.Frame(root) #Πρώτη σελίδα
    income_expenses_frame = IncomeExpensesFrame(root) #Έσοδα - Έξοδα
    analysis_frame = FinanceAnalysis(root) # Ανάλυση

    frames = [home_frame, income_expenses_frame, analysis_frame]
    # Τοποθέτηση στη σελίδα
    for frame in frames:
        frame.grid(row=0, column=0, sticky='nsew')

    # Διαμόρφωση διάταξης στο root
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Προσθήκη ημερομηνίας σε κάθε πλαίσιο χρησιμοποιώντας grid
    date_label_format = ("Courier", 12)
    for i, frame in enumerate(frames):
        tk.Label(frame, text=current_date(True), font=date_label_format)\
            .grid(row=0, column=0, sticky='w', padx=10, pady=10)

    # Διαμόρφωση πρώτης σελίδας
    tk.Label(home_frame, text="Διαχείριση προσωπικών οικονομικών", font=("Helvetica", 35), background="#FFDEAD", foreground="#000000").grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=50)
    # Διαχωριστικό σελίδας
    separator = bttk.Separator(home_frame, orient='horizontal')
    separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(170, 90))
    tk.Label(home_frame, text="Ομάδα Δ", font=("Helvetica", 25), background="#FFDEAD", foreground="#000000").grid(row=2, column=0, columnspan=3, sticky='ew', padx=0, pady=0)
    # Ομάδα
    tk.Label(home_frame, text="Θανάσης Τρομπούκης (συντονιστής), Αλέξανδρος Ρουμελιωτάκης, Νίκος Ταμπουρατζής, Γιώργος Παπαδόπουλος, Γιώργος Τσιώκος", font=("Helvetica", 15), background="#FFDEAD", foreground="#000000").grid(row=3, column=0, columnspan=3, sticky='ew', padx=0, pady=0)

    # Κουμπί έσοδα - έξοδα
    bttk.Button(home_frame, text='Έσοδα - Έξοδα', style='primary.TButton', command=lambda: show_frame(income_expenses_frame))\
        .grid(row=4, column=0, padx=20, pady=40, sticky='ew')

    # Κουμπί Ανάλυσης
    bttk.Button(home_frame, text='Ανάλυση', style='primary.TButton', command=lambda: show_frame(analysis_frame))\
        .grid(row=4, column=1, padx=20, pady=20, sticky='ew')

    home_frame.grid_columnconfigure((0, 1), weight=1, uniform="group1")
    home_frame.grid_rowconfigure(1, weight=1)

    bttk.Button(income_expenses_frame, text="Επιστροφή", style='primary-outline.TButton', command=lambda: show_frame(home_frame)).grid(row=0, column=2, sticky='w', pady=10)
    bttk.Button(analysis_frame, text="Back to Home", style='primary-outline.TButton', command=lambda: show_frame(home_frame)).grid(row=10, column=0, sticky='ew')

    # Start on the Home Frame
    show_frame(home_frame)
    root.mainloop()

if __name__ == "__main__":
    # Αρχικοποίηση βάσης δεδομένων
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

    # Δημιουργία ενός νέου αντικειμένου Income με όρισμα το path που θα αποθηκευτεί η βάση
    dbin = Income(new_db)
    for income in income_list+expenses_list:
        # Καλούμε τη μέθοδο InsertCategory για να δημιουργήσουμε στο βρόχο τις νέες κατηγορίες εσόδων - εξόδων. Το εάν θα μπει στα έσοδα ή έξοδα αποφασίζεται στο app.py στη μέθοδο InsertCategory
        dbin.InsertCategory(income)

    income_examples = [
    {"date": "2023-04-01", "name": "Μισθός Απριλίου", "category": "Μισθός", "amount": 1200},
    {"date": "2023-04-03", "name": "Ενοίκιο ακινήτου", "category": "Ενοίκια", "amount": 500},
    # {"date": "2023-04-05", "name": "Πώληση προϊόντων", "category": "Πωλήσεις", "amount": 300},
    # {"date": "2023-04-07", "name": "Τόκοι καταθέσεων", "category": "Τόκοι τραπεζικών καταθέσεων", "amount": 150},
    # {"date": "2023-04-12", "name": "Κέρδη από μετοχές", "category": "Κέρδη από μετοχές", "amount": 250},
    # {"date": "2023-04-15", "name": "Αποζημίωση ασφάλισης", "category": "Αποζημιώσεις", "amount": 1000},
    # {"date": "2023-04-18", "name": "Συνταξιοδότηση", "category": "Σύνταξη", "amount": 800},
    # {"date": "2023-04-20", "name": "Έσοδα από μικρά projects", "category": "Άλλα έσοδα", "amount": 450}
]
    expense_examples = [
    {"date": "2023-04-01", "name": "Μηνιαίο ενοίκιο διαμερίσματος", "category": "Ενοίκια", "amount": 400},
    {"date": "2023-04-02", "name": "Αγορά τροφίμων", "category": "Τρόφιμα", "amount": 250},
    # {"date": "2023-04-03", "name": "Λογαριασμός ηλεκτρισμού", "category": "Δαπάνες για ενέργεια", "amount": 100},
    # {"date": "2023-04-04", "name": "Λογαριασμός ύδρευσης", "category": "Νερό", "amount": 50},
    # {"date": "2023-04-05", "name": "Γέμισμα καυσίμων", "category": "Καύσιμα", "amount": 60},
    # {"date": "2023-04-06", "name": "Πληρωμή λογαριασμού κινητού τηλεφώνου", "category": "Τηλεπικοινωνίες", "amount": 30},
    # {"date": "2023-04-07", "name": "Ανανέωση ασφάλισης αυτοκινήτου", "category": "Ασφάλειες", "amount": 200},
    # {"date": "2023-04-08", "name": "Πληρωμή ακινήτων ΕΝΦΙΑ", "category": "Φόροι και τέλη", "amount": 300},
    # {"date": "2023-04-09", "name": "Μηνιαία δόση στεγαστικού δανείου", "category": "Δόση δανείου", "amount": 500},
    # {"date": "2023-04-10", "name": "Επισκευή βλάβης στο σπίτι", "category": "Συντήρηση και επισκευές", "amount": 150},
    # {"date": "2023-04-11", "name": "Έκτακτα έξοδα ιατρικής φροντίδας", "category": "Άλλα έξοδα", "amount": 180}
]

    #  Καταχώρηση ψεύτικων εσόδων εάν δεν υπάρχουν
    if len(dbin.showData('income'))<1:
        for i in income_examples:
            dbin.InsertIncome(i['name'], 
                            i['amount'], 
                            return_index(i['category'], dbin.showData('category_table', dataframe=False)), 
                            i['date'], 
                            random.randint(0, 2))
    
    # Καταχώρηση ψεύτικων εξόδων εάν δεν υπάρχουν
    if len(dbin.showData('expenses'))<1:
        for i in expense_examples:
            dbin.InsertExpense(i['name'], 
                            i['amount'], 
                            return_index(i['category'], dbin.showData('category_table', dataframe=False)), 
                            i['date'], 
                            random.randint(0, 2))

    main()