from pydantic import BaseModel, EmailStr
from models.user_model import RoleEnum
from datetime import datetime
from models.borrow_model import TransactionStatus
from schemas.book_schema import GetBasicBook


class GetUserBooksResp(BaseModel):
    borrow_id: int
    book_id: int
    book_title: str
    issue_date: datetime
    due_date: datetime
    returned_date: datetime | None
    status: TransactionStatus
    renewal_count: int

    model_config = {
        "from_attributes": True
    }


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


class GetUserHistoryResp(BaseModel):
    borrow_id: int
    status: TransactionStatus
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None
    renewal_count: int
    book: GetBasicBook

    model_config = {
        "from_attributes": True
    }