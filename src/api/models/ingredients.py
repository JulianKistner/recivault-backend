"""
	Ingredient endpoints
"""
from pydantic import BaseModel, Field

from typing import Optional, List
from uuid import UUID

from src.api.models.general import APIHeader


class IngredientBase(BaseModel):
    amount: Optional[int] = Field(alias='amount', default=None)
    unit: Optional[str] = Field(alias='unit', default=None, max_length=50)
    ingredient: Optional[str] = Field(alias='ingredientName', validation_alias='ingredient', default=None,
                                      max_length=200)
    receipt_id: Optional[UUID] = Field(alias='receiptId', validation_alias='receipt_id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class IngredientInDBBase(IngredientBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow orm mapping
        from_attributes = True


class IngredientCreate(IngredientBase):
    amount: int = Field(alias='amount')
    unit: str = Field(alias='unit', max_length=50)
    ingredient: str = Field(alias='ingredientName', max_length=200)
    receipt_id: UUID = Field(alias='receiptId')

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class IngredientUpdate(IngredientBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class IngredientReadInDB(IngredientInDBBase):
    pass

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
        # Allow orm mapping
        from_attributes = True


class IngredientRead(IngredientBase):
    id: UUID = Field(alias='id', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True


class IngredientResponse(APIHeader):
    items: List[IngredientRead] = Field(alias='items')

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
