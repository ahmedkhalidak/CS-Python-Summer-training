from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Level:
    def __init__(self, root):
        self.root = root
        self.root.title("LEVEL")
        self.root.geometry('400x600')
        self.root.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.levelLabel = Label(root, text="Level:", **label_style)
        self.levelLabel.grid(row=2, column=0)
        self.level = IntVar()
        self.levelEntry = ttk.Combobox(root, values=[1, 2, 3, 4], textvariable=self.level)
        self.levelEntry.grid(row=2, column=1, padx=10, pady=10)
        self.levelEntry.bind("<<ComboboxSelected>>", self.update_department_combobox)

        self.departmentLabel = Label(root, text="Department:", **label_style)
        self.departmentLabel.grid(row=3, column=0)
        self.department = StringVar()
        self.departmentEntry = ttk.Combobox(root, textvariable=self.department)
        self.departmentEntry.grid(row=3, column=1, padx=10, pady=10)

        self.sectionsLabel = Label(root, text="Number OF Sections:", **label_style)
        self.sectionsLabel.grid(row=5, column=0)
        self.sections = IntVar()
        self.sectionsEntry = Entry(root, textvariable=self.sections, **entry_style)
        self.sectionsEntry.grid(row=5, column=1, padx=10, pady=10)

        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=6, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('no.sections', 'Level', 'Department'), show='headings')
        for col in ('no.sections', 'Level', 'Department'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=9, column=0, columnspan=2, pady=10)

        self.load_data()
        self.update_department_combobox(None)

    def update_department_combobox(self, event):
        level = self.level.get()
        if level in [1, 2]:
            self.departmentEntry['values'] = ["AI", "GENERAL", "SE"]
        elif level in [3, 4]:
            self.departmentEntry['values'] = ["AI", "SE", "CS", "IS"]

    def insert_to_db(self):
        sections = self.sections.get()
        level = self.level.get()
        department = self.department.get()

        if sections and level and department:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV5"
                )
                cursor = db.cursor()
                sql = "INSERT INTO lvl (`no.sections`, Level, Department) VALUES (%s, %s, %s)"
                cursor.execute(sql, (sections, level, department))
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
        cursor.execute("SELECT `no.sections`, Level, Department FROM lvl")
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
        sections, level, department = values
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM lvl WHERE `no.sections` = %s AND Level = %s AND Department = %s", (sections, level, department))
        db.commit()
        db.close()
        self.load_data()

if __name__ == "__main__":
    root = Tk()
    app = Level(root)
    root.mainloop()
