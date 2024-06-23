import pandas as pd
import matplotlib.pyplot as plt

def plot_donut_chart(data):
    total_income = 0
    total_expense = 0
    # Ρύθμιση του μεγέθους του γραφήματος για το διάγραμμα
    plt.rcParams["figure.figsize"] = (2, 2)

    # Μετατροπή των τιμών στη στήλη 'Ποσό' σε αριθμητικό τύπο, αγνοώντας τα σφάλματα
    data['Ποσό'] = pd.to_numeric(data['Ποσό'], errors='coerce')

    # Γκρουπάρισμα των δεδομένων ανά τύπο και υπολογισμός του συνολικού ποσού
    summary = data.groupby('Τύπος')['Ποσό'].sum()

    # Υπολογισμός συνολικών εσόδων και εξόδων
    total_income = summary.get('Έσοδο', 0)  # Ανάκτηση της τιμής για 'Έσοδα', 0 αν δεν υπάρχει
    total_expense = summary.get('Έξοδο', 0)
    remaining_amount = total_income - total_expense

    if remaining_amount != 0:
        colors = ['green' if typ == 'Έσοδο' else 'red' for typ in summary.index]
        fig, ax = plt.subplots()
        ax.pie(summary, startangle=90, colors=colors, wedgeprops=dict(width=0.3))
        centre_circle = plt.Circle((0,0), 0.70, fc='none')
        fig.gca().add_artist(centre_circle)
        ax.axis('equal')
        fig.patch.set_alpha(0.0)
        plt.text(.2, 1, f'Έσοδα: {total_income} €', color='green', fontsize=6)
        plt.text(-1.1, 1, f'Έξοδα: {total_expense} €', color='red', fontsize=6)
        plt.text(0, 0, f'Υπόλοιπο\n{remaining_amount} €', ha='center', va='center', fontsize=10, weight='light', color='white')
    else:
        fig, ax = plt.subplots()
        ax.pie([1], startangle=90, colors=['gray'], wedgeprops=dict(width=0.3))
        centre_circle = plt.Circle((0,0), 0.70, fc='none')
        fig.gca().add_artist(centre_circle)
        ax.axis('equal')
        fig.patch.set_alpha(0.0)
        plt.text(0, 0, f'Υπόλοιπο\n0 €', ha='center', va='center', fontsize=10, weight='light', color='white')
    return fig
