"""
    # Main module
"""


from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

import uvicorn

from src import settings
from src.api.router.system import router as system_router
from src.api.router.receipts import router as receipts_router
from src.api.router.ingredients import router as ingredients_router
from src.api.router.worksteps import router as worksteps_router
from src.api.router.tags import router as tag_router
from src.api.router.receipt_tag_link import router as receipt_tag_link_router


app = FastAPI(
    title=settings.FA_APP_NAME,
    version=settings.FA_APP_VERSION,
    docs_url="/api",
    terms_of_service="not available",
    openapi_url="/openapi.json",
    contact={
        "name": settings.MAINTAINER_NAME,
        "email": settings.MAINTAINER_EMAIL,
    },
    license_info={
        "name": "No license information",
        "url": "https://license-url-missing.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(receipts_router)
app.include_router(ingredients_router)
app.include_router(worksteps_router)
app.include_router(tag_router)
app.include_router(receipt_tag_link_router)


def init_app():
    """Initialize Fast API Application

    - Create FastAPI instance
    - Add Settings for CORS Policy
    - Add all router controller for additional endpoints

    :return: Instance of Fast API application with the new settings and added features
    """

    description = """
    Recivault Backend API
    """

    return app


def main():
    """main routine

    :return:
    """
    uvicorn.run(init_app(), port=settings.FA_PORT)


if __name__ == "__main__":
    main()
