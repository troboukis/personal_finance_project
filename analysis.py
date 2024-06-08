import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from app import DatabaseConnection, new_db
from ttkbootstrap import Style
import ttkbootstrap as bttk

class FinanceAnalysis(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Create a label
        tk.Label(self, text="Συχνότητα", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="n")

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
        text = "Refresh",
        command = self.refresh_data,
        cursor = 'hand2')

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

def chart1(data):
    plt.rcParams["figure.figsize"] = (6, 4)  # Adjust the figure size for a smaller bar chart

    data['Ποσό'] = pd.to_numeric(data['Ποσό'], errors='coerce')
    summary = data.groupby('Τύπος')['Ποσό'].sum()
    colors = ['#d62728', '#2ca02c']  # Custom colors

    fig, ax = plt.subplots(facecolor='#002B36')  # Set background color

    ax.set_ylabel('Ποσό (€)', fontsize=12, weight='bold')
    ax.set_title('Σύνολο Ποσών ανά Τύπο', fontsize=14, weight='bold')

    # Set grid behind bars
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)  # Lower zorder for grid lines

    # Remove top and right spines for a cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Draw bars with a higher zorder to be on top of the grid lines
    bars = ax.bar(summary.index, summary, color=colors, edgecolor='black', linewidth=1, width=0.4, zorder=3)  # Adjust the width here

    # Add text annotations on the bars
    for bar, amount in zip(bars, summary):
        height = bar.get_height()
        ax.annotate(f'{amount:.2f} €', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold')

    fig.patch.set_alpha(0.0)  # Transparent figure background
    ax.patch.set_alpha(0.0)  # Transparent axes background
    return fig

# Define additional chart functions
def chart2(data):
    # Define your second chart function here
    pass

# Add additional chart functions to this list
chart_functions = [chart1, chart2]

# Example usage in a root window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x768")  # Set a default window size
    app = FinanceAnalysis(root)
    app.pack(fill='both', expand=True)
    root.mainloop()













