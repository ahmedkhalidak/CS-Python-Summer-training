from tkinter import *

class LocationPageADD:
    def __init__(self, master):
        self.master = master
        self.master.title('Location Form')
        self.master.geometry('400x350')
        self.master.configure(bg='lightblue')
        
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}
        
        # Location Type
        self.typeLabel = Label(self.master, text="Type", **label_style)
        self.typeLabel.grid(row=0, column=0, padx=10, pady=10)
        self.typeListbox = Listbox(self.master, selectmode=SINGLE, height=3, **entry_style)
        for item in ["Hall", "Room", "Lab"]:
            self.typeListbox.insert(END, item)
        self.typeListbox.grid(row=0, column=1, padx=10, pady=10)
        
        # Capacity
        self.capacityLabel = Label(self.master, text="Capacity", **label_style)
        self.capacityLabel.grid(row=1, column=0, padx=10, pady=10)
        self.capacity = StringVar()
        self.capacityEntry = Entry(self.master, textvariable=self.capacity, **entry_style)
        self.capacityEntry.grid(row=1, column=1, padx=10, pady=10)
        
        # Building Number
        self.buildingLabel = Label(self.master, text="Building Number", **label_style)
        self.buildingLabel.grid(row=2, column=0, padx=10, pady=10)
        self.buildingListbox = Listbox(self.master, selectmode=SINGLE, height=2, **entry_style)
        for item in ["A", "B"]:
            self.buildingListbox.insert(END, item)
        self.buildingListbox.grid(row=2, column=1, padx=10, pady=10)
        
        # ID
        self.idLabel = Label(self.master, text="ID", **label_style)
        self.idLabel.grid(row=3, column=0, padx=10, pady=10)
        self.id = StringVar()
        self.idEntry = Entry(self.master, textvariable=self.id, **entry_style)
        self.idEntry.grid(row=3, column=1, padx=10, pady=10)
        
        # Submit Button
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'))
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)
