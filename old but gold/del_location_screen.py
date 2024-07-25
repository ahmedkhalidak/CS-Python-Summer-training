from tkinter import *

class LocationPagedel:
    def __init__(self, master):
        self.master = master
        self.master.title('Location Form')
        self.master.geometry('400x350')
        self.master.configure(bg='lightblue')
        
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}
        
    
        
        # ID
        self.idLabel = Label(self.master, text="ID", **label_style)
        self.idLabel.grid(row=1, column=0, padx=10, pady=10)
        self.id = StringVar()
        self.idEntry = Entry(self.master, textvariable=self.id, **entry_style)
        self.idEntry.grid(row=1, column=1, padx=10, pady=10)
        
  
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'))
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)
   


