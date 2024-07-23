from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
class LocationPageADD:
    def __init__(self, master):
        self.master = master
        self.master.title('Location Form')
        self.master.geometry('400x350')
        self.master.configure(bg='lightblue')
        
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}
        
        # Location Type
        self.type = StringVar()
        self.typeLabel = Label(self.master, text="Type", **label_style)
        self.typeLabel.grid(row=0, column=0, padx=10, pady=10)
        self.typeListbox = Listbox(self.master, selectmode=SINGLE, listvariable=self.type ,height=1, **entry_style)
        for item in ["Hall", "Room", "Lab"]:
            self.typeListbox.insert(END, item)
        self.typeListbox.grid(row=0, column=1, padx=10, pady=10)
        

        # number
        self.HNumLable = Label(self.master, text="Number", **label_style)
        self.HNumLable.grid(row=1, column=0, padx=10, pady=10)
        self.HNum = StringVar()
        self.HNumEntry = Entry(self.master, textvariable=self.HNum, **entry_style)
        self.HNumEntry.grid(row=1, column=1, padx=10, pady=10)
        # Capacity
        self.capacityLabel = Label(self.master, text="Capacity", **label_style)
        self.capacityLabel.grid(row=2, column=0, padx=10, pady=10)
        self.capacity = StringVar()
        self.capacityEntry = Entry(self.master, textvariable=self.capacity, **entry_style)
        self.capacityEntry.grid(row=2, column=1, padx=10, pady=10)
        
        # Building Number
        self.building = StringVar()
        self.buildingLabel = Label(self.master, text="Building Number", **label_style)
        self.buildingLabel.grid(row=3, column=0, padx=10, pady=10)
        self.buildingListbox = Listbox(self.master, selectmode=SINGLE,listvariable=self.building, height=2, **entry_style)
        for item in ["A", "B"]:
            print(item)
            self.buildingListbox.insert(END, item)
        self.buildingListbox.grid(row=3, column=1, padx=10, pady=10)
        
        # Submit Button
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.master, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.master, columns=('ID', 'type', 'number', 'capacity', 'bulding'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('type', text='type')
        self.tree.heading('number', text='number')
        self.tree.heading('capacity', text='capacity')
        self.tree.heading('bulding', text='bulding')

        self.tree.grid(row=6, column=1, columnspan=2, pady=20)

        self.deleteButton = Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.load_data()

    def insert_to_db(self):
        Type = self.type.get()
        Capacity = self.capacity.get()
        Building = self.building.get()
        number= self.HNum.get()
        # SName = self.username.get()
        # role = self.role.get()
        # SEmail = self.Email.get()
        # SID = self.idNumber.get()

        if Type and Capacity and Building:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBase"
                )
                cursor = db.cursor()
                sql = "INSERT INTO location (type, capacity, building, number) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (Type, Capacity, Building, number) )
                db.commit()
                messagebox.showinfo("Registration Success", "Location registered successfully.")
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
            database="PDataBase"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM location")
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
        record_id = values[0]
        print(record_id)
        print(selected_item)
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBase"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM location WHERE ID = %s", (record_id ,))
        db.commit()
        db.close()
        self.load_data()
