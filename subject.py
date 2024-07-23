from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
class SubjectADD:
    def __init__(self, root):
        self.root = root
        self.root.title("Subject")
        self.root.geometry('400x200')
        self.root.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}
        # Labels and Entry widgets
        self.courseName = Label(root, text="Course Name:")
        self.courseName.grid(row=0, column=0)
        self.courseName=StringVar()
        self.courseNameEntry = Entry(root, width=20,textvariable=self.courseName)
        self.courseNameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.courseCode = Label(root, text="Course Code:")
        self.courseCode.grid(row=1, column=0)
        self.courseCode=StringVar()
        self.courseCodeEntry = Entry(root, width=20,textvariable=self.courseCode)
        self.courseCodeEntry.grid(row=1, column=1, padx=10, pady=10)

        self.level = Label(root, text="Level:")
        self.level.grid(row=2, column=0)
        self.level=IntVar()
        self.levelEntry = Entry(root, width=20,textvariable=self.level)
        self.levelEntry.grid(row=2, column=1, padx=10, pady=10)

        self.department = Label(root, text="Department:")
        self.department.grid(row=3, column=0)
        self.department=StringVar()
        self.departmentEntry = Entry(root, width=20,textvariable=self.department)
        self.departmentEntry.grid(row=3, column=1, padx=10, pady=10)


        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('Name', 'Code', 'Level', 'Department'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Code', text='Code')
        self.tree.heading('Level', text='Level')
        self.tree.heading('Department', text='Department')
        self.tree.grid(row=6, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.load_data()

    def insert_to_db(self):
        Name = self.courseName.get()
        Code = self.courseCode.get()
        Level = self.level.get()
        Department = self.department.get()

        if Name and Code and Level and Department:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseNew"
                )
                cursor = db.cursor()
                sql = "INSERT INTO Subject (Name, Code,Level, Department) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (Name, Code, Level, Department))
                db.commit()
                messagebox.showinfo("Success", " successfully.")
                db.close()
                self.load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def fetch_data(self):
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseNew"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Subject")
        rows = cursor.fetchall()
        db.close()
        return rows

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_item = self.tree.selection()[0]
        print(selected_item)
        print(self.tree.item(selected_item))
        values = self.tree.item(selected_item, 'values')
        record_id = values[1]
        print(record_id)
        print(selected_item)
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseNew"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM Subject WHERE Code = %s", (record_id ,))
        db.commit()
        db.close()
        self.load_data()

