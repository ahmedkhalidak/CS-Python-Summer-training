from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class department:
    def __init__(self, root):
        self.frame = Frame(root, bg='lightblue', width=600, height=600)
        self.frame.pack(fill=BOTH, expand=True)

# استخدام pack بدلاً من grid
        self.departmentidLabel = Label(self.frame, text="department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentidLabel.pack(anchor='w', padx=10, pady=10)

        self.departmentidVar = StringVar()
        self.departmentidEntry = Entry(self.frame, textvariable=self.departmentidVar)
        self.departmentidEntry.pack(padx=10, pady=10)

        self.submitButton = Button(self.frame, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.pack(pady=20)

        self.loadButton = Button(self.frame, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=('id', 'name'), show='headings')
        for col in ('id', 'name'):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20, fill=BOTH, expand=True)

        self.deleteButton = Button(self.frame, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.pack(pady=10)
    def fetch_departments(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="pdatabasev8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT ID, Name FROM department ORDER BY ID")
            rows = cursor.fetchall()
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def find_next_available_id(self):
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="pdatabasev8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT ID FROM department ORDER BY ID")
        ids = [row[0] for row in cursor.fetchall()]
        db.close()

        # Find the lowest missing ID
        next_id = 1
        for id in ids:
            if next_id < id:
                break
            next_id = id + 1
        return next_id

    def department_exists(self, dept_name):
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="pdatabasev8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM department WHERE Name = %s", (dept_name,))
        count = cursor.fetchone()[0]
        db.close()
        return count > 0

    def insert_to_db(self):
        dept = self.departmentidVar.get()
        if dept:
            if self.department_exists(dept):
                messagebox.showwarning("Duplicate Error", "This department already exists.")
                return
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="pdatabasev8"
                )
                cursor = db.cursor()

                # Find the next available ID
                next_id = self.find_next_available_id()

                # Insert the department with the found ID
                cursor.execute("INSERT INTO department (ID, Name) VALUES (%s, %s)", (next_id, dept))
                db.commit()
                messagebox.showinfo("Success", f"Record inserted successfully with ID {next_id}.")
                db.close()
                self.load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_departments()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return
        values = self.tree.item(selected_item[0], 'values')
        record_id = values[0]
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="pdatabasev8"
            )
            cursor = db.cursor()
            cursor.execute("DELETE FROM department WHERE ID = %s", (record_id,))
            db.commit()
            db.close()
            self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    root = Tk()
    app = department(root)
    root.mainloop()
