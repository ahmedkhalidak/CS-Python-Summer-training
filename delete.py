import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class Delete:
    def __init__(self, root):
        self.root = root
        self.root.title("Delete Subject")
        self.root.geometry("800x400")  # تعيين حجم نافذة التطبيق

        # إعداد الاتصال بقاعدة البيانات
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            database='pdatabasev8'
        )
        self.cursor = self.conn.cursor()

        # جلب بيانات الأقسام وإعداد قاموس لربط الأسماء بالمعرفات
        self.department_data = self.fetch_department_data()
        self.department_dict = {name: id for id, name in self.department_data}

        # إطار لتجميع عناصر الواجهة
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(expand=True, fill='both')

        # إعداد الـ Combobox الخاصة بالأقسام
        tk.Label(frame, text="Department:", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.department_combobox = ttk.Combobox(frame, values=[name for id, name in self.department_data])
        self.department_combobox.grid(row=0, column=1, padx=10, pady=10)
        
        # إعداد الـ Combobox الخاصة بالمستويات
        tk.Label(frame, text="Level:", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.level_combobox = ttk.Combobox(frame)
        self.level_combobox.grid(row=1, column=1, padx=10, pady=10)
        
        # إعداد الـ Combobox الخاصة بالأيام
        tk.Label(frame, text="Day:", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.day_combobox = ttk.Combobox(frame)
        self.day_combobox.grid(row=2, column=1, padx=10, pady=10)

        # إعداد الجدول لعرض البيانات
        self.columns = ('ID', 'subject_ID', 'Day', 'sections', 'time_start')
        self.schedule_table = ttk.Treeview(frame, columns=self.columns, show='headings')
        self.schedule_table.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        for col in self.columns:
            self.schedule_table.heading(col, text=col)
            self.schedule_table.column(col, width=120, anchor='center')

        # إعداد زر الحذف
        self.delete_button = tk.Button(frame, text="Delete Selected", command=self.delete_selected_row, bg='#ff4d4d', fg='white', font=('Arial', 12, 'bold'))
        self.delete_button.grid(row=4, column=0, columnspan=2, pady=10)

        # ربط الأحداث مع comboboxs
        self.department_combobox.bind("<<ComboboxSelected>>", self.update_level_combobox)
        self.level_combobox.bind("<<ComboboxSelected>>", self.update_day_combobox)
        self.day_combobox.bind("<<ComboboxSelected>>", self.update_schedule_table)

        # تكبير الصفوف والأعمدة
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def fetch_department_data(self):
        """ جلب بيانات الأقسام من قاعدة البيانات """
        self.cursor.execute("SELECT ID, Name FROM department")
        return self.cursor.fetchall()

    def fetch_level_data(self, department_id):
        """ جلب بيانات المستويات بناءً على معرف القسم """
        self.cursor.execute("SELECT levelNO FROM level WHERE Dept_ID = %s", (department_id,))
        return self.cursor.fetchall()

    def fetch_day_data(self, department_id, level_no):
        """ جلب الأيام بناءً على القسم والمستوى مع تجنب التكرار """
        self.cursor.execute("SELECT ID FROM level WHERE Dept_ID = %s AND levelNO = %s", (department_id, level_no))
        level_id = self.cursor.fetchone()
        if level_id:
            self.cursor.execute("SELECT DISTINCT Day FROM schedule WHERE level_ID = %s", (level_id[0],))
            return self.cursor.fetchall()
        return []

    def fetch_schedule_data(self, department_id, level_no, day):
        """ جلب بيانات الجدول بناءً على القسم والمستوى واليوم المختارين """
        self.cursor.execute("""
            SELECT ID, subject_ID, Day, sections, time_start 
            FROM schedule
            WHERE level_ID = (
                SELECT ID FROM level WHERE Dept_ID = %s AND levelNO = %s
            ) AND Day = %s
        """, (department_id, level_no, day))
        return self.cursor.fetchall()

    def update_level_combobox(self, event):
        """ تحديث قائمة المستويات بناءً على القسم المختار """
        selected_department_name = self.department_combobox.get()
        department_id = self.department_dict[selected_department_name]
        levels = self.fetch_level_data(department_id)
        self.level_combobox['values'] = [level[0] for level in levels]
        self.level_combobox.set('')
        self.day_combobox.set('')
        self.schedule_table.delete(*self.schedule_table.get_children())

    def update_day_combobox(self, event):
        """ تحديث قائمة الأيام بناءً على القسم والمستوى المختارين مع إزالة التكرارات """
        selected_level = self.level_combobox.get()
        selected_department_name = self.department_combobox.get()
        department_id = self.department_dict[selected_department_name]
        days = self.fetch_day_data(department_id, selected_level)
        self.day_combobox['values'] = sorted(set(day[0] for day in days))
        self.day_combobox.set('')
        self.schedule_table.delete(*self.schedule_table.get_children())

    def update_schedule_table(self, event):
        """ تحديث جدول البيانات بناءً على جميع القيم المختارة """
        selected_level = self.level_combobox.get()
        selected_department_name = self.department_combobox.get()
        selected_day = self.day_combobox.get()
        if selected_day:
            department_id = self.department_dict[selected_department_name]
            schedule_data = self.fetch_schedule_data(department_id, selected_level, selected_day)
            self.schedule_table.delete(*self.schedule_table.get_children())
            for row in schedule_data:
                self.schedule_table.insert('', 'end', values=row)

    def delete_selected_row(self):
        """ دالة حذف البيانات """
        selected_item = self.schedule_table.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a row to delete.")
            return
        
        selected_row = self.schedule_table.item(selected_item)['values']
        schedule_id = selected_row[0]  # ID of the selected row

        # حذف البيانات من قاعدة البيانات
        self.cursor.execute("DELETE FROM schedule WHERE ID = %s", (schedule_id,))
        self.conn.commit()
        
        # تحديث الجدول بعد الحذف
        self.update_schedule_table(None)
        messagebox.showinfo("Success", "Selected row deleted successfully.")

    def close(self):
        """ إغلاق الاتصال بقاعدة البيانات """
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Delete(root)
    root.mainloop()
