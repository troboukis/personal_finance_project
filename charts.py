import pandas as pd

import matplotlib.pyplot as plt

def plot_donut_chart(data):
    total_income = 0
    total_expense = 0
    # Ρύθμιση του μεγέθους του γραφήματος για το διάγραμμα
    plt.rcParams["figure.figsize"] = (2, 2)

    # Μετατροπή των τιμών στη στήλη 'Ποσό' σε αριθμητικό τύπο. Αγνοούμε τα σφάλματα
    data['Ποσό'] = pd.to_numeric(data['Ποσό'], errors='coerce')

    # Γκρουπάρισμα των δεδομένων ανά τύπο και υπολογισμός του συνολικού ποσού
    summary = data.groupby('Τύπος')['Ποσό'].sum()

    # Δημιουργία λίστας με χρώματα, πράσινο για 'Έσοδα' και κόκκινο για 'Έξοδα'
    colors = ['green' if typ == 'Έσοδο' else 'red' for typ in summary.index]
    
    # Δημιουργία donut διαγράμματος
    fig, ax = plt.subplots()
    ax.pie(summary, startangle=90, colors=colors, wedgeprops=dict(width=0.3))

    # Προσθήκη εσωτερικού κύκλου για εφέ donut
    centre_circle = plt.Circle((0,0), 0.70, fc='none')
    fig.gca().add_artist(centre_circle)

    # Ρύθμιση αξόνων
    ax.axis('equal')
    fig.patch.set_alpha(0.0)
    
    # Υπολογισμός συνολικών εσόδων και εξόδων
    total_income = summary.get('Έσοδο', 0) # ανακτούμε την τιμή από το pandas Series. Εάν η κατηγορία 'Έσοδο' δεν υπάρχει, τότε επιστρέφει την τιμή 0.
    total_expense = summary.get('Έξοδο', 0)
    remaining_amount = total_income - total_expense

    # Προσθήκη κειμένου για τα έσοδα, τα έξοδα και το υπόλοιπο
    plt.text(.5, 1, f'Έσοδα: {total_income} €', color='green', fontsize=6)
    plt.text(-1.3, 1, f'Έξοδα: {total_expense} €', color='red', fontsize=6)
    plt.text(0, 0, f'Υπόλοιπο\n{remaining_amount} €', ha='center', va='center', fontsize=10, weight='light', color='white')
    
    # Επιστροφή της φιγούρας
    return fig

