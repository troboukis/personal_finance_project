import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import ttkbootstrap as bttk
import numpy as np
import mplcursors

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


        # Initialize canvas attribute for later reference
        self.canvas = None
        
        # Initialize the current chart index
        self.current_chart_index = 0

        # Create and embed the bar chart
        self.embed_bar_chart(self.df)

        # Add Refresh button
        refresh_button = bttk.Button(self,
        style='primary-outline.TButton',
        text = "Refresh 🔄",
        command = self.refresh_data,
        cursor = 'hand2')

        refresh_button.grid(row=1, column=0, padx=0, pady=5, sticky="nw")
        
        # Add Next Chart button
        next_chart_button = bttk.Button(self,
        style='primary-outline.TButton',
        text="Next Chart ➡️", 
        command=self.next_chart, 
        cursor = 'hand2')
        
        next_chart_button.grid(row=1, column=1, padx=10, pady=5, sticky="ne")


        # Add Next Chart button
        back_chart_button = bttk.Button(self,
        style='primary-outline.TButton',
        text="⬅️ Back Chart", 
        command=self.back_chart, 
        cursor = 'hand2')
        
        back_chart_button.grid(row=1, column=1, padx=115, pady=5, sticky="ne")


        # Add Exit button
        exit_button = bttk.Button(self,
        style='primary-outline.TButton',
        text="Exit", 
        command=self.quit,
        cursor = 'hand2')
        
        exit_button.grid(row=10, column=4,sticky="se")

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
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, padx=0, pady=10, sticky="nsew")

    def refresh_data(self):
        self.df = self.data.get_all_data()  # Re-fetch the data
        self.embed_bar_chart(self.df)  # Re-embed the updated bar chart

    def next_chart(self):
        self.current_chart_index = (self.current_chart_index + 1) % len(chart_functions)
        self.refresh_data()

    def back_chart(self):
        self.current_chart_index = (self.current_chart_index - 1) % len(chart_functions)
        self.refresh_data()


def chart1(data):
    # Group by category and calculate the sum of Έσοδα and Έξοδα
    grouped_data = data.groupby(['Κατηγορία', 'Τύπος'])['Ποσό'].sum().unstack(fill_value=0)
    
    # Calculate the difference between Έσοδα and Έξοδα
    net_amounts = grouped_data['Έσοδο'] - grouped_data['Έξοδο']
    
    # Sort the net amounts in ascending order (lowest on top, highest on bottom)
    net_amounts = net_amounts.sort_values(ascending=True)
    
    # Create the horizontal bar chart
    fig, ax = plt.subplots(figsize=(7, 4))
    net_amounts.plot(kind='barh', ax=ax, color=['red' if x < 0 else 'green' for x in net_amounts], edgecolor='black', linewidth=1, zorder=3)
    
    ax.grid(True, linestyle='--', linewidth=0.2, color='lightgray', which='both', axis='both', zorder=0)
    
    ax.axvline(x=0, color='white', linestyle='-', linewidth=0.8, zorder=4)
    
    ax.set_title('Έσοδα - Έξοδα ανά Κατηγορία', fontsize=12, weight='bold', color='white')
    ax.set_xlabel('Καθαρό Ποσό (€)', fontsize=12, weight='bold', color='white')
    ax.set_ylabel('Κατηγορία', fontsize=12, weight='bold', color='white')
    plt.tight_layout()
    
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.tick_params(axis='x', colors='#FFFFFA')
    ax.tick_params(axis='y', colors='#FFFFFA')
    for spine in ax.spines.values():
        spine.set_color('lightgray')
    
    # Add annotations
    for i, (category, amount) in enumerate(zip(net_amounts.index, net_amounts)):
        color = 'red' if amount < 0 else 'green'
        ax.annotate(f'{amount:.2f} €', xy=(amount, i),
                    xytext=(5, 0), textcoords='offset points',
                    ha='left' if amount >= 0 else 'right', va='center', fontsize=8, weight='bold', color='white')

        # Draw annotation line
        ax.vlines(x=amount, ymin=i - 0.4, ymax=i + 0.4, color='white', linewidth=1)

    return fig



def chart2(data):
    # Group by type (Έσοδο, Έξοδο) and sum the amounts
    total_amounts = data.groupby('Τύπος')['Ποσό'].sum()
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.grid(True, linestyle='-', linewidth=0.2, color='lightgray', which='both', axis='both')
    
    # Plot the bars
    bars = ax.bar(total_amounts.index, total_amounts, color=['red', 'green'], edgecolor='black', linewidth=1, width=0.4, zorder=3)
    
    # Add annotations
    for bar, amount in zip(bars, total_amounts):
        height = bar.get_height()
        ax.annotate(f'{amount:.2f} €', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold', color='white')
        
        # Draw annotation line
        ax.plot([bar.get_x(), bar.get_x() + bar.get_width()], [height, height], color='white', linewidth=1)

    ax.set_title('Συνολικά Έσοδα και Έξοδα', fontsize=12, weight='bold', color='white')
    ax.set_xlabel('Τύπος', fontsize=12, weight='bold', color='white')
    ax.set_ylabel('Ποσό (€)', fontsize=12, weight='bold', color='white')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.tick_params(axis='x', colors='#FFFFFA')
    ax.tick_params(axis='y', colors='#FFFFFA')

    for spine in ax.spines.values():
        spine.set_color('lightgray')
    
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
    
    # # Plotting
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ['green' if val >= 0 else 'red' for val in grouped_data['Διαφορά']]
    bars = grouped_data['Διαφορά'].plot(kind='barh', color=colors, ax=ax)
    ax.set_title('Διαφορά Εσόδων και Εξόδων ανά Μήνα', fontsize=12, weight='bold', color='white', pad=20)
    ax.set_ylabel('Μήνας (Έτος, Μήνας)', fontsize=12, weight='bold', color='white', labelpad=10)
    ax.set_xlabel('Διαφορά Ποσών', fontsize=12, weight='bold', color='white', labelpad=10)
    ax.axvline(0, color='white', linestyle='--', linewidth=1)
    ax.set_yticklabels(month_year_labels, fontsize=10, weight='bold', color='white')
    ax.tick_params(axis='x', colors='lightgray')
    ax.tick_params(axis='y', colors='lightgray')
    for spine in ax.spines.values():
        spine.set_color('lightgray')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    plt.tight_layout()
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Add values next to bars
    for bar, value in zip(ax.patches, grouped_data['Διαφορά']):
        if value >= 0:
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value:.2f}', ha='left', va='center', color='white', fontsize=10)
        else:
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value:.2f}', ha='right', va='center', color='white', fontsize=10)

    return fig


chart_functions = [chart2, chart1, chart3]

# Example usage in a root window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x768")  # Set a default window size
    app = FinanceAnalysis(root)
    app.pack(fill='both', expand=True)
    root.mainloop()
