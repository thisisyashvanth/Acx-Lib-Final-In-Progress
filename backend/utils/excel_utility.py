from openpyxl import Workbook
from io import BytesIO


def generate_users_excel(users: list):

    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    headers = [
        "User ID", "Name", "Employee ID",
        "Email", "Role", "Restricted"
    ]
    ws.append(headers)

    for user in users:
        ws.append([
            user.get("id"),
            user.get("name"),
            user.get("employee_id"),
            user.get("email"),
            user.get("role"),
            "Restricted" if user.get("is_restricted") else "Active"
        ])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream


def generate_requests_excel(requests: list):
    wb = Workbook()
    ws = wb.active
    ws.title = "Request History"

    headers = [
        "Request ID",
        "Book",
        "Employee",
        "Type",
        "Requested On",
        "Reviewed On",
        "Status",
        "Remarks"
    ]
    ws.append(headers)

    for r in requests:
        ws.append([
            r.get("id"),
            r.get("book_title"),
            r.get("user_name"),
            r.get("request_type"),
            r.get("request_date"),
            r.get("return_date"),
            r.get("status"),
            r.get("remarks")
        ])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream