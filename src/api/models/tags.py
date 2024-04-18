"""
	Tag endpoints
"""
from pydantic import BaseModel, Field

from typing import Optional, List
from uuid import UUID

from src.api.models.general import APIHeader


class TagBase(BaseModel):
    tag: Optional[str] = Field(alias='tag', default=None, max_length=20)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class TagInDBBase(TagBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow db mapping
        from_attributes = True


class TagCreate(TagBase):
    tag: str = Field(alias='tag', default=None, max_length=20)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class TagReadInDB(TagInDBBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow db mapping
        from_attributes = True


class TagRead(TagBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class TagResponse(APIHeader):
    items: List[TagRead] = Field(alias='items')

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
