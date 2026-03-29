from fastapi.security import OAuth2PasswordBearer
import os
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from jose import jwt, JWTError
from models.user_model import RoleEnum, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/swagger-login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Token.")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token.")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_hr(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.HR:
        raise HTTPException(status_code=403, detail="HR Access Required.")

    return current_user