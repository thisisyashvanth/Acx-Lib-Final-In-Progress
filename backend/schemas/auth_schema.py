from pydantic import BaseModel, EmailStr, field_validator
from schemas.user_schema import GetUserResp
from models.user_model import RoleEnum
from datetime import datetime


class UserLoginResp(BaseModel):
    access_token: str
    token_type: str
    user: GetUserResp

    model_config = {
        "from_attributes": True
    }


class UserLoginReq(BaseModel):
    email: EmailStr
    password: str


class UserSignupResp(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    role: RoleEnum
    is_restricted: bool
    restricted_until: datetime | None

    model_config = {
        "from_attributes": True
    }


class UserSignupReq(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    password: str

    @field_validator("email")
    def validate_company_email(cls, email: EmailStr):
        try:
            local, domain = email.rsplit("@", 1)
        except ValueError:
            raise ValueError("Invalid Email Format.")

        if domain.lower() != "acxhange.com":
            raise ValueError("Only acxhange.com Emails Are Allowed.")

        return email