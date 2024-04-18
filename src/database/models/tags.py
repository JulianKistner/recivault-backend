"""
Tag DB model
"""
from src.database.database import Base
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from uuid import UUID


class TagDB(Base):
    """"
    Database Model of Receipt Table
    """
    __tablename__ = "tags"
    __table_args__ = {'schema': 'public'}

    id: Mapped[UUID] = mapped_column("id", UUID_DB, primary_key=True, nullable=False)
    tag: Mapped[str] = mapped_column("tag", VARCHAR(20), nullable=False)
