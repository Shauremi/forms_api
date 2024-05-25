from typing import Optional, Sequence

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, insert, select
from sqlalchemy.orm import Session, relationship

from src.database import Base

class FormModel(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("UserModel", back_populates="forms")
    questions = relationship("QuestionModel", back_populates="form")

    @classmethod
    def list(cls, db_session: Session) -> Sequence["FormModel"]:
        stmt = select(cls)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    def get(cls, db_session: Session, id: int) -> Optional["FormModel"]:
        stmt = select(FormModel).where(FormModel.id == id)
        result = db_session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, db_session: Session, task: dict) -> "FormModel":
        created_task = FormModel(**task)
        db_session.add(created_task)
        db_session.commit()
        db_session.refresh(created_task)
        return created_task

class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    type = Column(String)  # text, radio, checkbox
    allow_multiple = Column(Boolean, default=False)
    form_id = Column(Integer, ForeignKey("forms.id"))


    form = relationship("FormModel", back_populates="questions")
    options = relationship("OptionModel", back_populates="question")

    @classmethod
    async def list(cls, db_session: Session) -> Sequence["QuestionModel"]:
        stmt = select(cls)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get(cls, db_session: Session, id: int) -> Optional["QuestionModel"]:
        stmt = select(FormModel).where(FormModel.id == id)
        result = db_session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, db_session: Session, task: dict) -> "QuestionModel":
        created_task = FormModel(**task)
        db_session.add(created_task)
        db_session.commit()
        db_session.refresh(created_task)
        return created_task

class OptionModel(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(String)

    question = relationship("QuestionModel", back_populates="options")

    @classmethod
    def list(cls, db_session: Session) -> Sequence["OptionModel"]:
        stmt = select(cls)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    def get(cls, db_session: Session, id: int) -> Optional["OptionModel"]:
        stmt = select(FormModel).where(FormModel.id == id)
        result = db_session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    def create(cls, db_session: Session, task: dict) -> "OptionModel":
        created_task = FormModel(**task)
        db_session.add(created_task)
        db_session.commit()
        db_session.refresh(created_task)
        return created_task