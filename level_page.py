from tkinter import *

class LevelPage:
    def __init__(self, master):
        self.master = master
        self.master.title('LEVEL Form')
        self.master.geometry('400x250')
        self.master.configure(bg='lightblue')

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.usernameLabel = Label(self.master, text="Name", **label_style)
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.username = StringVar()
        self.usernameEntry = Entry(self.master, textvariable=self.username, **entry_style)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.departmentLabel = Label(self.master, text="Department", **label_style)
        self.departmentLabel.grid(row=1, column=0, padx=10, pady=10)
        self.department = StringVar()
        self.departmentEntry = Entry(self.master, textvariable=self.department, **entry_style)
        self.departmentEntry.grid(row=1, column=1, padx=10, pady=10)

        self.studentNumberLabel = Label(self.master, text="Student Number", **label_style)
        self.studentNumberLabel.grid(row=2, column=0, padx=10, pady=1)
        self.studentNumber = IntVar()
        self.studentNumberEntry = Entry(self.master, textvariable=self.studentNumber, **entry_style)
        self.studentNumberEntry.grid(row=2, column=1, padx=10, pady=10)

        self.sectionsLabel = Label(self.master, text="Sections", **label_style)
        self.sectionsLabel.grid(row=3, column=0, padx=10, pady=10)
        self.sections = IntVar()
        self.sectionsEntry = Entry(self.master, textvariable=self.sections, **entry_style)
        self.sectionsEntry.grid(row=3, column=1, padx=10, pady=10)

        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'))
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)
