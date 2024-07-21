from tkinter import *
from add_subject_screen import SubjectADD
from del_subject_screen import Subjectdel
from upd_subject_screen import Subjectupd
# for functions (Subject / locations / subject)
class Functionssubject:
    def __init__(self, master):
        self.master = master
        self.master.title('Functions Form')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')
        
        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        self.ADDButton = Button(self.master, text="ADDButton",**button_style,command=self.open_ADD_Subject)
        self.ADDButton.grid(row=0, column=0, pady=10)
        
        self.deleteButton = Button(self.master, text="deleteButton",**button_style,command=self.open_del_Subject)
        self.deleteButton.grid(row=1, column=0, pady=10)
        
        self.updateButton = Button(self.master, text="updateButton",**button_style,command=self.open_upd_Subject)
        self.updateButton.grid(row=2, column=0, pady=10)
        
    
    def open_ADD_Subject(self):
        self.new_window(SubjectADD)
    def open_del_Subject(self):
        self.new_window(Subjectdel)
    def open_upd_Subject(self):
        self.new_window(Subjectupd)
    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
        