from sqlalchemy import select
from sqlalchemy.orm import Session

from src.repository.base import Repository
from src.users.schemas import User, UserBase
from src.users.models import UserModel


class DatabaseRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def read(self, user_id: int):
        user = self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        ).scalar_one_or_none()
        return user

    def add(self, user: UserBase):
        db_user = UserModel(fullname=user.fullname)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete(self, _id: int):
        db_user = self.read(_id)
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
        return db_user

    def update(self, _id: int, user: UserBase):
        result = self.session.execute(select(UserModel).where(UserModel.id == _id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)

        self.session.commit()
        self.session.refresh(db_user)
        return User.model_validate(db_user)

    def list_users(self):
        result = self.session.execute(select(UserModel))
        return [User.model_validate(obj) for obj in result.scalars().all()]
