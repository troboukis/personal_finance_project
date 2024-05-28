import tkinter as tk
from tkinter import ttk
import calendar
import datetime

class CalendarPopup(tk.Toplevel):
    def __init__(self, parent, text_var):
        super().__init__(parent)
        self.text_var = text_var
        self.title("Select Date")
        
        self.cal = calendar.Calendar()
        self.year = datetime.datetime.now().year
        self.month = datetime.datetime.now().month
        
        self.init_ui()

    def init_ui(self):
        self.cal_frame = ttk.Frame(self)
        self.cal_frame.pack(pady=10, padx=10)

        self.header = ttk.Label(self.cal_frame, text=f"{calendar.month_name[self.month]} {self.year}", font=("Helvetica", 12))
        self.header.grid(row=0, column=0, columnspan=7)
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ttk.Label(self.cal_frame, text=day).grid(row=1, column=i)

        self.update_calendar()

        self.btn_prev = ttk.Button(self, text="<", command=self.prev_month)
        self.btn_prev.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_next = ttk.Button(self, text=">", command=self.next_month)
        self.btn_next.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def update_calendar(self):
        for widget in self.cal_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()

        month_days = self.cal.monthdayscalendar(self.year, self.month)
        for r, week in enumerate(month_days, start=2):
            for c, day in enumerate(week):
                if day != 0:
                    btn = ttk.Button(self.cal_frame, text=str(day), command=lambda d=day: self.set_date(d))
                    btn.grid(row=r, column=c)

    def set_date(self, day):
        selected_date = datetime.date(self.year, self.month, day).strftime("%d-%m-%Y")
        self.text_var.set(selected_date)
        self.destroy()

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.header.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.header.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self.update_calendar()
