from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from uuid import UUID
from starlette.responses import JSONResponse, Response
from starlette.requests import Request

from src.api.models.auth import User
from src.api.models.tags import TagResponse
from src.database.database import get_db

from src.service.receipt_tag_link import (serv_create_receipt_tag_link,
                                          serv_delete_receipt_tag_link,
                                          serv_read_tags_by_receipt)

from src.authentication.auth import get_user_info


router = APIRouter(prefix="/api",
                   dependencies=[Depends(get_user_info)])


@router.post(
    "/receipts/{receipt_id}/tags/{tag_id}",
    tags=['receipt-tag-links'],
    response_class=Response,
    description="Links a tag to a receipt",
    status_code=status.HTTP_201_CREATED,
    deprecated=False
)
def endp_create_receipt_tag_link(request: Request,
                                 db_session: Session = Depends(get_db),
                                 receipt_id: UUID = Path(alias='receipt_id',
                                                         title='UUID of receipt'),
                                 tag_id: UUID = Path(alias='tag_id',
                                                     title='UUID of tag'),
                                 user: User = Depends(get_user_info)):
    """
    POST Endpoint to create a receipt tag link

    :param request: General request information
    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param tag_id: UUID of tag
    :param user: User information
    :return: HTTP Respone
    """
    return serv_create_receipt_tag_link(request=request, db_session=db_session, receipt_id=receipt_id, tag_id=tag_id,
                                        user=user)


@router.delete(
    "/receipts/{receipt_id}/tags/{tag_id}",
    tags=['receipt-tag-links'],
    response_class=Response,
    description="Removes a link between receipt and tag",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=False
)
def endp_delete_receipt_tag_link(request: Request,
                                 db_session: Session = Depends(get_db),
                                 receipt_id: UUID = Path(alias='receipt_id',
                                                         title='UUID of receipt'),
                                 tag_id: UUID = Path(alias='tag_id',
                                                     title='UUID of tag'),
                                 user: User = Depends(get_user_info)):
    """
    Delete Endpoint to remove a receipt tag link

    :param request: General request information
    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param tag_id: UUID of tag
    :param user: User information
    :return: HTTP Respone
    """
    return serv_delete_receipt_tag_link(request=request, db_session=db_session, receipt_id=receipt_id, tag_id=tag_id,
                                        user=user)


@router.get(
    "/receipts/{receipt_id}/tags",
    tags=['receipt-tag-links'],
    response_class=JSONResponse,
    response_model=TagResponse,
    description="Get all links by a receipt",
    status_code=status.HTTP_200_OK,
    deprecated=False
)
def endp_get_tags_by_receipt(request: Request,
                             db_session: Session = Depends(get_db),
                             receipt_id: UUID = Path(alias='receipt_id',
                                                     title='UUID of receipt'),
                             user: User = Depends(get_user_info)):
    """
    GET Endpoint to fetch all links by receipt

    :param request: General request information
    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param user: User information
    :return: HTTP Respone
    """
    return serv_read_tags_by_receipt(request=request, db_session=db_session, receipt_id=receipt_id, user=user)
