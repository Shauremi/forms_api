from typing import List, Optional
from src.repository.base import Repository
from src.users.schemas import User, UserBase


class InMemoryRepository(Repository):
    def __init__(self):
        self._users: List[User] = []
        self._id_counter = 0

    def read(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def add(self, user: UserBase):
        new_user = User(id=self._id_counter, **user.model_dump())
        self._users.append(new_user)
        self._id_counter += 1
        return new_user

    def delete(self, _id: int):
        db_user = self.read(_id)
        if db_user:
            self._users.remove(db_user)
            return True
        return False

    def update(self, _id: int, user: User):
        db_user = self.read(_id)
        if db_user:
            if user.fullname is not None:
                db_user.fullname = user.fullname
        return db_user

    def list_users(self):
        return self._users
