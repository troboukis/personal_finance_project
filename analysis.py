import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from app import DatabaseConnection, new_db

class FinanceAnalysis(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Create a label
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=8, column=0, padx=10, pady=5, sticky="w")
        
        # Initialize the DatabaseConnection
        self.data = DatabaseConnection(new_db)
        self.df = self.data.get_all_data()  # Assuming get_all_data is a method, it needs to be called with ()

        # Initialize canvas attribute for later reference
        self.canvas = None

        # Create and embed the donut chart
        self.embed_donut_chart(self.df)  # Pass the DataFrame directly

    def embed_donut_chart(self, data):
        if self.canvas:  # Check if canvas exists before trying to destroy it
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
            
        figure = chart1(data)
        self.canvas = FigureCanvasTkAgg(figure, self)  # Save the canvas as an instance attribute
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=1, padx=10, pady=10)

def chart1(data):
    plt.rcParams["figure.figsize"] = (4, 4)  # Smaller figure size
    data['Ποσό'] = pd.to_numeric(data['Ποσό'], errors='coerce')
    summary = data.groupby('Τύπος')['Ποσό'].sum()
    colors = ['green' if typ == 'Έσοδο' else 'red' for typ in summary.index]
    
    fig, ax = plt.subplots()
    ax.pie(summary, labels=summary.index, startangle=90, colors=colors, wedgeprops=dict(width=0.3))
    centre_circle = plt.Circle((0,0), 0.70, fc='none')
    ax.add_artist(centre_circle)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig.patch.set_alpha(0.0)  # Transparent background

    total_income = summary.get('Έσοδο', 0)
    total_expense = summary.get('Έξοδο', 0)
    remaining_amount = total_income - total_expense

    # Text inside the donut
    ax.text(0, 0, f'Υπόλοιπο\n{remaining_amount} €', ha='center', va='center', fontsize=10, weight='bold', color='white')

    return fig


# Example usage in a root window
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceAnalysis(root)
    app.pack(fill='both', expand=True)
    root.mainloop()
