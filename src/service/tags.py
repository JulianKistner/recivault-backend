import uuid
import re

from fastapi import status
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.requests import Request
from uuid import UUID
from typing import List

from src.crud.tags import save_tag, delete_tag, read_tag, read_tags
from src.api.models.tags import TagResponse, TagCreate, TagReadInDB, TagRead
from src.database.models.tags import TagDB


def serv_create_tag(request: Request, db_session: Session, body: TagCreate) -> TagResponse:
    """
    Service to create a new tag

    :param request: General request information
    :param db_session: Database session
    :param body: API post model
    :return: API response model
    """
    try:
        regex = r'^[a-zA-Z]+$'

        if not re.match(regex, body.tag):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unallowed symbols in tag')

        body.tag = body.tag.upper()

        db_tag: TagDB = TagDB(**body.dict())
        db_tag.id = uuid.uuid4()

        db_tag = save_tag(db_session=db_session, db_tag=db_tag)

        tmp_tag: TagReadInDB = TagReadInDB.model_validate(db_tag)
        api_tag: TagRead = TagRead(**tmp_tag.dict())

        return TagResponse(method=request.method,
                           items=[api_tag])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_tags(request: Request, db_session: Session) -> TagResponse:
    """
    Service to get all tags

    :param request: General request informtion
    :param db_session: Database session
    :return: API response model
    """
    try:
        db_tags: List[TagDB] = read_tags(db_session=db_session)

        api_tags: List[TagRead] = []

        for db_tag in db_tags:
            tmp_tag: TagReadInDB = TagReadInDB.model_validate(db_tag)
            api_tag: TagRead = TagRead(**tmp_tag.dict())
            api_tags.append(api_tag)

        return TagResponse(method=request.method,
                           items=api_tags)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_tag(request: Request, db_session: Session, tag_id: UUID) -> TagResponse:
    """
    Service to get a tag by id

    :param request: General request information
    :param db_session: Database session
    :param tag_id: UUID of tag
    :return: API response model
    """
    try:
        db_tag: TagDB = read_tag(db_session=db_session, uuid=tag_id)

        tmp_tag: TagReadInDB = TagReadInDB.model_validate(db_tag)
        api_tag: TagRead = TagRead(**tmp_tag.dict())

        return TagResponse(method=request.method,
                           items=[api_tag])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_delete_tag(request: Request, db_session: Session, tag_id: UUID):
    """
    Service to delete a tag

    :param request: General request information
    :param db_session: Database session
    :param tag_id: UUID of tag
    :return: HTTP response
    """
    try:
        db_tag: TagDB = read_tag(db_session=db_session, uuid=tag_id)

        delete_tag(db_session=db_session, db_tag=db_tag)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

