from tkinter import *
from functionsfstuff import Functionsstuff
from functionsfsubject import Functionssubject
from functionslocation import Functionslocation
# for functions (stuff / locations / subject)
class Functions:
    def __init__(self, master):
        self.master = master
        self.master.title('work on data Form')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')
        
        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        
        self.stuffButton = Button(self.master, text="stuffButton",**button_style,command=self.open_stuff)
        self.stuffButton.grid(row=0, column=0, pady=10)
        
        self.locationButton = Button(self.master, text="locationButton",**button_style,command=self.open_location)
        self.locationButton.grid(row=1, column=0, pady=10)
        
        self.subjectButton = Button(self.master, text="subjectButton",**button_style,command=self.open_subject)
        self.subjectButton.grid(row=2, column=0, pady=10)
        
    def open_stuff(self):
        self.new_window(Functionsstuff)
        
    def open_location(self):
        self.new_window(Functionslocation)
        
    def open_subject(self):
        self.new_window(Functionssubject)

    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
        