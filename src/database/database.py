"""
    # Declares the database connection and the standard functions to persist the entities
"""


from fastapi import HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.settings import DATABASE_URI
from src.database.DatabaseException import CustomDatabaseException


engine = create_engine(DATABASE_URI, pool_size=1, max_overflow=2, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Get general database session
    """
    db = SessionLocal()
    try:
        # Grafana can be included here to track database transactions
        yield db
    finally:
        db.close()


def save_entity_to_db(entity, db_session: Session):
    """ " Save new data or update existing data in the database table

    :param db_session: database session
    :param entity: database entity
    :type entity: database entity
    """
    try:
        db_session.add(entity)
        db_session.commit()
        db_session.refresh(entity)
        return entity

    except SQLAlchemyError as ex:
        raise CustomDatabaseException(ex=ex)

    except Exception as ex:
        raise CustomDatabaseException(ex=ex)


def remove_entity_from_db(entity, db_session: Session):
    """ " delete data from table

    :param db_session: database session
    :param entity: database entity
    :type entity: database entity
    """
    try:
        db_session.delete(entity)
        db_session.commit()

    except SQLAlchemyError as ex:
        raise CustomDatabaseException(ex=ex)

    except Exception as ex:
        raise CustomDatabaseException(ex=ex)
