from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class StuffPageADD:
    def __init__(self, master):
        self.master = master
        self.master.title('Stuff Form For Add')
        self.master.geometry('600x500')
        self.master.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.nameLabel = Label(self.master, text="Name", **label_style)
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.name = StringVar()
        self.nameEntry = Entry(self.master, textvariable=self.name, **entry_style)
        self.nameEntry.grid(row=0, column=1, padx=10, pady=10)

        self. position = StringVar()
        self. position.set("DR")
        self.r1 = Radiobutton(self.master, text='Dr', variable=self. position, value="DR", bg='lightblue', font=('Arial', 12))
        self.r1.grid(row=1, column=0, padx=10, pady=10)
        self.r2 = Radiobutton(self.master, text='TA', variable=self. position, value="TA", bg='lightblue', font=('Arial', 12))
        self.r2.grid(row=1, column=1, padx=10, pady=10)
        
        self.emailLabel = Label(self.master, text="Email", **label_style)
        self.emailLabel.grid(row=2, column=0, padx=10, pady=10)
        self.email = StringVar()
        self.emailEntry = Entry(self.master, textvariable=self.email, **entry_style)
        self.emailEntry.grid(row=2, column=1, padx=10, pady=10)

        #self.idLabel = Label(self.master, text="ID Number", **label_style)
        #self.idLabel.grid(row=3, column=0, padx=10, pady=10)
        #self.idNumber = IntVar()
        #self.idNumberEntry = Entry(self.master, textvariable=self.idNumber, **entry_style)
        #self.idNumberEntry.grid(row=3, column=1, padx=10, pady=10)
        
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=3, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.master, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.master, columns=('id', 'name', ' position', 'email'), show='headings')
        self.tree.heading('id', text='id')
        self.tree.heading('name', text='name')
        self.tree.heading(' position', text=' position')
        self.tree.heading('email', text='email')
        self.tree.grid(row=5, column=0, columnspan=2, pady=20)

        # self.deleteButton = Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        # self.deleteButton.grid(row=6, column=0, columnspan=2, pady=10)

        self.deleteButton = Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=6, column=0, columnspan=2, pady=10)

        self.load_data()

    # def insert_to_db(self):
    #     name = self.name.get()
    #     position = self. position.get()
    #     email = self.email.get()

    #     if name and position and email :
    #         try:
    #             db = mysql.connector.connect(
    #                 host="localhost",
    #                 user='root',
    #                 password='',
    #                 database="PDataBaseV5"
    #             )
    #             cursor = db.cursor()
    #             sql = "INSERT INTO staff_info (name, position, email)) VALUES (%s, %s, %s)"
    #             cursor.execute(sql, (name, position, email))
    #             db.commit()
    #             messagebox.showinfo("Registration Success", "User registered successfully.")
    #             db.close()
    #             self.load_data()
    #         except mysql.connector.Error as err:
    #             messagebox.showerror("Database Error", f"Error: {err}")
    #     else:
    #         messagebox.showwarning("Input Error", "Please enter all fields.")


    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV5"
    )

    def insert_to_db(self):
        name = self.name.get()
        position = self.position.get()
        email = self.email.get()

        if name and position and email:
            try:
                with self.connect_db() as db:
                    cursor = db.cursor()
                    sql = "INSERT INTO staff_info (name, position, email) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (name, position, email))
                    db.commit()
                messagebox.showinfo("Registration Success", "User registered successfully.")
                self.load_data()
            except Error as err:
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
        cursor.execute("SELECT id,name,position,email FROM staff_info")
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
        record_id = values[0]
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