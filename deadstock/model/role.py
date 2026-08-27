from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy import String
from typing import List

class Role(Base):
    __tablename__ = "user_role"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30))

    accesses: Mapped[List["RoleAccess"]] = relationship(back_populates="role")
    users: Mapped["User"] = relationship(back_populates="role")