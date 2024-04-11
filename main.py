import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style, DateEntry
from ttkbootstrap.constants import *
import datetime


def current_date():
    # Return the current date as a string
    return datetime.datetime.now().strftime("%h %m %Y, %H:%M")

def on_enter_frame(frame):
    # Define actions to take when a frame is entered
    if frame.winfo_name() == '!frame':
        print(f"Entering home")
    elif frame.winfo_name() == '!frame2':
        print("Entering Έσοδα")
    elif frame.winfo_name() == '!frame3':
        print("Entering Έξοδα")
    elif frame.winfo_name() == '!frame4':
        print("Entering Ανάλυση")

def show_frame(frame):
    frame.tkraise()
    on_enter_frame(frame)  # Call the function when the frame is raised

def main():
    root = tk.Tk()
    root.title("Διαχείριση προσωπικών οικονομικών")
    root.geometry("1366x768+0+0")

    style = Style(theme="solar")
    style.configure('W.TButton', font=('Roboto', 20, 'bold'), padding=20)


    # Creating frames for each section
    home_frame = tk.Frame(root)
    income_frame = tk.Frame(root)
    expenses_frame = tk.Frame(root)
    analysis_frame = tk.Frame(root)

    for frame in (home_frame, income_frame, expenses_frame, analysis_frame):
        frame.place(x=0, y=0, width=1366, height=768)

    # Add Date Label to Each Frame
    date_label_format = ("Courier", 12)
    tk.Label(home_frame, text=current_date(), font=date_label_format).place(x=10, y=10)
    tk.Label(income_frame, text=current_date(), font=date_label_format).place(x=10, y=10)
    tk.Label(expenses_frame, text=current_date(), font=date_label_format).place(x=10, y=10)
    tk.Label(analysis_frame, text=current_date(), font=date_label_format).place(x=10, y=10)

    # Home Frame Widgets
    tk.Label(home_frame, text="Διαχείριση προσωπικών οικονομικών", font=("Helvetica", 35), background="#FFDEAD", foreground="#000000").place(x=300, y=300)
    ttk.Button(home_frame, text='Έσοδα', style='primary.TButton', command=lambda: show_frame(income_frame)).place(x=325, y=400)
    ttk.Button(home_frame, text='Έξοδα', style='primary.TButton', command=lambda: show_frame(expenses_frame)).place(x=525, y=400)
    ttk.Button(home_frame, text='Ανάλυση', style='primary.TButton', command=lambda: show_frame(analysis_frame)).place(x=725, y=400)

    # Income Frame Widgets
    tk.Label(income_frame, text="Έσοδα", font=("Helvetica", 35)).pack(pady=200)
    ttk.Button(income_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame)).pack()

    # Expenses Frame Widgets
    tk.Label(expenses_frame, text="Έξοδα", font=("Helvetica", 35)).pack(pady=200)
    ttk.Button(expenses_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame)).pack()

    # Analysis Frame Widgets
    tk.Label(analysis_frame, text="Ανάλυση", font=("Helvetica", 35)).pack(pady=200)
    ttk.Button(analysis_frame, text="Back to Home", style='primary.TButton', command=lambda: show_frame(home_frame)).pack()

    # Start on the Home Frame
    show_frame(home_frame)

    root.mainloop()

main()
