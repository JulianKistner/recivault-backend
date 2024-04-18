#/models.py
from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    id: UUID
    username: str
    realm_roles: list
    client_roles: list


class authConfiguration(BaseModel):
    server_url: str
    realm: str
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
