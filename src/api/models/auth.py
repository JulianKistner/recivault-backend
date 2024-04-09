#/models.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    username: str
    email: str
    name: str
    realm_roles: list
    client_roles: list


class authConfiguration(BaseModel):
    server_url: str
    realm: str
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
