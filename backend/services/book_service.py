from schemas.book_schema import CreateBookReq
from sqlalchemy.orm import Session
from models.book_model import Book
from fastapi import HTTPException
from models.borrow_model import BorrowRecord


def create_book(book: CreateBookReq, db: Session):

    existing_isbn = db.query(Book).filter(Book.isbn == book.isbn).first()

    if existing_isbn:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists.")

    existing_book_number = db.query(Book).filter(Book.bookNumber == book.bookNumber).first()

    if existing_book_number:
        raise HTTPException(status_code=400, detail="Book with this Book Number already exists.")

    new_book = Book (
        title = book.title,
        bookNumber = book.bookNumber,
        author = book.author,
        isbn = book.isbn,
        category = book.category,
        total_copies = book.total_copies,
        available_copies = book.total_copies
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


def get_all_books(db: Session):
    return db.query(Book).all()


def delete_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found.")
    
    if book.available_copies != book.total_copies:
        raise HTTPException(status_code=400, detail="Cannot Delete Book. Some Copies are Currently Issued to Employees.")

    db.delete(book)
    db.commit()

    return {"title": book.title, "response": "Book Deleted Successfully."}


def get_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found.")

    return book


def get_book_user_history(id: int, db: Session, hr):
    
    records = db.query(BorrowRecord).filter_by(book_id=id).all()

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