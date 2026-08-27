from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, ForeignKey
from uuid import UUID, uuid4
from datetime import datetime

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(11))
    email: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[datetime] = mapped_column(DateTime)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("user_role.id"))

    role: Mapped["Role"] = relationship(back_populates="users")