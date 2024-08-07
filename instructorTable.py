from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class InstructorTable:
    def __init__(self, master):
        self.master = master
        self.master.title('Instructor Schedule')
        self.master.geometry('1000x600')  # زيادة العرض إلى حجم أكبر
        self.master.configure(bg='lightblue')

        self.instructor_dict = {}
        self.setup_widgets()
        self.load_data()

    def setup_widgets(self):
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.roleLabel = Label(self.master, text="Role:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.roleLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.roleVar = StringVar()
        self.roleEntry = ttk.Combobox(self.master, textvariable=self.roleVar)
        self.roleEntry['values'] = ["Dr", "TA"]
        self.roleEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.roleEntry.bind("<<ComboboxSelected>>", self.fetch_instructors)

        self.instructortidLabel = Label(self.master, text="Instructor:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.instructortidLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.instructortidVar = StringVar()
        self.instructortidEntry = ttk.Combobox(self.master, textvariable=self.instructortidVar)
        self.instructortidEntry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        self.instructortidEntry.bind("<<ComboboxSelected>>", self.fetch_schedule)

        # Create a Canvas widget and a Frame for the table
        self.canvas = Canvas(self.master, bg='lightblue')
        self.canvas.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Create a horizontal scrollbar linked to the Canvas
        self.scroll_x = Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Create a Frame inside the Canvas to hold the table
        self.table_frame = Frame(self.canvas, bg='lightblue')

        # Add the Frame to the Canvas
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Update the Canvas scrollregion
        self.table_frame.bind("<Configure>", self.on_frame_configure)

        # Configure row and column weights
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def on_frame_configure(self, event):
        # Update the scrollregion of the Canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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

    def fetch_schedule(self, event=None):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

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
            sql = """
            SELECT Day, time_start, sub_name
            FROM schedule
            WHERE instructor_ID = %s
            """
            cursor.execute(sql, (instructor_id,))
            rows = cursor.fetchall()
            db.close()

            self.display_schedule(rows)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def display_schedule(self, schedule_data):
        title = f"Schedule for {self.instructortidVar.get()}"
        titleLabel = Label(self.table_frame, text=title, font=('Arial', 16, 'bold'), bg='lightblue')
        titleLabel.grid(row=0, column=0, columnspan=len(self.time_slots) + 2, pady=10)

        Label(self.table_frame, text="Day", bg='lightblue', font=('Arial', 12, 'bold'), borderwidth=1, relief="solid", width=15, height=3).grid(row=1, column=0, sticky="nsew")
        Label(self.table_frame, text="Time Slot", bg='lightblue', font=('Arial', 12, 'bold'), borderwidth=1, relief="solid", width=15, height=3).grid(row=1, column=1, sticky="nsew")

        for col, time_slot in enumerate(self.time_slots):
            Label(self.table_frame, text=time_slot, bg='lightblue', font=('Arial', 12, 'bold'), borderwidth=1, relief="solid", width=15, height=3).grid(row=1, column=col+2, sticky="nsew")

        current_row = 2
        schedule_dict = {day: {time_slot: "" for time_slot in self.time_slots} for day in self.days}

        for day, time_start, sub_name in schedule_data:
            if day not in schedule_dict:
                continue
            start_index = self.time_slots.index(time_start)
            end_index = start_index + 4  # 4 periods for a 2-hour session

            for col in range(start_index, min(end_index, len(self.time_slots))):
                schedule_dict[day][self.time_slots[col]] = sub_name

        for day, slots in schedule_dict.items():
            day_label = Label(self.table_frame, text=day, bg='lightblue', font=('Arial', 12, 'bold'), borderwidth=1, relief="solid", width=15, height=3)
            day_label.grid(row=current_row, column=0, rowspan=1, sticky="nsew")

            for col, time_slot in enumerate(self.time_slots):
                subject = slots.get(time_slot, "")
                entry = Entry(self.table_frame, width=20, borderwidth=1, relief="solid", font=('Arial', 12))
                entry.grid(row=current_row, column=col+2, sticky="nsew")
                entry.insert(0, subject)

            current_row += 1

        for col in range(len(self.time_slots) + 2):
            self.table_frame.columnconfigure(col, weight=1)
        for row in range(current_row):
            self.table_frame.rowconfigure(row, weight=1)

    def load_data(self):
        self.time_slots = [
            "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
            "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00",
            "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00",
            "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
        ]
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

if __name__ == "__main__":
    root = Tk()
    app = InstructorTable(root)
    root.mainloop()
