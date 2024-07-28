from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class CreateTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Table")
        self.root.geometry('1400x900')

        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        self.time_slots = [
            "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", 
            "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00", 
            "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00", 
            "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
        ]

        self.create_widgets()
        self.load_levels_and_departments()

    def create_widgets(self):
        label_style = {'font': ('Arial', 12, 'bold')}

        self.input_frame = Frame(self.root)
        self.input_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

        self.levelLabel = Label(self.input_frame, text="Level:", **label_style)
        self.levelLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.level = IntVar()
        self.levelEntry = ttk.Combobox(self.input_frame, values=[1, 2, 3, 4], textvariable=self.level)
        self.levelEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.levelEntry.bind("<<ComboboxSelected>>", self.update_department_combobox)

        self.departmentLabel = Label(self.input_frame, text="Department:", **label_style)
        self.departmentLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.department = StringVar()
        self.departmentEntry = ttk.Combobox(self.input_frame, textvariable=self.department)
        self.departmentEntry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        self.departmentEntry.bind("<<ComboboxSelected>>", self.create_table)

        self.createButton = Button(self.input_frame, text="Create", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.create_table)
        self.createButton.grid(row=2, column=0, columnspan=2, pady=20)

        self.table_frame_outer = Frame(self.root)
        self.table_frame_outer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.table_canvas = Canvas(self.table_frame_outer)
        self.table_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar_v = Scrollbar(self.table_frame_outer, orient=VERTICAL, command=self.table_canvas.yview)
        self.scrollbar_v.pack(side=RIGHT, fill=Y)
        self.scrollbar_h = Scrollbar(self.root, orient=HORIZONTAL, command=self.table_canvas.xview)
        self.scrollbar_h.grid(row=1, column=0, sticky='ew')

        self.table_canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)

        self.table_frame = Frame(self.table_canvas)
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor='nw')

        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=4)  
        self.root.grid_columnconfigure(1, weight=1)  

    def load_levels_and_departments(self):
        self.levels_departments = {}
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBaseV5'
            )
            cursor = connection.cursor()
            query = "SELECT Level, Department, `no.sections` FROM lvl"
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                level, department, sections = row
                if level not in self.levels_departments:
                    self.levels_departments[level] = {}
                self.levels_departments[level][department] = sections
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def update_department_combobox(self, event):
        level = self.level.get()
        if level in self.levels_departments:
            departments = list(self.levels_departments[level].keys())
            self.departmentEntry['values'] = departments

    def create_table(self, event=None):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        level = self.level.get()
        department = self.department.get()
        sections = self.levels_departments[level][department]

        
        title = f"Level {level} - {department}"
        titleLabel = Label(self.table_frame, text=title, font=('Arial', 16, 'bold'))
        titleLabel.grid(row=0, column=0, columnspan=len(self.time_slots) + 2, pady=10)

        Label(self.table_frame, text="Day", borderwidth=1, relief="solid", width=10).grid(row=1, column=0, sticky="nsew")
        Label(self.table_frame, text="Sections", borderwidth=1, relief="solid", width=15).grid(row=1, column=1, sticky="nsew")

        for col, time_slot in enumerate(self.time_slots):
            Label(self.table_frame, text=time_slot, borderwidth=1, relief="solid", width=15).grid(row=1, column=col+2, sticky="nsew")

        current_row = 2
        for day in self.days:
            day_label = Label(self.table_frame, text=day, borderwidth=1, relief="solid", width=10)
            day_label.grid(row=current_row, column=0, rowspan=sections, sticky="nsew")

            for section in range(1, sections + 1):
                Label(self.table_frame, text=f"Section {section}", borderwidth=1, relief="solid", width=15).grid(row=current_row, column=1, sticky="nsew")

                for col in range(1, len(self.time_slots) + 1):
                    entry = Entry(self.table_frame, width=15, borderwidth=1, relief="solid")
                    entry.grid(row=current_row, column=col+1, sticky="nsew")

                current_row += 1

            
            separator = Frame(self.table_frame, bg='black', height=2, bd=1, relief="solid")
            separator.grid(row=current_row, column=0, columnspan=len(self.time_slots) + 2, sticky="nsew", pady=(5, 5))

            current_row += 1

        for col in range(len(self.time_slots) + 2):
            self.table_frame.columnconfigure(col, weight=1)
        for row in range(current_row):
            self.table_frame.rowconfigure(row, weight=1)
