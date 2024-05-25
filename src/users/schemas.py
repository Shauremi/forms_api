from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: str

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True