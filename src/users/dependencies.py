from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from src.repository.base import Repository
from src.repository.in_memory import InMemoryRepository
from src.repository.postgres import DatabaseRepository
from src.config import config
from src.database import get_db

@lru_cache(maxsize=1)
def get_in_memory_repository() -> InMemoryRepository:
    return InMemoryRepository()

def get_user_repository(db: Session = Depends(get_db)) -> Repository:
    if config.repository_type == "memory":
        return get_in_memory_repository()
    elif config.repository_type == "database":
        return DatabaseRepository(db)
    else:
        raise ValueError("Invalid repository type")
