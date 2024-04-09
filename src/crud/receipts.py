"""
	Receipt endpoints
"""
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select

from starlette import status
from starlette.exceptions import HTTPException

from typing import List
from uuid import UUID

from src.database.models.receipts import ReceiptDB
from src.database.database import save_entity_to_db, remove_entity_from_db


def save_receipt(db_session: Session, db_receipt: ReceiptDB) -> ReceiptDB:
    """
    saves a receipt entity to database

    :param db_session: Database session
    :param db_receipt: Database object    :return:
    """
    try:
        return save_entity_to_db(db_session=db_session, entity=db_receipt)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_receipts(db_session: Session) -> List[ReceiptDB]:
    """
    read all receipts in database

    :param db_session: Database Session
    :return: List of database objects
    """
    try:
        return db_session.execute(select(ReceiptDB)).scalars().all()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_receipt(db_session: Session, uuid: UUID) -> ReceiptDB:
    """
    read a receipt by id

    :param db_session: Database session
    :param uuid: UUID of receipt
    :return: Database object
    """
    try:
        return db_session.execute(select(ReceiptDB)
                                  .where(ReceiptDB.id == uuid)).scalars().one()

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Receipt with id "{uuid}" not found')
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def delete_receipt(db_session: Session, db_receipt: ReceiptDB):
    """
    delete a receipt entity from database

    :param db_session: Database session
    :param db_receipt: Database object
    """
    try:
        remove_entity_from_db(db_session=db_session, entity=db_receipt)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')
