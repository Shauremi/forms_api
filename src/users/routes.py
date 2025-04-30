from typing import List
from fastapi import APIRouter, Depends, HTTPException

from src.repository.base import Repository
from src.users.schemas import User, UserBase
from src.users.dependencies import get_user_repository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(user: UserBase, repo: Repository = Depends(get_user_repository)):
    return repo.add(user)


@router.get("/", response_model=List[User])
def list_users(repo: Repository = Depends(get_user_repository)):
    return [User.model_validate(obj) for obj in repo.list_users()]


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, repo: Repository = Depends(get_user_repository)):
    db_user = repo.read(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, repo: Repository = Depends(get_user_repository)):
    success = repo.delete(user_id) # 204
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.put("/{user_id}")
def partial_update_user(
    user_id: int, user: UserBase, repo: Repository = Depends(get_user_repository)
):
    updated = repo.update(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated # 201
