"""
	Ingredient endpoints
"""

from src.database.database import Base
from sqlalchemy import VARCHAR, ForeignKeyConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from uuid import UUID, uuid4, uuid1


class IngredientDB(Base):
    """
    Database Model of Ingredient Table
    """
    __tablename__ = "ingredients"
    __table_args__ = (ForeignKeyConstraint(['receipt_id'],
                                           ['public.receipts.id']),
                      {'schema': 'public'})

    id: Mapped[UUID] = mapped_column("id", UUID_DB, primary_key=True, nullable=False, default=uuid4())
    amount: Mapped[int] = mapped_column('amount', Integer, nullable=False)
    unit: Mapped[str] = mapped_column('unit', VARCHAR(50), nullable=False)
    ingredient: Mapped[str] = mapped_column('ingredient', VARCHAR(200), nullable=False)
    receipt_id: Mapped[UUID] = mapped_column('receipt_id', UUID_DB, nullable=False)

    receipt = relationship('ReceiptDB')
