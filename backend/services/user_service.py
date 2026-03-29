from sqlalchemy.orm import Session
from models.user_model import User
from fastapi import HTTPException


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(id: int, db: Session):
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