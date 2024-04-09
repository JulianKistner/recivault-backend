"""
	Ingredient endpoints
"""
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select

from starlette import status
from starlette.exceptions import HTTPException

from typing import List
from uuid import UUID

from src.database.models.ingredients import IngredientDB
from src.database.database import save_entity_to_db, remove_entity_from_db


def save_ingredient(db_session: Session, db_ingredient: IngredientDB) -> IngredientDB:
    """
    Saves an ingredient entity to database

    :param db_session: Database session
    :param db_ingredient: Database object    :return:
    """
    try:
        return save_entity_to_db(db_session=db_session, entity=db_ingredient)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_ingredients(db_session: Session) -> List[IngredientDB]:
    """
    Read all ingredients in database

    :param db_session: Database session
    :return: List of database objects
    """
    try:
        return db_session.execute(select(IngredientDB)).scalars().all()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_ingredients_by_receipt(db_session: Session, receipt_id: UUID) -> List[IngredientDB]:
    """
    Read all ingredients in database by receipt

    :param receipt_id: UUID of receipt
    :param db_session: Database session
    :return: List of database objects
    """
    try:
        return db_session.execute(select(IngredientDB)
                                  .where(IngredientDB.receipt_id == receipt_id)).scalars().all()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_ingredient(db_session: Session, uuid: UUID) -> IngredientDB:
    """
    Read an ingredient by id

    :param db_session: Database session
    :param uuid: UUID of ingredient
    :return: Database object
    """
    try:
        return db_session.execute(select(IngredientDB).
                                  where(IngredientDB.id == uuid)).scalars().one()

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Receipt with id "{uuid}" not found')
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def delete_ingredient(db_session: Session, db_ingredient: IngredientDB):
    """
    Remove an ingredient entity to database

    :param db_session: Database session
    :param db_ingredient: Database object
    """
    try:
        remove_entity_from_db(db_session=db_session, entity=db_ingredient)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')

