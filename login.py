from tkinter import *
from tkinter import messagebox
from pathlib import Path
from main import MainPage
import mysql.connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Login(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.title("Login - YourApp")
        self.geometry("1012x506")
        self.configure(bg="#5E95FF")

        self.canvas = Canvas(
            self,
            bg="#5E95FF",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            469.0, 0.0, 1012.0, 506.0, fill="#FFFFFF", outline=""
        )

        # تحميل الصور
        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(736.0, 331.0, image=entry_image_1)
        self.entry_image_1 = entry_image_1  # حفظ الصورة في الذاكرة

        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16),
            foreground="#777777",
        )
        self.username.place(x=573.0, y=229.0, width=326.0, height=22.0)

        entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(736.0, 229.0, image=entry_image_2)
        self.entry_image_2 = entry_image_2  # حفظ الصورة في الذاكرة

        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16),
            foreground="#777777",
            show="•",
        )
        self.password.place(x=573.0, y=330.0, width=326.0, height=22.0)

        self.canvas.create_text(
            573.0,
            306.0,
            anchor="nw",
            text="Password",
            fill="#5E95FF",
            font=("Montserrat Bold", 14),
        )

        self.canvas.create_text(
            573.0,
            204.0,
            anchor="nw",
            text="Username",
            fill="#5E95FF",
            font=("Montserrat Bold", 14),
        )

        self.canvas.create_text(
            553.0,
            66.0,
            anchor="nw",
            text="Enter your login details",
            fill="#5E95FF",
            font=("Montserrat Bold", 26),
        )

        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.logintodb,
            relief="flat",
        )
        button_1.place(x=641.0, y=412.0, width=190.0, height=48.0)

        self.username.bind("<Return>", lambda x: self.logintodb())
        self.password.bind("<Return>", lambda x: self.logintodb())

        self.resizable(False, False)
        self.mainloop()

    def logintodb(self):
        UName = self.username.get()
        Pass = self.password.get()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBasev8"
            )
            cursor = db.cursor()
            sql = "SELECT * FROM login WHERE UName=%s AND Pass=%s"
            cursor.execute(sql, (UName, Pass))
            myresult = cursor.fetchall()
            if myresult:
                self.open_main_page()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def open_main_page(self):
        self.destroy()
        main_page = Tk()
        MainPage(main_page)

if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
