from tkinter import *
from pathlib import Path
from department import department
from level import Level
from instructor import Instructor
from subject import Subject
from load import Load
from Createtable import CreateTable
from location import LocationPageADD

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assetsmain")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Main Page')
        self.master.geometry('1000x700')  
        self.master.configure(bg='#FFFFFF')   

        #    
        self.sidebar_frame = Frame(self.master, bg='#5E95FF', width=250)
        self.sidebar_frame.pack(side=LEFT, fill=Y)

          
        self.content_frame = Frame(self.master, bg='#FFFFFF')
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        
        button_style = {'bg': '#5E95FF', 'fg': 'white', 'font': ('Montserrat', 12, 'bold'), 'width': 25, 'relief': FLAT}

        self.department = Button(self.sidebar_frame, text="Department", **button_style, command=self.show_department)
        self.department.pack(pady=10)

        self.level = Button(self.sidebar_frame, text="Level", **button_style, command=self.show_level)
        self.level.pack(pady=10)

        self.instructor = Button(self.sidebar_frame, text="Instructor", **button_style, command=self.show_instructor)
        self.instructor.pack(pady=10)

        self.subject = Button(self.sidebar_frame, text="Subject", **button_style, command=self.show_subject)
        self.subject.pack(pady=10)

        self.location = Button(self.sidebar_frame, text="Location", **button_style, command=self.show_location)
        self.location.pack(pady=10)        

        self.load = Button(self.sidebar_frame, text="Load", **button_style, command=self.show_load)
        self.load.pack(pady=10)

        self.create_table = Button(self.sidebar_frame, text="Create Table", **button_style, command=self.show_create_table)
        self.create_table.pack(pady=10)

        self.exit = Button(self.sidebar_frame, text="Exit", **button_style, command=self.close_window)
        self.exit.pack(pady=10)
        self.show_welcome()

    def show_department(self):
        self.update_content(department)

    def show_level(self):
        self.update_content(Level)

    def show_instructor(self):
        self.update_content(Instructor)

    def show_subject(self):
        self.update_content(Subject)

    def show_location(self):
        self.update_content(LocationPageADD)

    def show_load(self):
        self.update_content(Load)

    def show_create_table(self):
        self.update_content(CreateTable)

    def update_content(self, page_class):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        page_class(self.content_frame)

    def show_welcome(self):
        Label(self.content_frame, text="Welcome to the application.", bg='#FFFFFF', font=("Montserrat Medium", 17)).pack(pady=20)

    def close_window(self):
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = MainPage(root)
    root.mainloop()
