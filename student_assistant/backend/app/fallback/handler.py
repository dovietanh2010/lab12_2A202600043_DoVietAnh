FALLBACK_RESPONSE = {
    "response": (
        "Minh chua ho tro truc tiep noi dung nay. "
        "Hien tai minh phu hop nhat voi cac nhu cau sau:\n\n"
        "- **Tai lieu noi bo**: Quy che dao tao, quy dinh hoc phi, noi quy thi cu, thong bao hoc vu\n"
        "- **Thong tin ca nhan**: Lich hoc, bang diem, lich thi, hoc phi ca nhan\n\n"
        "Neu ban can ho tro sau hon, ban co the lien he:\n"
        "- **Phong Dao tao**: Tang 2, Nha A, So 01 Dai Co Viet, Ha Noi\n"
        "- **Dien thoai**: (024) 3868-xxxx (ext. 123)\n"
        "- **Email**: daotao@university.edu.vn\n"
        "- **Gio lam viec**: Thu 2 - Thu 6, 8:00 - 11:30, 13:30 - 17:00"
    ),
    "sources": [],
    "tool_used": "fallback",
}


def get_fallback_response() -> dict:
    return FALLBACK_RESPONSE.copy()
