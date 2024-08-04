from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Load:
    def __init__(self, root):
        self.root = root
        self.root.title("Load")
        self.root.geometry('400x400')
        self.root.configure(bg='lightblue')

        # Fetch data from instructor table
        self.instructor_dict = {}
        self.departments = self.fetch_departments()
        self.department_dict = {name: dept_id for dept_id, name in self.departments}
        self.levels_dic = {}

        self.roleLabel = Label(root, text="Role:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.roleLabel.grid(row=1, column=0)
        self.roleVar = StringVar()
        self.roleEntry = ttk.Combobox(root, textvariable=self.roleVar)
        self.roleEntry['values'] = ["Dr", "TA"]
        self.roleEntry.grid(row=1, column=1, padx=10, pady=10)
        self.roleEntry.bind("<<ComboboxSelected>>", self.fetch_instructors)

        self.instructortidLabel = Label(root, text="Instructor:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.instructortidLabel.grid(row=2, column=0)
        self.instructortidVar = StringVar()
        self.instructortidEntry = ttk.Combobox(root, textvariable=self.instructortidVar)
        self.instructortidEntry['values'] = [name for name in self.instructor_dict.keys()]
        self.instructortidEntry.grid(row=2, column=1, padx=10, pady=10)
        
        self.departmentLabel = Label(self.root, text="Department:" , bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentLabel.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.department = StringVar()
        self.departmentEntry = ttk.Combobox(self.root, textvariable=self.department)
        self.departmentEntry['values'] = [name for name in self.department_dict.keys()]
        self.departmentEntry.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        self.departmentEntry.bind("<<ComboboxSelected>>", self.load_levels)

        self.levelLabel = Label(self.root, text="Level:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.levelLabel.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.level = IntVar()
        self.levelEntry = ttk.Combobox(self.root, textvariable=self.level) 
        self.levelEntry.grid(row=4, column=1, padx=10, pady=10, sticky=W)
        self.levelEntry.bind("<<ComboboxSelected>>", self.fetch_subjects)
        # Fetch data from subject table
        self.subject_dict = {}

        self.subjectLabel = Label(root, text="Subject:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.subjectLabel.grid(row=5, column=0)
        self.subjectVar = StringVar()
        self.subjectEntry = ttk.Combobox(root, textvariable=self.subjectVar)
        self.subjectEntry.grid(row=5, column=1, padx=10, pady=10)

        self.sectionsLabel = Label(root, text="Number of Sections:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.sectionsLabel.grid(row=6, column=0)
        self.sectionsVar = IntVar()
        self.sectionsEntry = Entry(root, textvariable=self.sectionsVar)
        self.sectionsEntry.grid(row=6, column=1, padx=10, pady=10)

        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=7, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=8, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=( 'instructortid', 'subject', 'sections'), show='headings')
        for col in ( 'instructortid', 'subject', 'sections'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=9, column=0, columnspan=2, pady=20)

    def fetch_instructors(self,event):
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
            sql = "SELECT ID, Name FROM instructor where Role = %s" 
            cursor.execute(sql , (role, ))
            rows = cursor.fetchall()
            self.instructor_dict = {name: instructor_id for instructor_id, name in rows}
            self.instructortidEntry['values'] = [name for name in self.instructor_dict.keys()]
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

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
        
    def load_levels(self,event):
        self.levels_dic.clear()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBasev8'
            )
            cursor = connection.cursor()
            # Load levels and sections
            dept_id=self.department_dict[self.department.get()]
            dept_id=str(dept_id)
            query_levels = "SELECT ID,  levelNo, No_sections FROM level WHERE Dept_ID = " + dept_id
            cursor.execute(query_levels)
            data = cursor.fetchall()
            self.levels_dic = {levelNo: [ID, No_sections] for ID,levelNo,No_sections in data}
            self.levelEntry['values'] = [levelNo for levelNo in self.levels_dic.keys()]
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_subjects(self, event):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            id = self.level.get()
            cursor.execute("SELECT ID, Name FROM subject where level_ID = %s", (id,))
            rows = cursor.fetchall()
            self.subject_dict = {Name: ID for ID,Name in rows}
            self.subjectEntry['values'] = [Name for Name in self.subject_dict.keys()]
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def insert_to_db(self):
        instr_id = self.instructor_dict[self.instructortidVar.get()]
        subj_id = self.subject_dict[self.subjectVar.get()]
        No_sections = self.sectionsVar.get()

        if instr_id and subj_id and No_sections:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV8"
                )
                cursor = db.cursor()
                sql = "INSERT INTO instructorload (instructor_ID, subject_ID, No_sections) VALUES (%s, %s, %s)"
                cursor.execute(sql, (instr_id, subj_id, No_sections))
                db.commit()
                messagebox.showinfo("Success", "Record inserted successfully.")
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
            database="PDataBaseV8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM instructorload")
        rows = cursor.fetchall()
        db.close()
        return rows

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

if __name__ == "__main__":
    root = Tk()
    app = Load(root)
    root.mainloop()
