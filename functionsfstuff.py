from tkinter import *
from add_stuff_screen import StuffPageADD
from del_stuff_screen import StuffPagedel
from upd_stuff_screen import StuffPageupd
# for functions (stuff / locations / subject)
class Functionsstuff:
    def __init__(self, master):
        self.master = master
        self.master.title('Functions Form')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')
        
        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        
        self.ADDButton = Button(self.master, text="ADDButton",**button_style,command=self.open_ADD_stuff)
        self.ADDButton.grid(row=0, column=0, pady=10)
        
        self.deleteButton = Button(self.master, text="deleteButton",**button_style,command=self.open_del_stuff)
        self.deleteButton.grid(row=1, column=0, pady=10)
        
        self.updateButton = Button(self.master, text="updateButton",**button_style,command=self.open_upd_stuff)
        self.updateButton.grid(row=2, column=0, pady=10)
        
    
    def open_ADD_stuff(self):
        self.new_window(StuffPageADD)
    def open_del_stuff(self):
        self.new_window(StuffPagedel)
    def open_upd_stuff(self):
        self.new_window(StuffPageupd)
    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
        