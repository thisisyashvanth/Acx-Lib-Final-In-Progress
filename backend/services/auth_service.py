from schemas.auth_schema import UserLoginReq, UserSignupReq
from sqlalchemy.orm import Session
from models.user_model import User
from fastapi import HTTPException
from security.security import create_token, hash_password, verify_password
from models.user_model import RoleEnum
from schemas.user_schema import GetUserResp


def employee_signup(employee: UserSignupReq, db: Session):
    isExistingEmail = db.query(User).filter(User.email == employee.email).first()
    isExistingEmployeeId = db.query(User).filter(User.employee_id == employee.employee_id).first()

    if isExistingEmail or isExistingEmployeeId:
        raise HTTPException(status_code=400, detail="User Already Exists.")

    new_user = User (
        employee_id = employee.employee_id,
        name = employee.name,
        email = employee.email,
        hashed_password = hash_password(employee.password),
        role = RoleEnum.EMPLOYEE
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def hr_signup(hr: UserSignupReq, db: Session):
    existing = db.query(User).filter(User.email == hr.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="HR Already Exists.")

    new_user = User (
        employee_id = hr.employee_id,
        name = hr.name,
        email = hr.email,
        hashed_password = hash_password(hr.password),
        role = RoleEnum.HR
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login(user: UserLoginReq, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="User Doesn't Exist. Create an Account First.")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials.")

    payload = {
        "sub": str(db_user.id),
        "role": db_user.role.value
    }

    token = create_token(payload)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": GetUserResp.model_validate(db_user)
    }