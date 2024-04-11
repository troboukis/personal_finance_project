import tkinter as tk
import ttkbootstrap as bttk
from ttkbootstrap import Style
import datetime
from expenses import ExpensesFrame

def current_date():
    # Return the current date as a string
    return datetime.datetime.now().strftime("%b %d %Y, %H:%M")

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
    income_frame = tk.Frame(root)
    expenses_frame = ExpensesFrame(root)
    analysis_frame = tk.Frame(root)

    frames = [home_frame, income_frame, expenses_frame, analysis_frame]
    for frame in frames:
        frame.grid(row=0, column=0, sticky='nsew')

    # Configuring grid layout on root
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Add Date Label to Each Frame using grid
    date_label_format = ("Courier", 12)
    for i, frame in enumerate(frames):
        tk.Label(frame, text=current_date(), font=date_label_format)\
            .grid(row=0, column=0, sticky='w', padx=10, pady=10)

    # Home Frame Widgets
    tk.Label(home_frame, text="Διαχείριση προσωπικών οικονομικών", font=("Helvetica", 35), background="#FFDEAD", foreground="#000000").grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=50)
    # default separator style
    separator = bttk.Separator(home_frame, orient='horizontal')
    separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(170, 90))

    bttk.Button(home_frame, text='Έσοδα', style='primary.TButton', command=lambda: show_frame(income_frame))\
        .grid(row=2, column=0, padx=20, pady=40, sticky='ew')
    bttk.Button(home_frame, text='Έξοδα', style='primary.TButton', command=lambda: show_frame(expenses_frame))\
        .grid(row=2, column=1, padx=20, pady=20, sticky='ew')
    bttk.Button(home_frame, text='Ανάλυση', style='primary.TButton', command=lambda: show_frame(analysis_frame))\
        .grid(row=2, column=2, padx=20, pady=20, sticky='ew')

    home_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="group1")
    home_frame.grid_rowconfigure(1, weight=1)

    # Income Frame Widgets
    tk.Label(income_frame, text="Έσοδα", font=("Helvetica", 35))\
        .grid(row=10, column=0, sticky='ew', padx=20, pady=20)
    bttk.Button(income_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame))\
        .grid(row=10, column=0, sticky='ew')

    # Expenses Frame Widgets are already configured in ExpensesFrame class using grid
    # Adding the back to home button in the expenses frame (you need to adjust this in the ExpensesFrame class if not done)
    tk.Label(income_frame, text="Έσοδα", font=("Helvetica", 35)).grid(row=10, column=0, sticky='ew', padx=10, pady=200)
    bttk.Button(expenses_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame)).grid(row=10, column=0, columnspan=2, sticky='ew')

    # Analysis Frame Widgets
    tk.Label(analysis_frame, text="Ανάλυση", font=("Helvetica", 35)).grid(row=1, column=0, sticky='ew', padx=10, pady=200)
    bttk.Button(analysis_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame)).grid(row=10, column=0, sticky='ew')
    

    # Start on the Home Frame
    show_frame(home_frame)

    root.mainloop()

if __name__ == "__main__":
    main()