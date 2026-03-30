from fastapi import APIRouter, Depends, HTTPException
from schemas.book_schema import CreateBookResp, CreateBookReq, DeleteBookResp, GetBookResp
from sqlalchemy.orm import Session
from core.database import get_db
from security.dependency import get_current_user, require_hr
from services import book_service
from models.borrow_model import BorrowRecord


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/add", response_model=CreateBookResp)
def create_book(book: CreateBookReq, db: Session = Depends(get_db), user=Depends(require_hr)):
    return book_service.create_book(book, db)

    
@router.get("/get-all", response_model=list[GetBookResp])
def get_all_books(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return book_service.get_all_books(db)


@router.get("/get/{id}", response_model=GetBookResp)
def get_book(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return book_service.get_book(id, db)


@router.delete("/remove/{id}", response_model=DeleteBookResp)
def delete_book(id: int, db: Session = Depends(get_db), user=Depends(require_hr)):
    return book_service.delete_book(id, db)



@router.get("/{book_id}/users")
def get_book_user_history(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only HR (recommended)
    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR allowed")

    records = db.query(BorrowRecord).filter_by(book_id=book_id).all()

    return [
        {
            "borrow_id": r.id,
            "user_id": r.user_id,
            "employee_id": r.user.employee_id,
            "employee_name": r.user.name,
            "issue_date": r.issue_date,
            "due_date": r.due_date,
            "returned_date": r.returned_date,
            "status": r.status,
            "renewal_count": r.renewal_count
        }
        for r in records
    ]