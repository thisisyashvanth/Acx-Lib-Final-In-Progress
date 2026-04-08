from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from core.database import get_db
from security.dependency import require_hr
from utils.excel_utility import generate_requests_excel, generate_users_excel


router = APIRouter(prefix="/hr", tags=["HR"])


@router.post("/export-users")
def export_users(users: list[dict], db: Session = Depends(get_db), hr = Depends(require_hr)):

    file_stream = generate_users_excel(users)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=users.xlsx"
        }
    )


@router.post("/export-requests")
def export_requests(requests: list[dict], current_user = Depends(require_hr)):

    file_stream = generate_requests_excel(requests)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=request_history.xlsx"
        }
    )