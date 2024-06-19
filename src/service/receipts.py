"""
    Receipt endpoints
"""

from fastapi import status
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.requests import Request
from uuid import UUID, uuid4
from typing import List

from src.database.models.ingredients import IngredientDB
from src.database.models.worksteps import WorkstepDB
from src.pdf.receipt_pdf import ReceiptPDF
from src.api.models.auth import User
from src.crud.receipts import (save_receipt,
                               delete_receipt,
                               read_receipt,
                               read_receipts)
from src.crud.ingredients import read_ingredients_by_receipt
from src.crud.worksteps import read_worksteps_by_receipt

from src.api.models.receipts import (ReceiptUpdate,
                                     ReceiptCreate,
                                     ReceiptResponse,
                                     ReceiptRead,
                                     ReceiptReadInDB)

from src.api.models.ingredients import IngredientReadInDB
from src.api.models.worksteps import WorkstepReadInDB
from src.database.models.receipts import ReceiptDB


def serv_create_receipt(request: Request, db_session: Session, body: ReceiptCreate, user: User) -> ReceiptResponse:
    """
    # Service to create a receipt

    :param body: API post model
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_receipt: ReceiptDB = ReceiptDB(**body.dict())
        db_receipt.id = uuid4()
        db_receipt.user_id = user.id

        db_receipt = save_receipt(db_session=db_session, db_receipt=db_receipt)

        tmp_receipt: ReceiptReadInDB = ReceiptReadInDB.from_orm(db_receipt)
        api_receipt: ReceiptRead = ReceiptRead(**tmp_receipt.dict())

        return ReceiptResponse(method=request.method,
                               items=[api_receipt])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_receipts(request: Request, db_session: Session, user: User) -> ReceiptResponse:
    """
    # Service to request all receipts

    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_receipts: List[ReceiptDB] = read_receipts(db_session=db_session, user_id=user.id)

        api_receipts: List[ReceiptRead] = []

        for db_receipt in db_receipts:
            tmp_receipt: ReceiptReadInDB = ReceiptReadInDB.from_orm(db_receipt)
            api_receipt: ReceiptRead = ReceiptRead(**tmp_receipt.dict())
            api_receipts.append(api_receipt)

        return ReceiptResponse(method=request.method,
                               items=api_receipts)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_receipt(request: Request, db_session: Session, uuid: UUID, user: User) -> ReceiptResponse:
    """
    # Service to request a receipt by id

    :param uuid: UUID of receipt
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=uuid)
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        tmp_receipt: ReceiptReadInDB = ReceiptReadInDB.from_orm(db_receipt)
        api_receipt: ReceiptRead = ReceiptRead(**tmp_receipt.dict())

        return ReceiptResponse(method=request.method,
                               items=[api_receipt])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_receipt_pdf(request: Request, db_session: Session, uuid: UUID, user: User):
    """
    Service to generate a pdf of receipt

    :param request: General request information
    :param db_session: Database session
    :param uuid: UUID of receipt
    :param user: User information
    :return: PDF File
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=uuid)
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        tmp_receipt: ReceiptReadInDB = ReceiptReadInDB.from_orm(db_receipt)

        ingredients: List[IngredientReadInDB] = []

        db_ingredients: List[IngredientDB] = read_ingredients_by_receipt(db_session=db_session,
                                                                         receipt_id=tmp_receipt.id)

        for tmp_ingredient in db_ingredients:
            ingredients.append(IngredientReadInDB.from_orm(tmp_ingredient))

        worksteps: List[WorkstepReadInDB] = []

        db_worksteps: List[WorkstepDB] = read_worksteps_by_receipt(db_session=db_session, receipt_id=tmp_receipt.id)

        for tmp_workstep in db_worksteps:
            worksteps.append(WorkstepReadInDB.from_orm(tmp_workstep))

        receipt_pdf = ReceiptPDF()
        receipt_pdf.add_page()
        receipt_pdf.chapter_title(title=tmp_receipt.title)
        receipt_pdf.chapter_description(description=tmp_receipt.description)
        receipt_pdf.chapter_ingredients(ingredients=ingredients)
        receipt_pdf.chapter_worksteps(worksteps=worksteps)

        pdf_bytes = receipt_pdf.output(dest='S').encode('latin1')
        return Response(content=pdf_bytes, media_type="application/pdf",
                        headers={"Content-Disposition": f"attachment;filename={tmp_receipt.title}.pdf"})

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_update_receipt(request: Request, db_session: Session, uuid: UUID, body: ReceiptUpdate,
                        user: User) -> ReceiptResponse:
    """
    # Service to update an existing receipt

    :param body: API patch model
    :param uuid: UUID of receipt
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        patch_items = body.dict(exclude_unset=True)

        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=uuid)
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        if patch_items:
            for key, value in patch_items.items():
                setattr(db_receipt, key, value)

        db_receipt = save_receipt(db_session=db_session, db_receipt=db_receipt)

        tmp_receipt: ReceiptReadInDB = ReceiptReadInDB.from_orm(db_receipt)
        api_receipt: ReceiptRead = ReceiptRead(**tmp_receipt.dict())

        return ReceiptResponse(method=request.method,
                               items=[api_receipt])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_delete_receipt(request: Request, db_session: Session, uuid: UUID, user: User):
    """
    # Service to remove a receipt

    :param uuid: UUID of receipt
    :param request: General request information
    :param db_session: Database session
    :param user: User information
    :return: API response model
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=uuid)
        if not db_receipt.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not owner of the receipt')

        delete_receipt(db_session=db_session, db_receipt=db_receipt)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
