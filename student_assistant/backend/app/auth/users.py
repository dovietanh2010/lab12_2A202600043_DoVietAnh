USERS_DB: dict[str, dict] = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin",
        "display_name": "Quản trị viên",
        "student_id": None,
    },
    "sinhvien1": {
        "username": "sinhvien1",
        "password": "sv001",
        "role": "student",
        "display_name": "Nguyễn Văn An",
        "student_id": "SV001",
    },
    "sinhvien2": {
        "username": "sinhvien2",
        "password": "sv002",
        "role": "student",
        "display_name": "Trần Thị Bích",
        "student_id": "SV002",
    },
    "sinhvien3": {
        "username": "sinhvien3",
        "password": "sv003",
        "role": "student",
        "display_name": "Lê Hoàng Cường",
        "student_id": "SV003",
    },
}


def authenticate(username: str, password: str) -> dict | None:
    user = USERS_DB.get(username)
    if user and user["password"] == password:
        return {
            "username": user["username"],
            "role": user["role"],
            "display_name": user["display_name"],
            "student_id": user["student_id"],
        }
    return None
