"""
    Receipt Tag Linking
"""
from src.database.database import Base
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from uuid import UUID


class ReceiptTagLinkDB(Base):
    """
    Database Model of Receipt_Tag_Link Table
    """
    __tablename__ = "receipt_tag_links"
    __table_args__ = (ForeignKeyConstraint(['receipt_id'],
                                           ['public.receipts.id']),
                      ForeignKeyConstraint(['tag_id'],
                                           ['public.tags.id']),
                      {'schema': 'public'})

    receipt_id: Mapped[UUID] = mapped_column('receipt_id', UUID_DB, primary_key=True)
    tag_id: Mapped[UUID] = mapped_column('tag_id', UUID_DB, primary_key=True)

    relationship('ReceiptDB')
    relationship('TagDB')
