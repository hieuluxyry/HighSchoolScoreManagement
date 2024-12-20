-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS QuanLyDiemTHPT;
USE QuanLyDiemTHPT;

-- Table: Lop (Class)
CREATE TABLE IF NOT EXISTS Lop (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    TenLop VARCHAR(50) NOT NULL,
    GVCN VARCHAR(100) NOT NULL
);

-- Table: HocSinh (Student)
CREATE TABLE IF NOT EXISTS HocSinh (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    HoTen VARCHAR(100) NOT NULL,
    NgaySinh DATE NOT NULL,
    GioiTinh ENUM('Nam', 'Nu') NOT NULL,
    DiaChi VARCHAR(200),
    LopID INT NOT NULL,
    FOREIGN KEY (LopID) REFERENCES Lop(ID)
);

-- Table: MonHoc (Subject)
CREATE TABLE IF NOT EXISTS MonHoc (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    TenMonHoc VARCHAR(100) NOT NULL
);

-- Table: Diem (Grades)
CREATE TABLE IF NOT EXISTS Diem (
    DiemID INT PRIMARY KEY AUTO_INCREMENT,
    HocSinhID INT NOT NULL,
    MonHocID INT NOT NULL,
    DiemThiHK1 FLOAT CHECK (DiemThiHK1 >= 0 AND DiemThiHK1 <= 10),
    DiemThiHK2 FLOAT CHECK (DiemThiHK2 >= 0 AND DiemThiHK2 <= 10),
    DiemTBMon FLOAT CHECK (DiemTBMon >= 0 AND DiemTBMon <= 10),
    NamHoc VARCHAR(9) NOT NULL,
    FOREIGN KEY (HocSinhID) REFERENCES HocSinh(ID),
    FOREIGN KEY (MonHocID) REFERENCES MonHoc(ID)
);
