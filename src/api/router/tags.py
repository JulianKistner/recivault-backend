"""
    Tag endpoints
"""

from fastapi import APIRouter, Depends, status, Body, Path
from sqlalchemy.orm import Session
from uuid import UUID
from starlette.responses import JSONResponse, Response
from starlette.requests import Request

from src.database.database import get_db

from src.api.models.tags import TagResponse, TagCreate
from src.service.tags import serv_get_tag, serv_get_tags, serv_create_tag, serv_delete_tag

from src.authentication.auth import get_user_info


router = APIRouter(prefix="/api",
                   dependencies=[Depends(get_user_info)])


@router.post(
    "/tags",
    tags=["tags"],
    response_model=TagResponse,
    response_class=JSONResponse,
    description="Endpoint to create a tag",
    status_code=status.HTTP_201_CREATED,
    deprecated=False
)
def endp_create_tag(request: Request,
                    db_session: Session = Depends(get_db),
                    body: TagCreate = Body(alias='tagCreate',
                                           title='Tag Create Model')):
    """
    POST Endpoint to create a tag

    :param request: General request information
    :param db_session: Database session
    :param body: API post model
    :return: API response model
    """
    return serv_create_tag(request=request, db_session=db_session, body=body)


@router.get(
    "/tags",
    tags=["tags"],
    response_model=TagResponse,
    response_class=JSONResponse,
    description="Endpoint to get all tags",
    status_code=status.HTTP_200_OK,
    deprecated=False
)
def endp_get_tags(request: Request, db_session: Session = Depends(get_db)):
    """
    GET Endpoint to fetch all tags

    :param request: General request information
    :param db_session: Database session
    :return: API response model
    """
    return serv_get_tags(request=request, db_session=db_session)


@router.get(
    "/tags/{uuid}",
    tags=["tags"],
    response_model=TagResponse,
    response_class=JSONResponse,
    description="Endpoint to get a tag by id",
    status_code=status.HTTP_200_OK,
    deprecated=False
)
def endp_get_tag(request: Request,
                 db_session: Session = Depends(get_db),
                 uuid: UUID = Path(alias='uuid',
                                   title='UUID of tag')):
    """
    GET Endpoint to fetch a tag by id

    :param request: General request information
    :param db_session: Database session
    :param uuid: UUID of tag
    :return: API response model
    """
    return serv_get_tag(request=request, db_session=db_session, tag_id=uuid)


@router.delete(
    "/tags/{uuid}",
    tags=["tags"],
    response_class=Response,
    description="Endpoint to delete a tag",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=False
)
def endp_delete_tag(request: Request,
                    db_session: Session = Depends(get_db),
                    uuid: UUID = Path(alias='uuid',
                                      title='UUID of tag')):
    """
    DELETE Endpoint to delete a tag by id

    :param request: General request information
    :param db_session: Database session
    :param uuid: UUID of tag
    :return: HTTP Response
    """
    return serv_delete_tag(request=request, db_session=db_session, tag_id=uuid)
