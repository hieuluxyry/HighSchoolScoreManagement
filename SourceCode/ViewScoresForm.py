from tkinter import ttk, Toplevel, Button
class ViewScoresForm(Toplevel):
    def __init__(self, parent, db_connection, callback=None):
        super().__init__(parent)
        self.title("Xem điểm")
        self.geometry("1280x720")
        self.config(bg="Brown")
        self.db_connection = db_connection
        self.callback = callback
        self.tree = ttk.Treeview(self, columns=("ID", "HocSinh", "LopHoc", "GVCN", "MonHoc", "DiemThiHK1", "DiemThiHK2", "DiemTBMon", "NamHoc"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("HocSinh", text="Học sinh")
        self.tree.heading("LopHoc", text="Lớp học")
        self.tree.heading("GVCN", text="GVCN")
        self.tree.heading("MonHoc", text="Môn học")
        self.tree.heading("DiemThiHK1", text="Điểm HK1")
        self.tree.heading("DiemThiHK2", text="Điểm HK2")
        self.tree.heading("DiemTBMon", text="Điểm TB môn")
        self.tree.heading("NamHoc", text="Năm học")
        self.tree.pack(pady=10, expand=True)

        button_refresh = Button(self, text="Làm mới", command=self.load_scores)
        button_refresh.config(bg="white",fg="black")
        button_refresh.pack(pady=10)

        button_close = Button(self, text="Đóng", command=self.close_form)
        button_close.config(bg="white",fg="black")
        button_close.pack(pady=10)

        self.load_scores()

    def load_scores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT Diem.DiemID, HocSinh.HoTen, LopHoc.TenLop, GiaoVien.TenGiaoVien, MonHoc.TenMonHoc, 
                   Diem.DiemThiHK1, Diem.DiemThiHK2, Diem.DiemTBMon, Diem.NamHoc
            FROM Diem
            JOIN HocSinh ON Diem.HocSinhID = HocSinh.ID
            JOIN LopHoc ON HocSinh.LopID = LopHoc.ID
            JOIN GiaoVien ON LopHoc.GVCNID = GiaoVien.ID
            JOIN MonHoc ON Diem.MonHocID = MonHoc.ID
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()
