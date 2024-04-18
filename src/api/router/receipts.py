"""
Receipt endpoints
"""

from fastapi import APIRouter, Depends, status, Body, Path
from sqlalchemy.orm import Session
from uuid import UUID
from starlette.responses import JSONResponse, Response
from starlette.requests import Request

from src.api.models.auth import User
from src.database.database import get_db
from src.api.models.receipts import ReceiptCreate, ReceiptUpdate, ReceiptResponse
from src.service.receipts import (
    serv_create_receipt,
    serv_delete_receipt,
    serv_update_receipt,
    serv_get_receipts,
    serv_get_receipt,
)
from src.authentication.auth import get_user_info


router = APIRouter(prefix="/api",
                   dependencies=[Depends(get_user_info)])


@router.post(
    "/receipts",
    tags=["receipts"],
    response_class=JSONResponse,
    response_model=ReceiptResponse,
    description="Endpoint to create receipt",
    status_code=status.HTTP_201_CREATED,
    deprecated=False,
)
def endp_create_receipt(request: Request,
                        db_session: Session = Depends(get_db),
                        body: ReceiptCreate = Body(alias='receiptCreate',
                                                   title='Receipt Create Model'),
                        user: User = Depends(get_user_info)):
    """
    POST Endpoint to create a receipt

    :param body: API post model
    :param request: General request information
    :param db_session: database session
    :param user: User information
    :return: API response model
    """
    return serv_create_receipt(request=request, db_session=db_session, body=body, user=user)


@router.get(
    "/receipts",
    tags=["receipts"],
    response_class=JSONResponse,
    response_model=ReceiptResponse,
    description="Endpoint to get all receipts",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_get_receipts(request: Request, db_session: Session = Depends(get_db), user: User = Depends(get_user_info)):
    """
    # GET Endpoint to fetch all receipts

    :param request: General request information
    :param db_session: database session
    :param user: User information
    :return: API response model
    """
    return serv_get_receipts(request=request, db_session=db_session, user=user)


@router.get(
    "/receipts/{uuid}",
    tags=["receipts"],
    response_class=JSONResponse,
    response_model=ReceiptResponse,
    description="Endpoint to get a receipt by id",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_get_receipt(request: Request,
                     db_session: Session = Depends(get_db),
                     uuid: UUID = Path(alias='uuid',
                                       title='UUID of receipt'),
                     user: User = Depends(get_user_info)):
    """
    # GET Endpoint to fetch a receipt by id

    :param uuid: # UUID of receipt
    :param request: General request information
    :param db_session: database session
    :param user: User information
    :return: API response model
    """
    return serv_get_receipt(request=request, db_session=db_session, uuid=uuid, user=user)


@router.patch(
    "/receipts/{uuid}",
    tags=["receipts"],
    response_class=JSONResponse,
    response_model=ReceiptResponse,
    description="Endpoint to update a receipt",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_update_receipt(request: Request,
                        db_session: Session = Depends(get_db),
                        uuid: UUID = Path(alias='uuid',
                                          title='UUID of receipt'),
                        body: ReceiptUpdate = Body(alias='receiptUpdate',
                                                   title='Receipt Patch Model'),
                        user: User = Depends(get_user_info)):
    """
    PATCH Endpoint to update a receipt

    :param body: API patch model
    :param uuid: UUID of receipt
    :param request: General request information
    :param db_session: database session
    :param user: User information
    :return: API response model
    """
    return serv_update_receipt(request=request, db_session=db_session, uuid=uuid, body=body, user=user)


@router.delete(
    "/receipts/{uuid}",
    tags=["receipts"],
    response_class=Response,
    description="Endpoint to delete a receipt",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=False,
)
def endp_delete_receipt(request: Request,
                        db_session: Session = Depends(get_db),
                        uuid: UUID = Path(alias='uuid',
                                          title='UUID of receipt'),
                        user: User = Depends(get_user_info)):
    """
    # DELETE Endpoint to remove a receipt

    :param uuid: UUID of receipt
    :param request: General request information
    :param db_session: database session
    :param user: User information
    :return: API response model
    """
    return serv_delete_receipt(request=request, db_session=db_session, uuid=uuid, user=user)
