from core.database import Base
from sqlalchemy import Column, Integer, String, CheckConstraint


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    category = Column(String(50))
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint('available_copies <= total_copies', name='check_copies'),
    )