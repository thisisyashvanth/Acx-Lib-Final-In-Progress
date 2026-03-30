import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, String, func
from core.database import Base
from sqlalchemy.orm import relationship


class RequestType(str, enum.Enum):
    BORROW = "BORROW"
    RETURN = "RETURN"
    RENEW = "RENEW"


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Requests(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    borrow_id = Column(Integer, ForeignKey("borrow_records.id"), nullable=True)

    request_type = Column(Enum(RequestType), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)

    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    remarks = Column(String(255), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    book = relationship("Book")
    borrow_record = relationship("BorrowRecord")