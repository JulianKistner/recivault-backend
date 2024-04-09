"""
	Workstep endpoints
"""
from pydantic import BaseModel, Field

from typing import Optional, List
from uuid import UUID

from src.api.models.general import APIHeader


class WorkstepBase(BaseModel):
    order_number: Optional[int] = Field(alias='orderNumber', validation_alias='order_number', default=None)
    workstep: Optional[str] = Field(alias='workstep', default=None, max_length=500)
    receipt_id: Optional[UUID] = Field(alias='receiptId', validation_alias='receipt_id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class WorkstepInDBBase(WorkstepBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow orm mapping
        from_attributes = True


class WorkstepCreate(WorkstepBase):
    workstep: Optional[str] = Field(alias='workstep', default=None, max_length=500)
    receipt_id: Optional[UUID] = Field(alias='receiptId', validation_alias='receipt_id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class WorkstepUpdate(WorkstepBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class WorkstepReadInDB(WorkstepInDBBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow orm mapping
        from_attributes = True


class WorkstepRead(WorkstepBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class WorkstepResponse(APIHeader):
    items: List[WorkstepRead] = Field(alias='items')

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
