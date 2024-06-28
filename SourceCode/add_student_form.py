from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

class AddStudentForm(Toplevel):
    def __init__(self, parent, db_connection, callback=None):
        super().__init__(parent)
        self.title("Thêm học sinh")
        self.geometry("1280x720")
        self.config(bg="Orange")
        self.db_connection = db_connection
        self.callback = callback
        Label(self, text="Họ và tên:", bg="white", fg="orange").grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        Label(self, text="Ngày sinh (YYYY-MM-DD):", bg="white", fg="orange").grid(row=1, column=0, padx=10, pady=10)
        self.entry_ngaysinh = Entry(self, width=30)
        self.entry_ngaysinh.grid(row=1, column=1, padx=10, pady=10)
        Label(self, text="Giới tính:", bg="white", fg="orange").grid(row=2, column=0, padx=10, pady=10)
        self.gioitinh_var = StringVar(self)
        self.gioitinh_var.set("Nam")
        self.option_menu = Menubutton(self, textvariable=self.gioitinh_var, indicatoron=True, borderwidth=1, relief="raised")
        self.option_menu.menu = Menu(self.option_menu, tearoff=0)
        self.option_menu["menu"] = self.option_menu.menu
        self.option_menu.menu.add_command(label="Nam", command=lambda: self.set_gioitinh("Nam", "blue"), background="lightblue")
        self.option_menu.menu.add_command(label="Nữ", command=lambda: self.set_gioitinh("Nữ", "pink"), background="lightpink")
        self.option_menu.grid(row=2, column=1, padx=10, pady=10)
        Label(self, text="Địa chỉ:", bg="white", fg="orange").grid(row=3, column=0, padx=10, pady=10)
        self.entry_diachi = Entry(self, width=30)
        self.entry_diachi.grid(row=3, column=1, padx=10, pady=10)
        Label(self, text="Lớp:", bg="white", fg="orange").grid(row=4, column=0, padx=10, pady=10)
        self.entry_lop = Entry(self, width=30)
        self.entry_lop.grid(row=4, column=1, padx=10, pady=10)
        Button(self, text="Thêm Học Sinh", bg="white", fg="orange", command=self.save_student).grid(row=5, column=0, columnspan=2, padx=10, pady=20)
        Button(self, text="Sửa Học Sinh", bg="white", fg="orange", command=self.edit_student).grid(row=6, column=0, padx=10, pady=10)
        Button(self, text="Xóa Học Sinh ", bg="white", fg="orange", command=self.delete_student).grid(row=6, column=1, padx=10, pady=10)
        Button(self, text="Thoát", bg="white", fg="orange", command=self.close_form).grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.tree = ttk.Treeview(self, columns=("ID", "HoTen", "NgaySinh", "GioiTinh", "DiaChi", "Lop"), show="headings", height=15)
        self.tree.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky=(N, S, W, E))
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=3, rowspan=8, sticky=(N, S, E))
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.heading("ID", text="ID")
        self.tree.heading("HoTen", text="Họ và tên")
        self.tree.heading("NgaySinh", text="Ngày sinh")
        self.tree.heading("GioiTinh", text="Giới tính")
        self.tree.heading("DiaChi", text="Địa chỉ")
        self.tree.heading("Lop", text="Lớp")
        self.load_students()
    def set_gioitinh(self, value, color):
        self.gioitinh_var.set(value)
        self.option_menu.config(bg=color)
    def load_students(self):
        try:
            self.tree.delete(*self.tree.get_children())
            cursor = self.db_connection.cursor()
            query = """
            SELECT HocSinh.ID, HocSinh.HoTen, HocSinh.NgaySinh, HocSinh.GioiTinh, HocSinh.DiaChi, Lop.TenLop 
            FROM HocSinh 
            JOIN Lop ON HocSinh.LopID = Lop.ID
            """
            cursor.execute(query)
            students = cursor.fetchall()
            for student in students:
                self.tree.insert("", "end", values=student)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def save_student(self):
        hoten = self.entry_name.get()
        ngaysinh = self.entry_ngaysinh.get()
        gioitinh = self.gioitinh_var.get()
        diachi = self.entry_diachi.get()
        lop = self.entry_lop.get()

        if hoten and ngaysinh and gioitinh and diachi and lop:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT ID FROM Lop WHERE TenLop = %s", (lop,))
                lop_id = cursor.fetchone()

                if lop_id:
                    sql = "INSERT INTO HocSinh (HoTen, NgaySinh, GioiTinh, DiaChi, LopID) VALUES (%s, %s, %s, %s, %s)"
                    values = (hoten, ngaysinh, gioitinh, diachi, lop_id[0])
                    cursor.execute(sql, values)
                    self.db_connection.commit()
                    messagebox.showinfo("Thêm học sinh", "Thêm học sinh thành công!")
                    self.load_students()
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy lớp học.")
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin học sinh.")

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn học sinh để sửa.")
            return
        item = self.tree.item(selected_item[0])
        student_id = item["values"][0]
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT HoTen, NgaySinh, GioiTinh, DiaChi, LopID FROM HocSinh WHERE ID = %s", (student_id,))
            student_details = cursor.fetchone()
            if student_details:
                edit_dialog = Toplevel(self)
                edit_dialog.title("Sửa thông tin học sinh")
                edit_dialog.geometry("400x300")
                Label(edit_dialog, text="Họ và tên:").grid(row=0, column=0, padx=10, pady=5)
                entry_name = Entry(edit_dialog, width=30)
                entry_name.insert(0, student_details[0])
                entry_name.grid(row=0, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Ngày sinh (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
                entry_ngaysinh = Entry(edit_dialog, width=30)
                entry_ngaysinh.insert(0, student_details[1])
                entry_ngaysinh.grid(row=1, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Giới tính:").grid(row=2, column=0, padx=10, pady=5)
                gioitinh_var = StringVar(edit_dialog)
                gioitinh_var.set(student_details[2])

                edit_option_menu = Menubutton(edit_dialog, textvariable=gioitinh_var, indicatoron=True, borderwidth=1, relief="raised")
                edit_option_menu.menu = Menu(edit_option_menu, tearoff=0)
                edit_option_menu["menu"] = edit_option_menu.menu

                edit_option_menu.menu.add_command(label="Nam", command=lambda: self.set_gioitinh_edit(gioitinh_var, "Nam", edit_option_menu, "blue"), background="lightblue")
                edit_option_menu.menu.add_command(label="Nữ", command=lambda: self.set_gioitinh_edit(gioitinh_var, "Nữ", edit_option_menu, "pink"), background="lightpink")

                edit_option_menu.grid(row=2, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Địa chỉ:").grid(row=3, column=0, padx=10, pady=5)
                entry_diachi = Entry(edit_dialog, width=30)
                entry_diachi.insert(0, student_details[3])
                entry_diachi.grid(row=3, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Lớp:").grid(row=4, column=0, padx=10, pady=5)
                entry_lop = Entry(edit_dialog, width=30)
                cursor.execute("SELECT TenLop FROM Lop WHERE ID = %s", (student_details[4],))
                lop_name = cursor.fetchone()[0]
                entry_lop.insert(0, lop_name)
                entry_lop.grid(row=4, column=1, padx=10, pady=5)

                def save_changes():
                    new_name = entry_name.get()
                    new_ngaysinh = entry_ngaysinh.get()
                    new_gioitinh = gioitinh_var.get()
                    new_diachi = entry_diachi.get()
                    new_lop = entry_lop.get()

                    if new_name and new_ngaysinh and new_gioitinh and new_diachi and new_lop:
                        try:
                            cursor.execute("SELECT ID FROM Lop WHERE TenLop = %s", (new_lop,))
                            lop_id = cursor.fetchone()

                            if lop_id:
                                update_sql = "UPDATE HocSinh SET HoTen = %s, NgaySinh = %s, GioiTinh = %s, DiaChi = %s, LopID = %s WHERE ID = %s"
                                update_values = (new_name, new_ngaysinh, new_gioitinh, new_diachi, lop_id[0], student_id)
                                cursor.execute(update_sql, update_values)
                                self.db_connection.commit()
                                messagebox.showinfo("Thông báo", "Cập nhật thông tin thành công!")
                                self.load_students()
                                edit_dialog.destroy()
                            else:
                                messagebox.showerror("Lỗi", "Không tìm thấy lớp học.")
                        except mysql.connector.Error as err:
                            messagebox.showerror("Lỗi", f"Lỗi: {err}")
                    else:
                        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin học sinh.")
                Button(edit_dialog, text="Lưu", command=save_changes).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin học sinh.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi: {err}")
    def set_gioitinh_edit(self, var, value, menu_button, color):
        var.set(value)
        menu_button.config(bg=color)

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn học sinh để xóa.")
            return
        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa học sinh này?"):
            item = self.tree.item(selected_item[0])
            student_id = item["values"][0]

            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM HocSinh WHERE ID = %s", (student_id,))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Xóa học sinh thành công!")
                self.load_students()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()
