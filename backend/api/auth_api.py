from fastapi import APIRouter, Depends
from schemas.auth_schema import UserLoginReq, UserLoginResp, UserSignupReq, UserSignupResp
from sqlalchemy.orm import Session
from core.database import get_db
from services import auth_service


router = APIRouter(prefix="/auth", tags=["Auth Routes"])

@router.post("/signup", response_model=UserSignupResp)
def employee_signup(employee: UserSignupReq, db: Session = Depends(get_db)):
    return auth_service.employee_signup(employee, db)
    

@router.post("/hr-signup", response_model=UserSignupResp)
def hr_signup(hr: UserSignupReq, db: Session = Depends(get_db)):
    return auth_service.hr_signup(hr, db)


@router.post("/login", response_model=UserLoginResp)
def login(user: UserLoginReq, db: Session = Depends(get_db)):
    return auth_service.login(user, db)