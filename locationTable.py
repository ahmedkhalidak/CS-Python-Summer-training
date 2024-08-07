from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

class LocationTable:
    def __init__(self, master):
        self.master = master
        self.master.title('Location Schedule')
        self.master.geometry('700x600')  # تقليل العرض إلى حجم أصغر
        self.master.configure(bg='lightblue')

        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        self.time_slots = [
            "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
            "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00",
            "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00",
            "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
        ]

        self.setup_widgets()

    def setup_widgets(self):
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}

        self.input_frame = Frame(self.master, bg='lightblue')
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.dayLabel = Label(self.input_frame, text="Day:", **label_style)
        self.dayLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.day = StringVar()
        self.dayEntry = ttk.Combobox(self.input_frame, textvariable=self.day)
        self.dayEntry['values'] = self.days  # Populate days here
        self.dayEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        self.load_button = Button(self.input_frame, text="Load", command=self.load_schedule)
        self.load_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

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

    def display_schedule(self, schedule_data, locations):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        title = f"Schedule for {self.day.get()}"
        titleLabel = Label(self.table_frame, text=title, font=('Arial', 14, 'bold'), bg='lightblue')
        titleLabel.grid(row=0, column=0, columnspan=len(self.time_slots) + 2, pady=10)

        # Headers
        Label(self.table_frame, text="Location/Time", bg='lightblue', font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=15, height=3).grid(row=1, column=0, sticky="nsew")
        for col, time_slot in enumerate(self.time_slots):
            Label(self.table_frame, text=time_slot, bg='lightblue', font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=12, height=3).grid(row=1, column=col+1, sticky="nsew")

        # Organize schedule data by location
        location_to_schedule = {loc: {i: '' for i in range(len(self.time_slots))} for loc in locations}

        for loc_name, time_start, sub_name, level_id, section_id in schedule_data:
            normalized_time_start = self.normalize_time_format(time_start)
            
            if normalized_time_start in self.time_slots:
                start_index = self.time_slots.index(normalized_time_start)
                end_index = start_index + 4  # 4 periods for a 2-hour session

                for col in range(start_index, min(end_index, len(self.time_slots))):
                    location_to_schedule[loc_name][col] = f"{sub_name} (Level: {level_id}, Section: {section_id})"

        # Create rows for each location
        for row_index, loc_name in enumerate(locations, start=2):
            loc_label = Label(self.table_frame, text=loc_name, bg='lightblue', font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", width=15, height=3)
            loc_label.grid(row=row_index, column=0, sticky="nsew")

            for col in range(len(self.time_slots)):
                cell = Label(self.table_frame, text=location_to_schedule[loc_name][col], bg='lightblue', font=('Arial', 10), borderwidth=1, relief="solid", width=12, height=3)
                cell.grid(row=row_index, column=col+1, sticky="nsew")

        # Adjust column and row configuration
        for col in range(len(self.time_slots) + 1):
            self.table_frame.columnconfigure(col, weight=1)
        for row in range(len(locations) + 2):
            self.table_frame.rowconfigure(row, weight=1)

        # Update Canvas scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def normalize_time_format(self, time_str):
        if len(time_str) == 1:  # Handle cases like '9' by converting to '9:00 - 9:30'
            time_str = f"{time_str}:00 - {str(int(time_str) + 2)}:00"
        return time_str

    def load_schedule(self):
        day = self.day.get()
        if not day:
            return

        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='PDataBasev8',
                user='root',
                password=''  # Replace with your MySQL password
            )
            if connection.is_connected():
                cursor = connection.cursor()
                
                # Get schedule data for the selected day with additional info
                query_schedule = """
                SELECT s.loc_name, s.time_start, s.sub_name, s.level_ID, s.sections
                FROM schedule s
                WHERE s.Day = %s
                """
                cursor.execute(query_schedule, (day,))
                schedule_data = cursor.fetchall()

                # Get all locations from the Location table
                query_locations = "SELECT Name FROM Location"
                cursor.execute(query_locations)
                locations = [loc[0] for loc in cursor.fetchall()]

                self.display_schedule(schedule_data, locations)

        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    root = Tk()
    app = LocationTable(root)
    root.mainloop()
