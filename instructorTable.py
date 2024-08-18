from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class InstructorTable:
    def __init__(self, master):
        self.master = master
        self.master.title('Instructor Schedule')
        self.master.geometry('1000x600')
        self.master.configure(bg='lightblue')

        self.time_slots = [
            "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
            "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00",
            "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00",
            "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
        ]
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

        self.instructor_dict = {}
        self.setup_widgets()
        self.fetch_subjects()
        self.fetch_locations()

    def setup_widgets(self):
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}

        self.roleLabel = Label(self.master, text="Role:", **label_style)
        self.roleLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.roleVar = StringVar()
        self.roleEntry = ttk.Combobox(self.master, textvariable=self.roleVar)
        self.roleEntry['values'] = ["Dr", "TA"]
        self.roleEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.roleEntry.bind("<<ComboboxSelected>>", self.fetch_instructors)

        self.instructortidLabel = Label(self.master, text="Instructor:", **label_style)
        self.instructortidLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.instructortidVar = StringVar()
        self.instructortidEntry = ttk.Combobox(self.master, textvariable=self.instructortidVar)
        self.instructortidEntry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        # Update this line to use load_schedule instead of fetch_schedule
        self.instructortidEntry.bind("<<ComboboxSelected>>", self.load_schedule)

        self.loadButton = Button(self.master, text="Load", command=self.load_schedule, bg='lightgreen')
        self.loadButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.canvas = Canvas(self.master, bg='lightblue')
        self.canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.scroll_x = Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.table_frame = Frame(self.canvas, bg='lightblue')
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.table_frame.bind("<Configure>", self.on_frame_configure)

        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fetch_locations(self):
        self.instructor_dict.clear()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "SELECT ID, Name FROM location"
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.location_dict = {id: name for id, name in rows}
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_subjects(self):
        self.instructor_dict.clear()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "SELECT ID, Name FROM subject"
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.subject_dict = {id: name for id, name in rows}
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_instructors(self, event):
        self.instructor_dict.clear()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            role = self.roleVar.get()
            cursor = db.cursor()
            sql = "SELECT ID, Name FROM Instructor WHERE Role = %s"
            cursor.execute(sql, (role,))
            rows = cursor.fetchall()
            self.instructor_dict = {name: instructor_id for instructor_id, name in rows}
            self.instructortidEntry['values'] = [name for name in self.instructor_dict.keys()]
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def normalize_time_format(self, time_str):
        for slot in self.time_slots:
            start_time, end_time = slot.split(" - ")
            if time_str == start_time:
                return slot
        return time_str

    def load_schedule(self):
        instructor_name = self.instructortidVar.get()
        instructor_id = self.instructor_dict.get(instructor_name)
        
        if instructor_id is None:
            messagebox.showerror("Error", "Instructor not selected")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "SELECT subject_ID, Location_ID, Day, time_start FROM schedule WHERE instructor_ID = %s"
            cursor.execute(sql, (instructor_id,))
            rows = cursor.fetchall()
            db.close()

            self.display_schedule(rows)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def display_schedule(self, schedule_data):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Title
        title = "Instructor Schedule"
        titleLabel = Label(self.table_frame, text=title, font=('Arial', 14, 'bold'), bg='lightblue')
        titleLabel.grid(row=0, column=0, columnspan=len(self.time_slots) + 1, pady=10)

        # Header
        Label(self.table_frame, text="Day/Time", bg='lightblue', font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=15, height=3).grid(row=1, column=0, sticky="nsew")
        for col, time_slot in enumerate(self.time_slots):
            Label(self.table_frame, text=time_slot, bg='lightblue', font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=12, height=3).grid(row=1, column=col+1, sticky="nsew")

        # Initialize schedule structure
        schedule_grid = {day: {i: '' for i in range(len(self.time_slots))} for day in self.days}

        for subject_ID, Location_ID, Day, time_start in schedule_data:
            normalized_time = self.normalize_time_format(time_start)
            start_col = self.time_slots.index(normalized_time) + 1
            day_index = self.days.index(Day) + 2

            # Assuming a 2-hour block, which spans 4 time slots
            end_col = min(start_col + 4, len(self.time_slots) + 1)

            cell_content = f"{self.subject_dict.get(subject_ID, 'Unknown Subject')}\n{self.location_dict.get(Location_ID, 'Unknown Location')}"
            
            for col in range(start_col, end_col):
                schedule_grid[self.days[day_index - 2]][col - 1] = cell_content

        # Display schedule
        for row_index, day in enumerate(self.days, start=2):
            Label(self.table_frame, text=day, bg='lightblue', font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=15, height=3).grid(row=row_index, column=0, sticky="nsew")

            col = 1
            while col <= len(self.time_slots):
                cell_content = schedule_grid[day][col - 1]
                merged_col_span = 1
                while (col + merged_col_span <= len(self.time_slots) and
                    schedule_grid[day][col + merged_col_span - 1] == cell_content):
                    merged_col_span += 1

                Label(self.table_frame, text=cell_content, bg='white', font=('Arial', 9, 'bold'), borderwidth=1, relief="solid", width=12, height=3).grid(row=row_index, column=col, columnspan=merged_col_span, sticky="nsew")
                col += merged_col_span

        self.table_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = Tk()
    app = InstructorTable(root)
    root.mainloop()
