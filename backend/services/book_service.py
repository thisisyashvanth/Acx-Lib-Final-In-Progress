from schemas.book_schema import CreateBookReq
from sqlalchemy.orm import Session
from models.book_model import Book
from fastapi import HTTPException


def create_book(book: CreateBookReq, db: Session):
    new_book = Book (
        title = book.title,
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

    db.delete(book)
    db.commit()

    return {"title": book.title, "response": "Book Deleted Successfully."}


def get_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found.")

    return book