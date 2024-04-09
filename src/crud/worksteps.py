"""
	Workstep endpoints
"""
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select

from starlette import status
from starlette.exceptions import HTTPException

from typing import List
from uuid import UUID

from src.database.models.worksteps import WorkstepDB
from src.database.database import save_entity_to_db, remove_entity_from_db


def save_workstep(db_session: Session, db_workstep: WorkstepDB) -> WorkstepDB:
    """
    Saves a workstep to database

    :param db_session: Database session
    :param db_workstep: Database object    :return:
    """
    try:
        return save_entity_to_db(db_session=db_session, entity=db_workstep)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_worksteps(db_session: Session) -> List[WorkstepDB]:
    """
    Read all worksteps in database

    :param db_session: Database session
    :return: List of database objects
    """
    try:
        return db_session.execute(select(WorkstepDB)).scalars().all()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_worksteps_by_receipt(db_session: Session, receipt_id: UUID) -> List[WorkstepDB]:
    """
    Read all worksteps in database by receipt

    :param receipt_id:
    :param db_session: Database session
    :return: List of database objects
    """
    try:
        return db_session.execute(select(WorkstepDB)
                                  .where(WorkstepDB.receipt_id == receipt_id)).scalars().all()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_workstep(db_session: Session, uuid: UUID) -> WorkstepDB:
    """
    Read a workstep by id

    :param db_session: Database session
    :param uuid: UUID of workstep
    :return: Database object
    """
    try:
        return db_session.execute(select(WorkstepDB)
                                  .where(WorkstepDB.id == uuid)).scalars().one()

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Receipt with id "{uuid}" not found')
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def delete_workstep(db_session: Session, db_workstep: WorkstepDB):
    """
    Removes a workstep from database

    :param db_session: Database session
    :param db_workstep: Database object
    """
    try:
        remove_entity_from_db(db_session=db_session, entity=db_workstep)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')
    