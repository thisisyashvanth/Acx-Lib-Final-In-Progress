from sqlalchemy.orm import Session
from models.borrow_model import BorrowRecord
from schemas.user_schema import GetUserBooksResp
from models.user_model import User
from fastapi import HTTPException
from schemas.user_schema import GetUserHistoryResp, GetBasicBook


def get_my_books(db: Session, current_user):
    records = db.query(BorrowRecord).filter_by(user_id=current_user.id).all()

    return [
        GetUserBooksResp(
            borrow_id=r.id,
            book_id=r.book_id,
            book_title=r.book.title,
            issue_date=r.issue_date,
            due_date=r.due_date,
            returned_date=r.returned_date,
            status=r.status,
            renewal_count=r.renewal_count
        )
        for r in records
    ]


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found.")

    return user


def delete_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found.")

    db.delete(user)
    db.commit()

    return {"response": "User Deleted Successfully"}


def get_user_history(id: int, db: Session):
    records = db.query(BorrowRecord).filter_by(user_id=id).all()

    if not records:
        return []

    return [
        GetUserHistoryResp(
            borrow_id=r.id,
            status=r.status,
            borrow_date=r.issue_date,
            due_date=r.due_date,
            return_date=r.returned_date,
            renewal_count=r.renewal_count,
            book=GetBasicBook(
                id=r.book.id,
                title=r.book.title,
                author=r.book.author,
                category=r.book.category
            )
        )
        for r in records
    ]