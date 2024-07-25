from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class LoadDel:
    def __init__(self, root):
        self.root = root
        self.root.title("Load and Delete")
        self.root.geometry('400x600')
        self.root.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.position = StringVar()
        self.position.set("DR")
        self.position.trace("w", self.update_names)  # إضافة تتبع للتغيير في قيمة position

        self.r1 = Radiobutton(root, text='Dr', variable=self.position, value="DR", **label_style)
        self.r1.grid(row=0, column=0, padx=10, pady=10)
        self.r2 = Radiobutton(root, text='TA', variable=self.position, value="TA", **label_style)
        self.r2.grid(row=0, column=1, padx=10, pady=10)

        self.stuffnameLabel = Label(root, text="Name:", **label_style)
        self.stuffnameLabel.grid(row=1, column=0)
        self.stuffname = StringVar()
        self.stuffnameEntry = ttk.Combobox(root, textvariable=self.stuffname, **entry_style)
        self.stuffnameEntry.grid(row=1, column=1, padx=10, pady=10)

        self.departmentLabel = Label(root, text="Department:", **label_style)
        self.departmentLabel.grid(row=2, column=0)
        self.department = StringVar()
        self.departmentEntry = Entry(root, textvariable=self.department, **entry_style)
        self.departmentEntry.grid(row=2, column=1, padx=10, pady=10)

        self.levelLabel = Label(root, text="Level:", **label_style)
        self.levelLabel.grid(row=3, column=0)
        self.level = IntVar()
        self.levelEntry = ttk.Combobox(root, values=[1, 2, 3, 4], textvariable=self.level, **entry_style)
        self.levelEntry.grid(row=3, column=1, padx=10, pady=10)

        self.subjectLabel = Label(root, text="Subject:", **label_style)
        self.subjectLabel.grid(row=4, column=0)
        self.subject = StringVar()
        self.subjectEntry = Entry(root, textvariable=self.subject, **entry_style)
        self.subjectEntry.grid(row=4, column=1, padx=10, pady=10)

        self.sectionsLabel = Label(root, text="Sections:", **label_style)
        self.sectionsLabel.grid(row=5, column=0)
        self.sections = IntVar()
        self.sectionsEntry = Entry(root, textvariable=self.sections, **entry_style)
        self.sectionsEntry.grid(row=5, column=1, padx=10, pady=10)

        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=6, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('position', 'name', 'sections', 'Level', 'subject', 'Department', 'id'), show='headings')
        for col in ('position', 'name', 'sections', 'Level', 'subject', 'Department', 'id'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=9, column=0, columnspan=2, pady=10)

        self.load_data()
        self.update_names()  # تحديث الأسماء عند بدء البرنامج

    def insert_to_db(self):
        position = self.position.get()
        name = self.stuffname.get()
        sections = self.sections.get()
        Level = self.level.get()
        subject = self.subject.get()
        Department = self.department.get()

        if position and name and sections and Level and subject and Department:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV5"
                )
                cursor = db.cursor()
                sql = "INSERT INTO staff_info (position, name, sections, level, subject, department) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (position, name, sections, Level, subject, Department))
                db.commit()
                messagebox.showinfo("Success", "Data inserted successfully.")
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
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        cursor.execute("SELECT position, name, sections, level, subject, department, id FROM staff_info")
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
        values = self.tree.item(selected_item, 'values')
        #جوا الفاليو ترتيب العمود اللي فيه الاي دي في الواجهة
        record_id = values[6]
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM staff_info WHERE id = %s", (record_id,))
        db.commit()
        db.close()
        self.load_data()

    def update_names(self, *args):
        position = self.position.get()
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        cursor.execute("SELECT name FROM staff_info WHERE position = %s", (position,))
        names = cursor.fetchall()
        db.close()

        self.stuffnameEntry['values'] = [name[0] for name in names]
        if names:
            self.stuffname.set(names[0][0])  # تعيين القيمة الافتراضية لأول اسم في القائمة





