from sqlalchemy import Column, Integer, String
from src.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
