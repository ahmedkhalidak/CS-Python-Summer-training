from tkinter import *

class StuffPageupd:
    def __init__(self, master):
        self.master = master
        self.master.title('Stuff Form For Add')
        self.master.geometry('400x250')
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

        self.idLabel = Label(self.master, text="ID Number", **label_style)
        self.idLabel.grid(row=3, column=0, padx=10, pady=10)
        self.idNumber = IntVar()
        self.idNumberEntry = Entry(self.master, textvariable=self.idNumber, **entry_style)
        self.idNumberEntry.grid(row=3, column=1, padx=10, pady=10)
        
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'))
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)

