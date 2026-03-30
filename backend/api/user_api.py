from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schema import GetUserResp, DeleteUserResp 
from sqlalchemy.orm import Session
from core.database import get_db
from services import user_service
from models.borrow_model import BorrowRecord
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

    return [
        {
            "borrow_id": r.id,
            "book_id": r.book_id,
            "book_title": r.book.title,
            "issue_date": r.issue_date,
            "due_date": r.due_date,
            "returned_date": r.returned_date,
            "status": r.status,
            "renewal_count": r.renewal_count
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