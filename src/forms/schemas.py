from pydantic import BaseModel
from typing import List, Optional
from src.users.schemas import User

class Option(BaseModel):
    id: int
    text: str

class Question(BaseModel):
    text: str
    type: str
    allow_multiple: bool
    options: Optional[List[Option]] = []

class Form(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner: User
    questions: List[Question]
