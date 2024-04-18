from fastapi import status
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.requests import Request
from uuid import UUID
from typing import List

from src.api.models.tags import TagResponse, TagRead, TagReadInDB
from src.api.models.auth import User
from src.crud.tags import read_tag, delete_tag
from src.crud.receipts import read_receipt
from src.crud.receipt_tag_link import (read_receipt_tag_link,
                                       read_links_by_receipt,
                                       read_receipts_by_link,
                                       save_receipt_tag_link,
                                       delete_receipt_tag_link)
from src.database.models.receipts import ReceiptDB
from src.database.models.receipt_tag_link import ReceiptTagLinkDB
from src.database.models.tags import TagDB


def serv_create_receipt_tag_link(request: Request, db_session: Session, receipt_id: UUID, tag_id: UUID, user: User):
    """
    Service to link receipt and tag

    :param request: General request information
    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param tag_id: UUID of tag
    :param user: User information
    :return: HTTP Response
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=receipt_id)

        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        db_tag: TagDB = read_tag(db_session=db_session, uuid=tag_id)

        db_receipt_tag_link: ReceiptTagLinkDB = ReceiptTagLinkDB()
        db_receipt_tag_link.receipt_id = db_receipt.id
        db_receipt_tag_link.tag_id = db_tag.id

        save_receipt_tag_link(db_session=db_session, db_link=db_receipt_tag_link)

        return Response(status_code=status.HTTP_201_CREATED, content='Linked')

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_delete_receipt_tag_link(request: Request, db_session: Session, receipt_id: UUID, tag_id: UUID, user: User):
    """
    Service to unlink a receipt and tag

    :param request: General request information
    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param tag_id: UUID of tag
    :param user: User information
    :return: HTTP Response
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=receipt_id)

        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        db_tag: TagDB = read_tag(db_session=db_session, uuid=tag_id)

        db_receipt_tag_link: ReceiptTagLinkDB = read_receipt_tag_link(db_session=db_session, receipt_id=db_receipt.id,
                                                                      tag_id=db_tag.id)

        delete_receipt_tag_link(db_session=db_session, db_link=db_receipt_tag_link)

        db_receipt_tag_links: List[ReceiptTagLinkDB] = read_receipts_by_link(db_session=db_session, tag_id=db_tag.id)

        if len(db_receipt_tag_links) == 0:
            delete_tag(db_session=db_session, db_tag=db_tag)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_read_tags_by_receipt(request: Request, db_session: Session, receipt_id: UUID, user: User) -> TagResponse:
    """
    Service to get all Tags of a link

    :param request: General request information
    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param user: User information
    :return: API response model
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=receipt_id)

        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        db_receipt_tag_links: List[ReceiptTagLinkDB] = read_links_by_receipt(db_session=db_session,
                                                                             receipt_id=receipt_id)

        api_tags: List[TagRead] = []

        for db_receipt_tag_link in db_receipt_tag_links:
            db_tag: TagDB = read_tag(db_session=db_session, uuid=db_receipt_tag_link.tag_id)
            tmp_tag: TagReadInDB = TagReadInDB.model_validate(db_tag)
            api_tag: TagRead = TagRead(**tmp_tag.dict())
            api_tags.append(api_tag)

        return TagResponse(method=request.method,
                           items=api_tags)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
