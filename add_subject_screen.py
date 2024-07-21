import tkinter as tk
from tkinter import *

class SubjectADD:
    def __init__(self, root):
        self.root = root
        self.root.title("Subject")
        self.root.geometry('400x200')
        
        # Labels and Entry widgets
        self.courseName = Label(root, text="Course Name:")
        self.courseName.grid(row=0, column=0)
        self.courseNameEntry = Entry(root, width=20)
        self.courseNameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.courseCode = Label(root, text="Course Code:")
        self.courseCode.grid(row=1, column=0)
        self.courseCodeEntry = Entry(root, width=20)
        self.courseCodeEntry.grid(row=1, column=1, padx=10, pady=10)

        self.level = Label(root, text="Level:")
        self.level.grid(row=2, column=0)
        self.levelEntry = Entry(root, width=20)
        self.levelEntry.grid(row=2, column=1, padx=10, pady=10)

        self.department = Label(root, text="Department:")
        self.department.grid(row=3, column=0)
        self.departmentEntry = Entry(root, width=20)
        self.departmentEntry.grid(row=3, column=1, padx=10, pady=10)

        self.submit = Button(root, text="Submit", command=self.button_click)
        self.submit.grid(row=4, column=1, columnspan=2, padx=10, pady=10, ipadx=10)
