"""
Receipt endpoints
"""
from src.database.database import Base
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from uuid import UUID, uuid4


class ReceiptDB(Base):
    """
    Database Model of Receipt Table
    """
    __tablename__ = "receipts"
    __table_args__ = {'schema': 'public'}

    id: Mapped[UUID] = mapped_column("id", UUID_DB, primary_key=True, nullable=False, default=uuid4())
    title: Mapped[str] = mapped_column("title", VARCHAR(50), nullable=False)
    description: Mapped[str] = mapped_column("description", VARCHAR(200), nullable=True)
    user_id: Mapped[UUID] = mapped_column("user_id", UUID_DB, nullable=False)
