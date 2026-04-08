import enum
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from core.database import Base
from sqlalchemy.orm import relationship


class TransactionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    issue_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime)
    returned_date = Column(DateTime, nullable=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.ACTIVE)
    renewal_count = Column(Integer, default=0)

    user = relationship("User")
    book = relationship("Book")