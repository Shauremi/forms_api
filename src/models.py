from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.database import Base as DeclarativeBase
from src.exceptions import HTTP400Exception

class Base(DeclarativeBase):

    __abstract__ = True

    def save(self, db_session: Session) -> None:
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError as error:
            db_session.rollback()
            raise HTTP400Exception(detail=repr(error))

    def delete(self, db_session: Session) -> None:
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError as error:
            db_session.rollback()
            raise HTTP400Exception(detail=repr(error))

    def update(self, db_session: Session, **kwargs) -> None:
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            db_session.commit()
        except SQLAlchemyError as error:
            db_session.rollback()
            raise HTTP400Exception(detail=repr(error))