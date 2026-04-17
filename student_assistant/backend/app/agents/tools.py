AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_schedule",
            "description": "Lay lich hoc cua sinh vien trong tuan. Goi khi sinh vien hoi ve lich hoc, thoi khoa bieu, hom nay hoc gi, tuan nay hoc gi.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_grades",
            "description": "Lay bang diem cua sinh vien. Goi khi sinh vien hoi ve diem, ket qua hoc tap, GPA, diem mon hoc cu the.",
            "parameters": {
                "type": "object",
                "properties": {
                    "semester": {
                        "type": "string",
                        "description": "Hoc ky can xem (VD: HK1-2024, HK2-2024). Neu khong chi dinh, tra ve tat ca cac hoc ky.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_exam",
            "description": "Lay lich thi cuoi ky cua sinh vien. Goi khi sinh vien hoi ve lich thi, bao gio thi, phong thi, hinh thuc thi.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_tuition",
            "description": "Lay thong tin hoc phi ca nhan cua sinh vien. Goi khi sinh vien hoi ve hoc phi, hoc phi con no, da dong bao nhieu, han dong hoc phi.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]

RAG_TOOL = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Tim kiem thong tin trong tai lieu noi bo cua truong (quy che dao tao, quy dinh hoc phi, noi quy thi cu, thong bao hoc vu, huong dan su dung he thong). Goi khi sinh vien hoi ve quy dinh, quy che, chinh sach, thong bao, huong dan cua truong.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Cau hoi hoac tu khoa can tim kiem trong tai lieu noi bo",
                },
            },
            "required": ["query"],
        },
    },
}


def get_all_tools() -> list[dict]:
    """Return router tools used by the LLM to choose the right branch."""
    return [RAG_TOOL] + AGENT_TOOLS
