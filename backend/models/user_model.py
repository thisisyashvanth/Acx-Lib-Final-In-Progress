import enum
from core.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, Enum

class RoleEnum(str, enum.Enum):
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    is_restricted = Column(Boolean, default=False)
    restricted_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())