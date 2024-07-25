import tkinter as tk
from tkinter import *

class Subjectdel:
    def __init__(self, root):
        self.root = root
        self.root.title("Subject")
        self.root.geometry('400x200')
        
        self.courseName = Label(root, text="Course Name:")
        self.courseName.grid(row=0, column=0)
        self.courseNameEntry = Entry(root, width=20)
        self.courseNameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.courseCode = Label(root, text="Course Code:")
        self.courseCode.grid(row=1, column=0)
        self.courseCodeEntry = Entry(root, width=20)
        self.courseCodeEntry.grid(row=1, column=1, padx=10, pady=10)

        self.submit = Button(root, text="Submit", command=self.button_click)
        self.submit.grid(row=4, column=1, columnspan=2, padx=10, pady=10, ipadx=10)
