from tkinter import *
from doctor_page import DoctorPage
from level_page import LevelPage
from location_page import LocationPage

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Main Page')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')

        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}

        self.doctorButton = Button(self.master, text="Doctor", command=self.open_doctor_page,**button_style)
        self.doctorButton.pack(pady=10)

        self.levelButton = Button(self.master, text="Level", command=self.open_level_page,**button_style)
        self.levelButton.pack(pady=10)

        self.locationButton = Button(self.master, text="Location", command=self.open_location_page,**button_style)
        self.locationButton.pack(pady=10)

    def open_doctor_page(self):
        self.new_window(DoctorPage)

    def open_level_page(self):
        self.new_window(LevelPage)

    def open_location_page(self):
        self.new_window(LocationPage)

    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
