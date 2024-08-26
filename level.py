from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Level:
    def __init__(self, frame):
        self.frame = frame
        self.frame.configure(bg='lightblue')

        self.departments = self.fetch_departments()
        self.department_dict = {name: dept_id for dept_id, name in self.departments}

        self.departmentidLabel = Label(frame, text="Department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentidLabel.grid(row=0, column=0)
        self.departmentidVar = StringVar()
        self.departmentidEntry = ttk.Combobox(frame, textvariable=self.departmentidVar)
        self.departmentidEntry['values'] = [name for name in self.department_dict.keys()]
        self.departmentidEntry.grid(row=0, column=1, padx=10, pady=10)

        self.levelLabel = Label(frame, text="Level:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.levelLabel.grid(row=1, column=0)
        self.levelVar = IntVar()
        self.levelEntry = ttk.Combobox(frame, textvariable=self.levelVar, values=[1, 2, 3, 4])
        self.levelEntry.grid(row=1, column=1, padx=10, pady=10)

        self.sectionsLabel = Label(frame, text="Number of Sections:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.sectionsLabel.grid(row=2, column=0)
        self.sectionsVar = IntVar()
        self.sectionsEntry = Entry(frame, textvariable=self.sectionsVar)
        self.sectionsEntry.grid(row=2, column=1, padx=10, pady=10)

        self.submitButton = Button(frame, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=3, column=0, columnspan=2, pady=20)

        self.loadButton = Button(frame, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(frame, columns=('id', 'department', 'level', 'sections'), show='headings')
        for col in ('id', 'department', 'level', 'sections'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(frame, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=10, column=0, columnspan=2, pady=10)

    def fetch_departments(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT ID, Name FROM department")
            rows = cursor.fetchall()
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def find_next_available_id(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT ID FROM level ORDER BY ID")
            ids = [row[0] for row in cursor.fetchall()]
            db.close()

            next_id = 1
            for id in ids:
                if next_id < id:
                    break
                next_id = id + 1
            return next_id
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return 1

    def department_exists(self, department_name, level_no):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM level WHERE Dept_ID = %s AND levelNo = %s", (self.department_dict.get(department_name), level_no))
            count = cursor.fetchone()[0]
            db.close()
            return count > 0
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False

    def insert_to_db(self):
        department_name = self.departmentidVar.get()
        levelNo = self.levelVar.get()
        No_sections = self.sectionsVar.get()

        if department_name and levelNo and No_sections:
            if self.department_exists(department_name, levelNo):
                messagebox.showwarning("Duplicate Error", "This department and level combination already exists.")
                return

            dept_id = self.department_dict.get(department_name)

            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV8"
                )
                cursor = db.cursor()

                next_id = self.find_next_available_id()

                sql = "INSERT INTO level (Dept_ID, levelNo, No_sections, ID) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (dept_id, levelNo, No_sections, next_id))
                db.commit()
                messagebox.showinfo("Success", f"Record inserted successfully with ID {next_id}.")
                db.close()
                self.load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def fetch_data(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            query = """
            SELECT level.ID, department.Name, level.levelNo, level.No_sections
            FROM level
            JOIN department ON level.Dept_ID = department.ID
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        record_id = values[0]
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("DELETE FROM level WHERE ID = %s", (record_id,))
            db.commit()
            db.close()
            self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    root = Tk()
    app = Level(root)
    root.mainloop()
