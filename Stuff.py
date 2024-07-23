from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class StuffPageADD:
    def __init__(self, master):
        self.master = master
        self.master.title('Stuff Form For Add')
        self.master.geometry('600x500')
        self.master.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.usernameLabel = Label(self.master, text="Name", **label_style)
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.username = StringVar()
        self.usernameEntry = Entry(self.master, textvariable=self.username, **entry_style)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.role = StringVar()
        self.role.set("DR")
        self.r1 = Radiobutton(self.master, text='Dr', variable=self.role, value="DR", bg='lightblue', font=('Arial', 12))
        self.r1.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.r2 = Radiobutton(self.master, text='TA', variable=self.role, value="TA", bg='lightblue', font=('Arial', 12))
        self.r2.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        self.EmailLabel = Label(self.master, text="Email", **label_style)
        self.EmailLabel.grid(row=2, column=0, padx=10, pady=10)
        self.Email = StringVar()
        self.EmailEntry = Entry(self.master, textvariable=self.Email, **entry_style)
        self.EmailEntry.grid(row=2, column=1, padx=10, pady=10)

        #self.idLabel = Label(self.master, text="ID Number", **label_style)
        #self.idLabel.grid(row=3, column=0, padx=10, pady=10)
        #self.idNumber = IntVar()
        #self.idNumberEntry = Entry(self.master, textvariable=self.idNumber, **entry_style)
        #self.idNumberEntry.grid(row=3, column=1, padx=10, pady=10)
        
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.master, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.master, columns=('SID', 'SName', 'Role', 'SEmail'), show='headings')
        self.tree.heading('SID', text='ID')
        self.tree.heading('SName', text='Name')
        self.tree.heading('Role', text='Role')
        self.tree.heading('SEmail', text='Email')
        self.tree.grid(row=6, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.load_data()

    def insert_to_db(self):
        SName = self.username.get()
        role = self.role.get()
        SEmail = self.Email.get()
       # SID = self.idNumber.get()

        if SName and role and SEmail :
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV5"
                )
                cursor = db.cursor()
                sql = "INSERT INTO add_stuff (SName, role, SEmail) VALUES (%s, %s, %s)"
                cursor.execute(sql, (SName, role, SEmail))
                db.commit()
                messagebox.showinfo("Registration Success", "User registered successfully.")
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
        cursor.execute("SELECT * FROM add_stuff")
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
        record_id = values[3]
        print(record_id)
        print(selected_item)
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV5"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM add_stuff WHERE SID = %s", (record_id ,))
        db.commit()
        db.close()
        self.load_data()

