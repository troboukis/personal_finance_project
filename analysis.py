import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import ttkbootstrap as bttk
import numpy as np

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app import DatabaseConnection, new_db
from ttkbootstrap import Style
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap

class FinanceAnalysis(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Create a label
        # tk.Label(self, text="freq", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="n")

        # Initialize the DatabaseConnection
        self.data = DatabaseConnection(new_db)
        self.df = self.data.get_all_data()
        self.df.to_csv("./t.csv", index=False)

        # Initialize canvas attribute for later reference
        self.canvas = None
        
        # Initialize the current chart index
        self.current_chart_index = 0

        # Create and embed the bar chart
        self.embed_bar_chart(self.df)

        # Add Refresh button
        refresh_button = bttk.Button(self)
        # style='primary-outline.TButton',
        # text = "Refresh",
        # command = self.refresh_data,
        # cursor = 'hand2')

        refresh_button.grid(row=1, column=0, padx=10, pady=5, sticky="ns")
        
        # Add Next Chart button
        next_chart_button = bttk.Button(self,
        style='primary-outline.TButton',
        text="Next Chart", 
        command=self.next_chart, 
        cursor = 'hand2')
        
        next_chart_button.grid(row=1, column=1, padx=10, pady=5, sticky="ne")

        # Add Exit button
        exit_button = bttk.Button(self,
        style='primary-outline.TButton',
        text="Exit", 
        command=self.quit,
        cursor = 'hand2')
        
        exit_button.grid(row=10, column=4,sticky="se") # padx=10, pady=5,

        # Configure grid to make widgets expand
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def embed_bar_chart(self, data):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
            
        figure = chart_functions[self.current_chart_index](data)
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def refresh_data(self):
        self.df = self.data.get_all_data()  # Re-fetch the data
        self.embed_bar_chart(self.df)  # Re-embed the updated bar chart

    def next_chart(self):
        self.current_chart_index = (self.current_chart_index + 1) % len(chart_functions)
        self.refresh_data()

# def chart1(data):
#     # Filter the data to include only "Έσοδο"
#     income_data = data[data['Τύπος'] == 'Έσοδο']

#     # Group by category and sum the amounts
#     income_by_category = income_data.groupby('Κατηγορία')['Ποσό'].sum()

#     # Create the vertical bar chart
#     fig, ax = plt.subplots(figsize=(10, 6))
#     income_by_category.plot(kind='bar', ax=ax)
#     ax.set_title('Έσοδα ανά Κατηγορία')
#     ax.set_xlabel('Κατηγορία')
#     ax.set_ylabel('Ποσό (€)')
#     ax.set_xticks(ax.get_xticks())
#     ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
#     plt.tight_layout()

#     return fig

def chart1(data):
    # Group by category and calculate the sum of Έσοδα and Έξοδα
    grouped_data = data.groupby(['Κατηγορία', 'Τύπος'])['Ποσό'].sum().unstack(fill_value=0)
    
    # Calculate the difference between Έσοδα and Έξοδα
    net_amounts = grouped_data['Έσοδο'] - grouped_data['Έξοδο']
    
    # Sort the net amounts in ascending order (lowest on top, highest on bottom)
    net_amounts = net_amounts.sort_values(ascending=True)
    
    # Create the horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    net_amounts.plot(kind='barh', ax=ax)
    ax.set_title('Έσοδα - Έξοδα ανά Κατηγορία')
    ax.set_xlabel('Καθαρό Ποσό (€)')
    ax.set_ylabel('Κατηγορία')
    plt.tight_layout()

    return fig

def chart2(data):
    
    # Group by type (Έσοδο, Έξοδο) and sum the amounts
    total_amounts = data.groupby('Τύπος')['Ποσό'].sum()
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    total_amounts.plot(kind='bar', ax=ax, color=['red', 'green'])
    ax.set_title('Συνολικά Έσοδα και Έξοδα')
    ax.set_xlabel('Τύπος')
    ax.set_ylabel('Ποσό (€)')
    plt.xticks(rotation=0)
    plt.tight_layout()

    return fig

def chart3(data):
   # Convert date to datetime and extract the year and month
    data['Ημερομηνία'] = pd.to_datetime(data['Ημερομηνία'])
    data['Έτος'] = data['Ημερομηνία'].dt.year
    data['Μήνας'] = data['Ημερομηνία'].dt.month
    
    # Group data by year, month and type, then calculate sum of amounts
    grouped_data = data.groupby(['Έτος', 'Μήνας', 'Τύπος'])['Ποσό'].sum().unstack(fill_value=0)
    
    # Calculate difference between income and expenses
    grouped_data['Διαφορά'] = grouped_data.get('Έσοδο', 0) - grouped_data.get('Έξοδο', 0)
    
    # Ensure all months are represented
    for year in grouped_data.index.levels[0]:
        for month in range(1, 13):
            if (year, month) not in grouped_data.index:
                grouped_data.loc[(year, month), 'Διαφορά'] = 0
    
    grouped_data = grouped_data.sort_index(ascending=False)  # Sort data so January is at the top
    
    # Creating month-year labels for the y-axis
    month_year_labels = [f'{y}-{m:02d}' for y, m in grouped_data.index]
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 8))
    grouped_data['Διαφορά'].plot(kind='barh', color='skyblue', title='Διαφορά Εσόδων και Εξόδων ανά Μήνα', ax=ax)
    ax.set_ylabel('Μήνας (Έτος, Μήνας)')
    ax.set_xlabel('Διαφορά Ποσών')
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.set_yticklabels(month_year_labels)  # Set custom labels
    
    return fig


chart_functions = [chart2, chart1, chart3]

# Example usage in a root window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x768")  # Set a default window size
    app = FinanceAnalysis(root)
    app.pack(fill='both', expand=True)
    root.mainloop()



