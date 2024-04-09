"""
General api model
"""
from pydantic import BaseModel, Field

from src.settings import FA_APP_VERSION


class APIHeader(BaseModel):
    """
    API Header
    """
    api_version: str = Field(alias='version', default=FA_APP_VERSION)
    method: str = Field(alias='method', default=None)

    class Config:
        # Allows to use field and alias name
        allow_population_by_field_name = True
