"""
    # settings module with general project settings
"""

import os
import uuid

from src.api.models.auth import authConfiguration


def load_env_with_default(env_name: str, default_value):
    if env_name in os.environ:
        return os.environ[env_name]
    else:
        return default_value


MAINTAINER_NAME: str = "Julian Kistner"
MAINTAINER_EMAIL: str = "jul.kistner.21@lehre.mosbach.dhbw.de"

FA_HOST: str = "localhost"
FA_PORT: int = 5000
FA_APP_NAME: str = "recivault-backend"
FA_APP_VERSION: str = "3.0.0"
FA_APP_UUID: str = str(uuid.uuid4())

DATABASE_URI = load_env_with_default(
    "DATABASE_URI",
    "",
)

keycloakConfig = authConfiguration(
    server_url="https://accounts.recivault.com/",
    realm="recivault",
    client_id="recivault-client",
    client_secret="",
    authorization_url="https://accounts.recivault.com/realms/recivault/protocol/openid-connect/auth",
    token_url="https://accounts.recivault.com/realms/recivault/protocol/openid-connect/token",
)
