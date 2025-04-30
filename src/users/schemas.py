from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    fullname: str
     
    model_config = ConfigDict(from_attributes=True)
    
class User(UserBase):
    id: int
