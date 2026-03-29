from fastapi import APIRouter, Depends
from schemas.book_schema import CreateBookResp, CreateBookReq, DeleteBookResp, GetBookResp
from sqlalchemy.orm import Session
from core.database import get_db
from security.dependency import get_current_user, require_hr
from services import book_service


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