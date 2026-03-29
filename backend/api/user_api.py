from fastapi import APIRouter, Depends
from schemas.user_schema import GetUserResp, DeleteUserResp 
from sqlalchemy.orm import Session
from core.database import get_db
from services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/get-all", response_model=list[GetUserResp])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


@router.get("/{id}", response_model=GetUserResp)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(id, db)


@router.delete("/{id}", response_model=DeleteUserResp)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(id, db)