from tkinter import *
from add_location_screen import LocationPageADD
from del_location_screen import LocationPagedel
from upd_location_screen import LocationPageupd
class Functionslocation:
    def __init__(self, master):
        self.master = master
        self.master.title('Functions Form')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')
        
        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        
        self.ADDButton = Button(self.master, text="ADDButton",**button_style,command=self.open_ADD_location)
        self.ADDButton.grid(row=0, column=0, pady=10)
        
        self.deleteButton = Button(self.master, text="deleteButton",**button_style,command=self.open_del_location)
        self.deleteButton.grid(row=1, column=0, pady=10)
        
        self.updateButton = Button(self.master, text="updateButton",**button_style,command=self.open_upd_location)
        self.updateButton.grid(row=2, column=0, pady=10)
        
    
    def open_ADD_location(self):
        self.new_window(LocationPageADD)
    def open_del_location(self):
        self.new_window(LocationPagedel)
    def open_upd_location(self):
        self.new_window(LocationPageupd)
    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
        