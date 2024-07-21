from tkinter import *
from workondata import  Functions

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Main Page')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')

        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}

        self.databasebutton= Button(self.master, text="databasebutton", command=self.open_database_page,**button_style)
        self.databasebutton.pack(pady=10)

        self.workinschudleButton = Button(self.master, text="workinschudleButton", command=self.open_level_page,**button_style)
        self.workinschudleButton.pack(pady=10)


    def open_database_page(self):
        self.new_window(Functions)

    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
