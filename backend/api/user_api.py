from fastapi import APIRouter, Depends
from schemas.user_schema import GetUserBooksResp, DeleteUserResp, GetUserResp, GetUserHistoryResp
from sqlalchemy.orm import Session
from core.database import get_db
from security.dependency import get_current_user, require_hr
from services import user_service


router = APIRouter(prefix="/users", tags=["User Routes"])


@router.get("/books", response_model=list[GetUserBooksResp])
def get_my_books(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return user_service.get_my_books(db, current_user)


@router.get("/get-all", response_model=list[GetUserResp])
def get_all_users(db: Session = Depends(get_db), hr = Depends(require_hr)):
    return user_service.get_all_users(db)


@router.get("/{id}", response_model=GetUserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    return user_service.get_user(id, db)


@router.delete("/{id}", response_model=DeleteUserResp)
def delete_user(id: int, db: Session = Depends(get_db), hr = Depends(require_hr)):
    return user_service.delete_user(id, db)


@router.get("/{id}/history", response_model=list[GetUserHistoryResp])
def get_user_history(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return user_service.get_user_history(id, db)