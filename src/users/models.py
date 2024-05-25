from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)

    forms = relationship("FormModel", back_populates="owner")
