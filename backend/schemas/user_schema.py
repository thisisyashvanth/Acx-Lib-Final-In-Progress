from pydantic import BaseModel, EmailStr
from models.user_model import RoleEnum
from datetime import datetime


class GetUserResp(BaseModel):
    id: int
    employee_id: str
    name: str
    email: EmailStr
    role: RoleEnum
    is_restricted: bool
    restricted_until: datetime | None

    model_config = {
        "from_attributes": True
    }


class DeleteUserResp(BaseModel):
    response: str