"""
    Workstep endpoints
"""
import uuid

from fastapi import status
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.requests import Request
from typing import List
from starlette.exceptions import HTTPException
from uuid import UUID

from src.api.models.auth import User
from src.api.models.worksteps import (WorkstepResponse,
                                      WorkstepCreate,
                                      WorkstepUpdate,
                                      WorkstepRead,
                                      WorkstepReadInDB)
from src.database.models.worksteps import WorkstepDB
from src.database.models.receipts import ReceiptDB

from src.crud.worksteps import save_workstep, read_workstep, read_worksteps_by_receipt, delete_workstep
from src.crud.receipts import read_receipt


def serv_create_workstep(request: Request,
                         db_session: Session,
                         body: WorkstepCreate,
                         user: User):
    """
    service to create a workstep

    :param body: API post model
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_worksteps: List[WorkstepDB] = read_worksteps_by_receipt(db_session=db_session, receipt_id=body.receipt_id)
        new_order_number: int = len(db_worksteps) + 1

        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=body.receipt_id)
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        db_workstep: WorkstepDB = WorkstepDB(**body.dict(exclude={'receipt_id',
                                                                  'order_number'}),
                                             order_number=new_order_number)
        db_workstep.receipt_id = db_receipt.id
        db_workstep.id = uuid.uuid4()

        db_workstep = save_workstep(db_session=db_session, db_workstep=db_workstep)

        tmp_workstep: WorkstepReadInDB = WorkstepReadInDB.model_validate(db_workstep)
        api_workstep: WorkstepRead = WorkstepRead(**tmp_workstep.dict())

        return WorkstepResponse(method=request.method,
                                items=[api_workstep])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_worksteps_by_receipt(request: Request,
                                  db_session: Session,
                                  receipt_id: UUID,
                                  user: User):
    """
    service to request all worksteps of a receipt

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

        db_worksteps: List[WorkstepDB] = read_worksteps_by_receipt(db_session=db_session, receipt_id=receipt_id)

        api_worksteps: List[WorkstepRead] = []

        for db_workstep in db_worksteps:
            tmp_workstep: WorkstepReadInDB = WorkstepReadInDB.model_validate(db_workstep)
            api_workstep: WorkstepRead = WorkstepRead(**tmp_workstep.dict())

            api_worksteps.append(api_workstep)

        api_worksteps.sort(key=lambda x: x.order_number)

        return WorkstepResponse(method=request.method,
                                items=api_worksteps)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_workstep_by_id(request: Request,
                            db_session: Session,
                            uuid: UUID,
                            user: User):
    """
    service to request workstep by uuid

    :param uuid: UUID of workstep
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_workstep: WorkstepDB = read_workstep(db_session=db_session, uuid=uuid)

        tmp_workstep: WorkstepReadInDB = WorkstepReadInDB.model_validate(db_workstep)

        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=tmp_workstep.receipt_id)
          
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        api_workstep: WorkstepRead = WorkstepRead(**tmp_workstep.dict())

        return WorkstepResponse(method=request.method,
                                items=[api_workstep])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_update_workstep(request: Request,
                         db_session: Session,
                         uuid: UUID,
                         body: WorkstepUpdate,
                         user: User):
    """
    service to update workstep

    :param body: API patch model
    :param uuid: UUID of workstep
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        patch_items = body.dict(exclude_unset=True,
                                exclude={'receipt_id',
                                         'order_number'})

        db_workstep: WorkstepDB = read_workstep(db_session=db_session, uuid=uuid)

        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=db_workstep.receipt_id)
          
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        if patch_items:
            for key, value in patch_items.items():
                setattr(db_workstep, key, value)

        db_workstep = save_workstep(db_session=db_session, db_workstep=db_workstep)

        tmp_workstep: WorkstepReadInDB = WorkstepReadInDB.model_validate(db_workstep)
        api_workstep: WorkstepRead = WorkstepRead(**tmp_workstep.dict())

        return WorkstepResponse(method=request.method,
                                items=[api_workstep])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_delete_workstep(request: Request,
                         db_session: Session,
                         uuid: UUID,
                         user: User):
    """
    service to remove a workstep

    :param uuid: UUID of workstep
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_workstep: WorkstepDB = read_workstep(db_session=db_session, uuid=uuid)
        receipt_id: UUID = db_workstep.receipt_id

        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=receipt_id)

        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        delete_workstep(db_session=db_session, db_workstep=db_workstep)

        db_worksteps: List[WorkstepDB] = read_worksteps_by_receipt(db_session=db_session, receipt_id=receipt_id)
        db_worksteps.sort(key=lambda x: x.order_number)

        new_order: int = 1
        for db_workstep in db_worksteps:
            db_workstep.order_number = new_order
            save_workstep(db_session=db_session, db_workstep=db_workstep)
            new_order += 1

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
