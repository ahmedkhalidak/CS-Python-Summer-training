from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector



class LoadDel:
    def __init__(self, root):
        self.root = root
        self.root.title("load")
        self.root.geometry('400x200')
        self.root.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}
        # Labels and Entry widgets

        # self.stuffname = Label(root, text="name:")
        # self.stuffname.grid(row=0, column=0)
        # self.stuffname=StringVar()
        # db.cursor().execute
        # self.stuffnameEntry = ttk.Combobox(root, values=["ahmed" ,"mohammed"],textvariable=self.stuffname)
        # # Entry(root, width=20 ,textvariable=self.stuffname)
        # self.stuffnameEntry.grid(row=0, column=1, padx=10, pady=10)


        self.position = StringVar()
        self.position.set("DR")
        self.r1 = Radiobutton(root, text='Dr', variable=self.position, value="DR", bg='lightblue', font=('Arial', 12))
        self.r1.grid(row=0, column=0, padx=10, pady=10)
        self.r2 = Radiobutton(root, text='TA', variable=self.position, value="TA", bg='lightblue', font=('Arial', 12))
        self.r2.grid(row=0, column=1, padx=10, pady=10)



        self.stuffname = Label(root, text="name:")
        self.stuffname.grid(row=1, column=0)
        self.stuffname=StringVar()
        self.stuffnameEntry = ttk.Combobox(root, values=["ahmed" ,"mohammed"],textvariable=self.stuffname)
        # Entry(root, width=20 ,textvariable=self.stuffname)
        self.stuffnameEntry.grid(row=1, column=1, padx=10, pady=10)


        self.department = Label(root, text="Department:")
        self.department.grid(row=2, column=0)
        self.department=StringVar()
        self.departmentEntry = Entry(root, width=20,textvariable=self.department)
        self.departmentEntry.grid(row=2, column=1, padx=10, pady=10)


        self.level = Label(root, text="Level:")
        self.level.grid(row=3, column=0)
        self.level=IntVar()
        self.levelEntry = ttk.Combobox(root, values=[1,2,3,4],textvariable=self.level)
        self.levelEntry.grid(row=3, column=1, padx=10, pady=10)


        self.subject = Label(root, text="subject:")
        self.subject.grid(row=4, column=0)
        self.subject=StringVar()
        self.subjectEntry = Entry(root, width=20,textvariable=self.subject)
        self.subjectEntry.grid(row=4, column=1, padx=10, pady=10)


        self.sections = Label(root, text="sections:")
        self.sections.grid(row=5, column=0)
        self.sections=IntVar()
        self.sectionsEntry = Entry(root, width=20,textvariable=self.sections)
        self.sectionsEntry.grid(row=5, column=1, padx=10, pady=10)



        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=6, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=7, column=0, columnspan=2, pady=10)


        self.tree = ttk.Treeview(self.root, columns=( 'position', 'name', 'sections' ,'Level', 'subject' , 'Department', 'id'), show='headings')
        self.tree.heading('position', text='position')
        self.tree.heading('name', text='name')
        self.tree.heading('sections', text='sections')
        self.tree.heading('Level', text='Level')
        self.tree.heading('subject', text='subject')
        self.tree.heading('Department', text='Department')
        self.tree.heading('id', text='id')
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)


        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=9, column=0, columnspan=2, pady=10)

        self.load_data()

    def insert_to_db(self):
        position = self.position.get()
        name = self.stuffname.get()
        sections = self.sections.get()
        Level = self.level.get()
        subject = self.subject.get()
        Department = self.department.get()

        if position and name  and sections and Level  and subject and Department:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV5"
                )
                cursor = db.cursor()
                sql = "INSERT INTO staff_info ( position ,name, sections ,level, subject , department) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, ( position , name, sections ,Level, subject , Department))
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
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        # cursor.execute("SELECT * FROM staff_info")
        cursor.execute("SELECT position ,name, sections ,level, subject , department ,id FROM staff_info")
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
        # جوا الفاليو ترتيب العمود اللي فيه الاي دي في الواجهة
        record_id = values[6]
        print(record_id)
        print(selected_item)
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM staff_info WHERE id = %s", (record_id ,))
        db.commit()
        db.close()
        self.load_data()


