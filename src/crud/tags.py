"""
	tag crud functions
"""
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select

from starlette import status
from starlette.exceptions import HTTPException

from typing import List
from uuid import UUID

from src.database.models.tags import TagDB
from src.database.database import save_entity_to_db, remove_entity_from_db


def save_tag(db_session: Session, db_tag: TagDB) -> TagDB:
    """
    saves a new tag

    :param db_session: Database session
    :param db_tag: Database object     :return:
    """
    try:
        return save_entity_to_db(db_session=db_session, entity=db_tag)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_tags(db_session: Session) -> List[TagDB]:
    """
    read all tags in database

    :param db_session: Database session
    :return: List of database objects
    """

    try:
        return db_session.execute(select(TagDB)).scalars().all()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_tag(db_session: Session, uuid: UUID) -> TagDB:
    """
    read a tag by uuid

    :param db_session: Database session
    :param uuid: UUID of tag
    :return: Database obejct
    """
    try:
        return db_session.execute(select(TagDB).where(TagDB.id == uuid)).scalars().one()

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Receipt with id "{uuid}" not found')
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def delete_tag(db_session: Session, db_tag: TagDB):
    """
    delete a tag entity from database

    :param db_session: Database session
    :param db_tag: Database object
    """
    try:
        remove_entity_from_db(db_session=db_session, entity=db_tag)

    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')
