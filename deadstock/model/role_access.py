from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy import String

class RoleAccess(Base):
    __tablename__ = "role_access"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30))

    role: Mapped["Role"] = relationship(back_populates="accesses")