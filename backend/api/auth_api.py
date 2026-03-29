from fastapi import APIRouter, Depends
from schemas.auth_schema import UserLoginResp, UserLoginReq, UserSignupReq, UserSignupResp
from sqlalchemy.orm import Session
from core.database import get_db
from services import auth_service
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=UserLoginResp)
def login(user: UserLoginReq, db: Session = Depends(get_db)):
    return auth_service.login(user, db)


# For Swagger
@router.post("/swagger-login")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login_form(form_data, db)
    
   
@router.post("/signup", response_model=UserSignupResp)
def employee_signup(user: UserSignupReq, db: Session = Depends(get_db)):
    return auth_service.employee_signup(user, db)
    

@router.post("/hr-signup", response_model=UserSignupResp)
def hr_signup(hr: UserSignupReq, db: Session = Depends(get_db)):
    return auth_service.hr_signup(hr, db)