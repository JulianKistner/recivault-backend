"""
	Receipt endpoints
"""
from pydantic import BaseModel, Field

from typing import Optional, List
from uuid import UUID

from src.api.models.general import APIHeader


class ReceiptBase(BaseModel):
    title: Optional[str] = Field(alias='title', default=None, max_length=50)
    description: Optional[str] = Field(alias='description', default=None, max_length=500)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class ReceiptInDBBase(ReceiptBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow orm mapping
        orm_mode = True
        from_attributes = True


class ReceiptCreate(ReceiptBase):
    title: str = Field(alias='title', default=None, max_length=50)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class ReceiptUpdate(ReceiptBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class ReceiptReadInDB(ReceiptInDBBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow orm mapping
        orm_mode = True


class ReceiptRead(ReceiptBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class ReceiptResponse(APIHeader):
    items: List[ReceiptRead] = Field(alias='items')

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
