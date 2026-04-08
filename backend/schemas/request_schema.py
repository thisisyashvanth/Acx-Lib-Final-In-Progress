from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.request_model import RequestStatus, RequestType


class CreateRequestReq(BaseModel):
    book_id: int
    request_type: RequestType


class CreateRequestResp(BaseModel):
    id: int
    message: str


class ReviewRequestReq(BaseModel):
    status: RequestStatus
    remarks: Optional[str] = None


class ReviewRequestResp(BaseModel):
    id: int
    status: RequestStatus
    message: str


class GetRequestResp(BaseModel):
    id: int
    user_id: int
    book_id: int
    request_type: RequestType
    status: RequestStatus
    requested_at: datetime
    reviewed_at: Optional[datetime]
    remarks: Optional[str]

    class Config:
        from_attributes = True


class ReviewRequestBody(BaseModel):
    approve: bool
    remarks: str | None = None