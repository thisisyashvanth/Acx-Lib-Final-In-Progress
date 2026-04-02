from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schema import GetUserResp, DeleteUserResp 
from sqlalchemy.orm import Session
from core.database import get_db
from services import user_service
from models.borrow_model import BorrowRecord
from models.request_model import RequestStatus, RequestType, Requests
from security.dependency import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/my-books")
def get_my_books(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    records = db.query(BorrowRecord).filter_by(
        user_id=current_user.id
    ).all()

    borrow_ids = [record.id for record in records]
    pending_requests_by_borrow: dict[int, list[str]] = {}

    if borrow_ids:
        pending_requests = db.query(Requests).filter(
            Requests.user_id == current_user.id,
            Requests.borrow_id.in_(borrow_ids),
            Requests.status == RequestStatus.PENDING,
            Requests.request_type.in_([RequestType.RENEW, RequestType.RETURN])
        ).all()

        for request in pending_requests:
            pending_requests_by_borrow.setdefault(request.borrow_id, []).append(request.request_type.value)

    return [
        {
            "borrow_id": r.id,
            "book_id": r.book_id,
            "book_title": r.book.title,
            "issue_date": r.issue_date,
            "due_date": r.due_date,
            "returned_date": r.returned_date,
            "status": r.status,
            "renewal_count": r.renewal_count,
            "pending_request_types": pending_requests_by_borrow.get(r.id, [])
        }
        for r in records
    ]


@router.get("/get-all", response_model=list[GetUserResp])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


@router.get("/{id}", response_model=GetUserResp)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(id, db)


@router.delete("/{id}", response_model=DeleteUserResp)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(id, db)


@router.get("/{id}/history")
def get_user_history(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    records = db.query(BorrowRecord).filter_by(user_id=id).all()

    if not records:
        return []

    return [
        {
            "borrow_id": r.id,
            "status": r.status,
            "borrow_date": r.issue_date,
            "due_date": r.due_date,
            "return_date": r.returned_date,
            "renewal_count": r.renewal_count,
            "book": {
                "id": r.book.id,
                "title": r.book.title,
                "author": r.book.author,
                "category": r.book.category
            }
        }
        for r in records
    ]
