"""
Ingredient endpoints
"""

from fastapi import APIRouter, Depends, status, Path, Body
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, Response
from starlette.requests import Request

from src.authentication.auth import get_user_info
from src.database.database import get_db
from src.service.ingredients import (
    serv_get_ingredient,
    serv_create_ingredient,
    serv_update_ingredient,
    serv_get_ingredients_by_receipt,
    serv_delete_ingredient,
)
from uuid import UUID
from src.api.models.ingredients import IngredientCreate, IngredientUpdate, IngredientResponse

router = APIRouter(prefix="/api",
                   dependencies=[Depends(get_user_info)])


@router.post(
    "/ingredients",
    tags=["ingredients"],
    response_class=JSONResponse,
    response_model=IngredientResponse,
    description="Endpoint to create a ingredient ",
    status_code=status.HTTP_201_CREATED,
    deprecated=False,
)
def endp_create_ingredient(request: Request,
                           db_session: Session = Depends(get_db),
                           body: IngredientCreate = Body(alias='ingredientCreate',
                                                         title='Ingredient Post Model')):
    """
    # POST Endpoint to create ingredient

    :param body: API post model
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_create_ingredient(request=request, db_session=db_session, body=body)


@router.get(
    "/ingredients/{uuid}",
    tags=["ingredients"],
    response_class=JSONResponse,
    response_model=IngredientResponse,
    description="Endpoint to get a ingredient by id",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_get_ingredient_by_id(request: Request,
                              db_session: Session = Depends(get_db),
                              uuid: UUID = Path(alias='uuid',
                                                title='UUID of ingredient')):
    """
    # GET Endpoint to fetch ingredient by id

    :param uuid: UUID of ingredient
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_get_ingredient(request=request, db_session=db_session, uuid=uuid)


@router.get(
    "/receipts/{receipt_id}/ingredients",
    tags=["ingredients"],
    response_class=JSONResponse,
    response_model=IngredientResponse,
    description="Endpoint to get ingredients by receipt",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_get_ingredients_by_receipt(request: Request,
                                    db_session: Session = Depends(get_db),
                                    receipt_id: UUID = Path(alias='receipt_id',
                                                            title='UUID of receipt')
                                    ):
    """
    GET Endpoint to fetch ingredient by receipt

    :param receipt_id: UUID of receipt
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_get_ingredients_by_receipt(request=request, db_session=db_session, receipt_id=receipt_id)


@router.patch(
    "/ingredients/{uuid}",
    tags=["ingredients"],
    response_class=JSONResponse,
    response_model=IngredientResponse,
    description="Endpoint to update ingredient",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_update_ingredient(request: Request,
                           db_session: Session = Depends(get_db),
                           uuid: UUID = Path(alias='uuid',
                                             title='UUID of ingredient'),
                           body: IngredientUpdate = Body(alias='ingredientUpdate',
                                                         title='Ingredient Patch Model')):
    """
    PATCH Endpoint to update ingredient

    :param body: API patch model
    :param uuid: UUID of ingredient
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_update_ingredient(request=request, db_session=db_session, uuid=uuid, body=body)


@router.delete(
    "/ingredients/{uuid}",
    tags=["ingredients"],
    response_class=Response,
    description="Endpoint to delete a ingredient",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=False,
)
def endp_delete_ingredient(request: Request,
                           db_session: Session = Depends(get_db),
                           uuid: UUID = Path(alias='uuid',
                                             title='UUID of ingredient')):
    """
    DELETE Endpoint to remove ingredient

    :param uuid: UUID of ingredient
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_delete_ingredient(request=request, db_session=db_session, uuid=uuid)
