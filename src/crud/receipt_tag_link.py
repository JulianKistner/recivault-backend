from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select

from starlette import status
from starlette.exceptions import HTTPException

from typing import List
from uuid import UUID

from src.database.models.receipt_tag_link import ReceiptTagLinkDB
from src.database.database import save_entity_to_db, remove_entity_from_db

def save_receipt_tag_link(db_session: Session, db_link: ReceiptTagLinkDB) -> ReceiptTagLinkDB:
    """
    Saves a receipt tag link to the database

    :param db_session: Database session
    :param db_link: Database object     :return:
    """
    try:
        return save_entity_to_db(db_session=db_session, entity=db_link)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def delete_receipt_tag_link(db_session: Session, db_link: ReceiptTagLinkDB):
    """
    Removes a receipt tag link from the database

    :param db_session: Database session
    :param db_link: Database object
    """
    try:
        remove_entity_from_db(db_session=db_session, entity=db_link)

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_receipt_tag_link(db_session: Session, receipt_id: UUID, tag_id: UUID) -> ReceiptTagLinkDB:
    """
    Read a receipt tag link by given ids

    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :param tag_id: UUID of tag
    :return: Database object
    """
    try:
        return db_session.execute(select(ReceiptTagLinkDB).where(ReceiptTagLinkDB.receipt_id == receipt_id,
                                                                 ReceiptTagLinkDB.tag_id == tag_id)).scalars().one()

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No Link found')
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_links_by_receipt(db_session: Session, receipt_id: UUID) -> List[ReceiptTagLinkDB]:
    """
    Read all links from one receipt

    :param db_session: Database session
    :param receipt_id: UUID of receipt
    :return: List of database objects
    """
    try:
        return (db_session.execute(select(ReceiptTagLinkDB).where(ReceiptTagLinkDB.receipt_id == receipt_id))
                .scalars().all())

    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')


def read_receipts_by_link(db_session: Session, tag_id: UUID) -> List[ReceiptTagLinkDB]:
    """
    Read all receipts linked to a tag

    :param db_session: Database session
    :param tag_id: UUID of tag
    :return: List of database objects
    """
    try:
        return (db_session.execute(select(ReceiptTagLinkDB).where(ReceiptTagLinkDB.tag_id == tag_id))
                .scalars().all())

    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database Error')
