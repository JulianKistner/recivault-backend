"""
	Workstep endpoints
"""
from src.database.database import Base
from sqlalchemy import VARCHAR, ForeignKeyConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from uuid import UUID, uuid4


class WorkstepDB(Base):
    """
    Database Model of Workstep Table
    """
    __tablename__ = "worksteps"
    __table_args__ = (ForeignKeyConstraint(['receipt_id'],
                                           ['public.receipts.id']),
                      {'schema': 'public'})

    id: Mapped[UUID] = mapped_column("id", UUID_DB, primary_key=True, nullable=False, default=uuid4())
    order_number: Mapped[int] = mapped_column('order_number', Integer, nullable=False)
    workstep: Mapped[str] = mapped_column('workstep', VARCHAR(500), nullable=False)
    receipt_id: Mapped[UUID] = mapped_column('receipt_id', UUID_DB, nullable=False)

    receipt = relationship('ReceiptDB')
