from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateBookResp(BaseModel):
    title: str
    bookNumber: str
    author: str
    isbn: str
    category: str | None = None
    total_copies: int
    available_copies: int

    model_config = {
        "from_attributes": True
    }


class CreateBookReq(BaseModel):
    title: str
    author: str
    bookNumber: str
    isbn: str
    category: str
    total_copies: int


class GetBookResp(BaseModel):
    id: int
    title: str
    bookNumber: str
    author: str
    isbn: str
    category: str
    total_copies: int
    available_copies: int

    model_config = {
        "from_attributes": True
    }


class DeleteBookResp(BaseModel):
    title: str
    response: str

    model_config = {
        "from_attributes": True
    }


class GetBookUserHistoryResp(BaseModel):
    borrow_id: int
    user_id: int
    employee_id: str
    employee_name: str
    issue_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]
    status: str
    renewal_count: int
    
    model_config = {
        "from_attributes": True
    }


class GetBasicBook(BaseModel):
    id: int
    title: str
    author: str
    category: str | None

    model_config = {"from_attributes": True}