from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends

from models.users import User
from schemas.users import UpdateUserSchema, GetUserSchema
from common.auth import Auth
from db_setup import get_db


router = APIRouter(tags=["User API"])


auth = Auth()


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[GetUserSchema])
async def fetch_users(db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    user_objects = db.query(User).all()
    return user_objects


@router.get("/users/me", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
async def get_user(user_id: str, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    uid = user_id if user_id != "me" else user_object.id
    user_object = db.query(User).filter(User.id == uid).first()

    if user_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "User not found!"}
        )
    
    return user_object


@router.patch("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
async def update_user(user_id: UUID, user_data: UpdateUserSchema, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    if user_id != user_object.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not authenticated"}
        )
    
    update_user_data = user_data.model_dump(exclude_none=True)

    user_query = db.query(User).filter(User.id == user_id)
    user_object = user_query.first()

    if user_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "User not found!"}
        )
    
    user_query.update(update_user_data)
    db.commit()
    db.refresh(user_object)
    return user_object


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: UUID, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    if user_id != user_object.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not authenticated"}
        )
    
    user_object = db.query(User).filter(User.id == user_id).first()

    if user_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "User not found!"}
        )
    
    db.delete(user_object)
    db.commit()
    return {"Deleted": True}