#/auth.py
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from src.settings import keycloakConfig
from fastapi import Security, HTTPException, status,Depends
from pydantic import Json
from src.api.models.auth import User

# This is used for fastapi docs authentification
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=keycloakConfig.authorization_url,
    tokenUrl=keycloakConfig.token_url,
)

# This actually does the auth checks
# client_secret_key is not mandatory if the client is public on keycloak
keycloak_openid = KeycloakOpenID(
    server_url=keycloakConfig.server_url, # https://sso.example.com/auth/
    client_id=keycloakConfig.client_id, # backend-client-id
    realm_name=keycloakConfig.realm, # example-realm
    verify=True
)

async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

# Get the payload/token from keycloak
async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,
            key= await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

# Get user infos from the payload
async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            name=payload.get("given_name"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("realm_access", {}).get("roles", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
