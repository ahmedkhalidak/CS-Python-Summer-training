from tkinter import *
from Stuff import StuffPageADD
from location import LocationPageADD
from subject import SubjectADD
from load import LoadDel
# for functions (stuff / locations / subject)
class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('new main')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')
        
        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        
        self.doctorButton = Button(self.master, text="doctorButton",**button_style,command=self.open_stuff)
        self.doctorButton.grid(row=0, column=0, pady=10)
        
        self.locationButton = Button(self.master, text="locationButton",**button_style,command=self.open_location)
        self.locationButton.grid(row=0, column=1, pady=10)
        
        self.subjectButton = Button(self.master, text="subjectButton",**button_style,command=self.open_subject)
        self.subjectButton.grid(row=1, column=0, pady=10)

        self.loudButton = Button(self.master, text="load",**button_style,command=self.open_load )
        self.loudButton.grid(row=1, column=1, pady=10)

        
        self.creatTables = Button(self.master, text="creatTables",**button_style,command=self.open_subject)
        self.creatTables.grid(row=2, column=0, pady=10)

        
        self.ExitButton = Button(self.master, text="ExitButton",**button_style,command=self.close_window)
        self.ExitButton.grid(row=2, column=1, pady=10)

    def open_stuff(self):
        self.new_window(StuffPageADD)
        
    def open_location(self):
        self.new_window(LocationPageADD)
        
    def open_subject(self):
        self.new_window(SubjectADD)


    def open_load(self):
        self.new_window(LoadDel)

    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
        
    def close_window(self):
        self.master.destroy()
