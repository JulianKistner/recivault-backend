"""
    # Provides all general system endpoints
"""


from fastapi import APIRouter, status

from starlette.responses import JSONResponse

from src import settings


router = APIRouter(prefix="")


@router.get("/", tags=["root"])
async def root() -> JSONResponse:
    """
    Root point of the service
    :return: JSON Response with HTTP 200 status code and welcome message as content
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Welcome to Service: {settings.FA_APP_NAME}"},
    )


@router.get("/health", tags=["system"], status_code=status.HTTP_200_OK)
async def health() -> JSONResponse:
    """
    Health Check, necessary to check the availability of the service on kubernetes
    :return: JSON Response with HTTP 200 status code and message as content
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "OK"})


@router.get(
    "/version",
    tags=["system"],
    status_code=status.HTTP_200_OK,
)
async def version() -> JSONResponse:
    """
    Get App Version
    :return: JSON Response with HTTP 200 status code and version as content
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"version": settings.FA_APP_VERSION}
    )
