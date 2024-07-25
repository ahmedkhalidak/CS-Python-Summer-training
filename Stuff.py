from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class StuffPageADD:
    def __init__(self, master):
        self.master = master
        self.master.title('Staff Form for Add')
        self.master.geometry('600x500')
        self.master.configure(bg='lightblue')

        self.setup_widgets()
        self.load_data()

    def setup_widgets(self):
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        # Name Entry
        Label(self.master, text="Name", **label_style).grid(row=0, column=0, padx=10, pady=10)
        self.name = StringVar()
        Entry(self.master, textvariable=self.name, **entry_style).grid(row=0, column=1, padx=10, pady=10)

        # Position Radiobuttons
        self.position = StringVar()
        self.position.set("DR")
        Radiobutton(self.master, text='Dr', variable=self.position, value="DR", bg='lightblue', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10)
        Radiobutton(self.master, text='TA', variable=self.position, value="TA", bg='lightblue', font=('Arial', 12)).grid(row=1, column=1, padx=10, pady=10)

        # Email Entry
        Label(self.master, text="Email", **label_style).grid(row=2, column=0, padx=10, pady=10)
        self.email = StringVar()
        Entry(self.master, textvariable=self.email, **entry_style).grid(row=2, column=1, padx=10, pady=10)

        # Submit Button
        Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db).grid(row=3, column=0, columnspan=2, pady=20)

        # Load Data Button
        Button(self.master, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data).grid(row=4, column=0, columnspan=2, pady=10)

        # Treeview for Displaying Data
        self.tree = ttk.Treeview(self.master, columns=('id', 'name', 'position', 'email'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, column=0, columnspan=2, pady=20)

        # Delete Button
        Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record).grid(row=6, column=0, columnspan=2, pady=10)

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
        with self.connect_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT id, name, position, email FROM staff_info")
            rows = cursor.fetchall()
        return rows

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record to delete")
            return

        record_id = self.tree.item(selected_item[0], 'values')[0]
        try:
            with self.connect_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM staff_info WHERE id = %s", (record_id,))
                db.commit()
            self.tree.delete(selected_item[0])
            messagebox.showinfo("Success", "Record deleted successfully.")
        except Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
