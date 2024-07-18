from tkinter import *

class LocationPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Location Form')
        self.master.geometry('400x300')
        self.master.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.usernameLabel = Label(self.master, text="Name", **label_style)
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.username = StringVar()
        self.usernameEntry = Entry(self.master, textvariable=self.username, **entry_style)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.sizeLabel = Label(self.master, text="Size", **label_style)
        self.sizeLabel.grid(row=1, column=0, padx=10, pady=10)
        self.size = IntVar()
        self.sizeEntry = Entry(self.master, textvariable=self.size, **entry_style)
        self.sizeEntry.grid(row=1, column=1, padx=10, pady=10)

        self.is_lab = IntVar()
        self.isLabButton = Checkbutton(self.master, text="IS Lab", variable=self.is_lab, bg='lightblue', font=('Arial', 12, 'bold'))
        self.isLabButton.grid(row=2, column=1, padx=10, pady=10)

        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'))
        self.submitButton.grid(row=3, column=0, columnspan=2, pady=20)
