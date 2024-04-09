"""
    Ingredient endpoints
"""
import uuid

from fastapi import status
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.requests import Request
from uuid import UUID
from typing import List
from starlette.exceptions import HTTPException
from src.api.models.ingredients import (IngredientCreate,
                                        IngredientUpdate,
                                        IngredientResponse,
                                        IngredientRead,
                                        IngredientReadInDB)
from src.database.models.ingredients import IngredientDB
from src.database.models.receipts import ReceiptDB
from src.crud.ingredients import (save_ingredient,
                                  read_ingredients_by_receipt,
                                  read_ingredient,
                                  delete_ingredient)
from src.crud.receipts import read_receipt


def serv_create_ingredient(request: Request, db_session: Session, body: IngredientCreate) -> IngredientResponse:
    """
    service to create ingredient

    :param body: API post model
    :param request: General request information
    :param db_session: Database session
    :return: API response model
    """
    try:
        db_receipt: ReceiptDB = read_receipt(db_session=db_session, uuid=body.receipt_id)

        db_ingredient: IngredientDB = IngredientDB(**body.dict(exclude={'receipt_id'}))
        db_ingredient.receipt = db_receipt
        db_ingredient.id = uuid.uuid4()

        db_ingredient = save_ingredient(db_session=db_session, db_ingredient=db_ingredient)

        tmp_ingredient: IngredientReadInDB = IngredientReadInDB.model_validate(db_ingredient)
        api_ingredient: IngredientRead = IngredientRead(**tmp_ingredient.dict())

        return IngredientResponse(method=request.method,
                                  items=[api_ingredient])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_ingredient(request: Request, db_session: Session, uuid: UUID):
    """
    service to request an ingredient by id

    :param uuid: UUID of ingredient
    :param request: General request information
    :param db_session: Database session
    :return: API response model
    """
    try:
        db_ingredient: IngredientDB = read_ingredient(db_session=db_session, uuid=uuid)

        tmp_ingredient: IngredientReadInDB = IngredientReadInDB.model_validate(db_ingredient)
        api_ingredient: IngredientRead = IngredientRead(**tmp_ingredient.dict())

        return IngredientResponse(method=request.method,
                                  items=[api_ingredient])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_get_ingredients_by_receipt(request: Request, db_session: Session, receipt_id: UUID):
    """
    service to request ingredients of receipt

    :param receipt_id: UUID of receipt
    :param request: General request information
    :param db_session: Database session
    :return: API response model
    """
    try:
        db_ingredients: List[IngredientDB] = read_ingredients_by_receipt(db_session=db_session, receipt_id=receipt_id)

        api_ingredients: List[IngredientRead] = []

        for db_ingredient in db_ingredients:
            tmp_ingredient: IngredientReadInDB = IngredientReadInDB.model_validate(db_ingredient)
            api_ingredient: IngredientRead = IngredientRead(**tmp_ingredient.dict())

            api_ingredients.append(api_ingredient)

        return IngredientResponse(method=request.method,
                                  items=api_ingredients)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_update_ingredient(request: Request, db_session: Session, uuid: UUID, body: IngredientUpdate):
    """
    service to update ingredient

    :param body: API patch model
    :param uuid: UUID of ingredient
    :param request: General request information
    :param db_session: Database session
    :return: API response model
    """
    try:
        patch_items = body.dict(exclude_unset=True,
                                exclude={'receipt_id'})

        db_ingredient: IngredientDB = read_ingredient(db_session=db_session, uuid=uuid)

        if patch_items:
            for key, value in patch_items.items():
                setattr(db_ingredient, key, value)

        db_ingredient = save_ingredient(db_session=db_session, db_ingredient=db_ingredient)

        tmp_ingredient: IngredientReadInDB = IngredientReadInDB.model_validate(db_ingredient)
        api_ingredient: IngredientRead = IngredientRead(**tmp_ingredient.dict())

        return IngredientResponse(method=request.method,
                                  items=[api_ingredient])

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serv_delete_ingredient(request: Request, db_session: Session, uuid: UUID):
    """
    service to remove ingredient

    :param uuid: UUID of ingredient
    :param request: General request information
    :param db_session: Database session
    :return: API response model
    """
    try:
        db_ingredient: IngredientDB = read_ingredient(db_session=db_session, uuid=uuid)

        delete_ingredient(db_session=db_session, db_ingredient=db_ingredient)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
