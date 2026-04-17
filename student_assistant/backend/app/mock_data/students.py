STUDENTS_DB = {
    "SV001": {
        "id": "SV001",
        "name": "Nguyễn Văn An",
        "class": "CNTT-K20A",
        "major": "Công nghệ Thông tin",
        "email": "an.nv@university.edu.vn",
    },
    "SV002": {
        "id": "SV002",
        "name": "Trần Thị Bích",
        "class": "CNTT-K20B",
        "major": "Công nghệ Thông tin",
        "email": "bich.tt@university.edu.vn",
    },
    "SV003": {
        "id": "SV003",
        "name": "Lê Hoàng Cường",
        "class": "KTPM-K21A",
        "major": "Kỹ thuật Phần mềm",
        "email": "cuong.lh@university.edu.vn",
    },
}

SCHEDULES_DB = {
    "SV001": [
        {"day": "Thứ 2", "time": "07:30 – 09:30", "subject": "Trí tuệ Nhân tạo", "room": "A301", "teacher": "TS. Phạm Văn Đức"},
        {"day": "Thứ 2", "time": "09:45 – 11:45", "subject": "Cơ sở Dữ liệu", "room": "B205", "teacher": "ThS. Nguyễn Thị Em"},
        {"day": "Thứ 3", "time": "13:00 – 15:00", "subject": "Lập trình Web", "room": "C102", "teacher": "TS. Trần Minh Phong"},
        {"day": "Thứ 4", "time": "07:30 – 09:30", "subject": "Trí tuệ Nhân tạo", "room": "A301", "teacher": "TS. Phạm Văn Đức"},
        {"day": "Thứ 5", "time": "09:45 – 11:45", "subject": "Mạng Máy tính", "room": "D404", "teacher": "PGS.TS. Lê Văn Giang"},
        {"day": "Thứ 6", "time": "07:30 – 09:30", "subject": "Lập trình Web", "room": "C102", "teacher": "TS. Trần Minh Phong"},
    ],
    "SV002": [
        {"day": "Thứ 2", "time": "13:00 – 15:00", "subject": "Xử lý Ảnh", "room": "A205", "teacher": "TS. Võ Thị Hạnh"},
        {"day": "Thứ 3", "time": "07:30 – 09:30", "subject": "Học Máy", "room": "B301", "teacher": "PGS.TS. Nguyễn Thành Tùng"},
        {"day": "Thứ 4", "time": "09:45 – 11:45", "subject": "Toán rời rạc", "room": "C103", "teacher": "ThS. Phạm Thị Kim"},
        {"day": "Thứ 5", "time": "13:00 – 15:00", "subject": "Học Máy", "room": "B301", "teacher": "PGS.TS. Nguyễn Thành Tùng"},
        {"day": "Thứ 6", "time": "07:30 – 09:30", "subject": "Xử lý Ảnh", "room": "A205", "teacher": "TS. Võ Thị Hạnh"},
    ],
    "SV003": [
        {"day": "Thứ 2", "time": "07:30 – 09:30", "subject": "Kiểm thử Phần mềm", "room": "D201", "teacher": "TS. Bùi Văn Lâm"},
        {"day": "Thứ 3", "time": "09:45 – 11:45", "subject": "Phát triển Ứng dụng Di động", "room": "A401", "teacher": "ThS. Hoàng Minh Nhật"},
        {"day": "Thứ 4", "time": "13:00 – 15:00", "subject": "Quản lý Dự án PM", "room": "B102", "teacher": "TS. Trần Thị Oanh"},
        {"day": "Thứ 6", "time": "07:30 – 09:30", "subject": "Kiểm thử Phần mềm", "room": "D201", "teacher": "TS. Bùi Văn Lâm"},
    ],
}

GRADES_DB = {
    "SV001": {
        "HK1-2024": [
            {"subject": "Lập trình Python", "credits": 3, "midterm": 8.0, "final": 7.5, "gpa": 7.7},
            {"subject": "Cấu trúc Dữ liệu", "credits": 4, "midterm": 9.0, "final": 8.5, "gpa": 8.7},
            {"subject": "Toán Cao cấp 2", "credits": 3, "midterm": 6.5, "final": 7.0, "gpa": 6.8},
            {"subject": "Vật lý Đại cương", "credits": 3, "midterm": 7.0, "final": 7.5, "gpa": 7.3},
        ],
        "HK2-2024": [
            {"subject": "Trí tuệ Nhân tạo", "credits": 3, "midterm": 8.5, "final": None, "gpa": None},
            {"subject": "Cơ sở Dữ liệu", "credits": 4, "midterm": 9.0, "final": None, "gpa": None},
            {"subject": "Lập trình Web", "credits": 3, "midterm": 7.5, "final": None, "gpa": None},
            {"subject": "Mạng Máy tính", "credits": 3, "midterm": 8.0, "final": None, "gpa": None},
        ],
    },
    "SV002": {
        "HK1-2024": [
            {"subject": "Xác suất Thống kê", "credits": 3, "midterm": 9.0, "final": 9.5, "gpa": 9.3},
            {"subject": "Lập trình Java", "credits": 3, "midterm": 8.0, "final": 8.0, "gpa": 8.0},
            {"subject": "Hệ điều hành", "credits": 4, "midterm": 7.5, "final": 8.0, "gpa": 7.8},
        ],
        "HK2-2024": [
            {"subject": "Xử lý Ảnh", "credits": 3, "midterm": 8.5, "final": None, "gpa": None},
            {"subject": "Học Máy", "credits": 4, "midterm": 9.0, "final": None, "gpa": None},
            {"subject": "Toán rời rạc", "credits": 3, "midterm": 7.0, "final": None, "gpa": None},
        ],
    },
    "SV003": {
        "HK1-2024": [
            {"subject": "Phân tích Thiết kế HT", "credits": 4, "midterm": 8.0, "final": 8.5, "gpa": 8.3},
            {"subject": "Lập trình C#", "credits": 3, "midterm": 7.5, "final": 7.0, "gpa": 7.2},
        ],
        "HK2-2024": [
            {"subject": "Kiểm thử Phần mềm", "credits": 3, "midterm": 8.0, "final": None, "gpa": None},
            {"subject": "Phát triển Ứng dụng Di động", "credits": 3, "midterm": 7.5, "final": None, "gpa": None},
            {"subject": "Quản lý Dự án PM", "credits": 3, "midterm": 9.0, "final": None, "gpa": None},
        ],
    },
}

EXAMS_DB = {
    "SV001": [
        {"subject": "Trí tuệ Nhân tạo", "date": "2026-04-08", "time": "07:30 – 09:30", "room": "HT-A1", "format": "Tự luận + Trắc nghiệm"},
        {"subject": "Cơ sở Dữ liệu", "date": "2026-04-08", "time": "09:45 – 11:45", "room": "HT-B2", "format": "Thực hành máy tính"},
        {"subject": "Lập trình Web", "date": "2026-04-09", "time": "13:00 – 15:00", "room": "HT-A1", "format": "Báo cáo Đồ án"},
        {"subject": "Mạng Máy tính", "date": "2026-04-10", "time": "07:30 – 09:30", "room": "HT-C3", "format": "Trắc nghiệm"},
    ],
    "SV002": [
        {"subject": "Xử lý Ảnh", "date": "2026-04-08", "time": "07:30 – 09:30", "room": "HT-A1", "format": "Tự luận + Thực hành"},
        {"subject": "Học Máy", "date": "2026-04-09", "time": "09:45 – 11:45", "room": "HT-B2", "format": "Báo cáo Đồ án"},
        {"subject": "Toán rời rạc", "date": "2026-04-10", "time": "13:00 – 15:00", "room": "HT-C3", "format": "Tự luận"},
    ],
    "SV003": [
        {"subject": "Kiểm thử Phần mềm", "date": "2026-04-08", "time": "09:45 – 11:45", "room": "HT-A1", "format": "Thực hành máy tính"},
        {"subject": "Phát triển Ứng dụng Di động", "date": "2026-04-09", "time": "07:30 – 09:30", "room": "HT-B2", "format": "Báo cáo Đồ án"},
        {"subject": "Quản lý Dự án PM", "date": "2026-04-10", "time": "13:00 – 15:00", "room": "HT-C3", "format": "Tự luận + Trắc nghiệm"},
    ],
}

TUITIONS_DB = {
    "SV001": {
        "semester": "HK2-2024-2025",
        "credits": 19,
        "unit_price": 450000,
        "subtotal": 8550000,
        "discount_percent": 0,
        "discount_amount": 0,
        "total_due": 8550000,
        "paid_amount": 4500000,
        "outstanding_amount": 4050000,
        "due_date": "2025-04-15",
        "status": "Còn nợ học phí đợt 2",
    },
    "SV002": {
        "semester": "HK2-2024-2025",
        "credits": 17,
        "unit_price": 450000,
        "subtotal": 7650000,
        "discount_percent": 20,
        "discount_amount": 1530000,
        "total_due": 6120000,
        "paid_amount": 6120000,
        "outstanding_amount": 0,
        "due_date": "2025-04-15",
        "status": "Đã thanh toán",
    },
    "SV003": {
        "semester": "HK2-2024-2025",
        "credits": 16,
        "unit_price": 450000,
        "subtotal": 7200000,
        "discount_percent": 50,
        "discount_amount": 3600000,
        "total_due": 3600000,
        "paid_amount": 1800000,
        "outstanding_amount": 1800000,
        "due_date": "2025-04-15",
        "status": "Còn nợ học phí",
    },
}


def get_student_info(student_id: str) -> dict | None:
    return STUDENTS_DB.get(student_id)


def get_schedule(student_id: str) -> list | None:
    if student_id not in STUDENTS_DB:
        return None
    return SCHEDULES_DB.get(student_id, [])


def get_grades(student_id: str, semester: str | None = None) -> dict | list | None:
    if student_id not in STUDENTS_DB:
        return None
    grades = GRADES_DB.get(student_id, {})
    if semester:
        return grades.get(semester, [])
    return grades


def get_exam(student_id: str) -> list | None:
    if student_id not in STUDENTS_DB:
        return None
    return EXAMS_DB.get(student_id, [])


def get_tuition(student_id: str) -> dict | None:
    if student_id not in STUDENTS_DB:
        return None
    return TUITIONS_DB.get(student_id)


def get_all_students() -> list[dict]:
    return list(STUDENTS_DB.values())
