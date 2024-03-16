from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends

from models.groups import Group
from models.users import User
from schemas.groups import CreateGroupSchema, UpdateGroupSchema, GetGroupSchema
from common.auth import Auth
from db_setup import get_db


router = APIRouter(tags=["Group API"])


auth = Auth()


@router.get("/groups", status_code=status.HTTP_200_OK, response_model=List[GetGroupSchema])
async def fetch_groups(db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    group_objects = db.query(Group).filter(Group.owner_id == user_object.id).all()
    return group_objects


@router.post("/groups", status_code=status.HTTP_201_CREATED, response_model=GetGroupSchema)
async def create_groups(group_data: CreateGroupSchema, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    if group_data.owner_id != user_object.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not authenticated"}
        )
    
    group_object = Group(**group_data.model_dump())
    db.add(group_object)
    db.commit()
    db.refresh(group_object)
    return group_object


@router.get("/groups/{group_id}", status_code=status.HTTP_200_OK, response_model=GetGroupSchema)
async def get_group(group_id: UUID, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    group_object = db.query(Group).filter(Group.id == group_id).first()

    if group_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Group not found!"}
        )
    
    return group_object


@router.patch("/groups/{group_id}", status_code=status.HTTP_200_OK, response_model=GetGroupSchema)
async def update_group(group_id: UUID, group_data: UpdateGroupSchema, user_id: UUID = None, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    if user_id is None:

        if group_data.owner_id != user_object.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Not authenticated"}
            )
        
        update_group_data = group_data.model_dump(exclude_none=True)

        group_query = db.query(Group).filter(Group.id == group_id)
        group_object = group_query.first()

        if group_object is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"message": "Group not found!"}
            )
        
        group_query.update(update_group_data)
        db.commit()
        db.refresh(group_object)
        return group_object

    else:
        group_object = db.query(Group).filter(Group.id == group_id).first()

        if group_object is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Group not found!"}
            )
        
        user = db.query(User).filter(User.id == user_object.id).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found!"}
            )

        group_object.members.append(user)
        db.commit()

        return {"message": f"User {user} joined group {group_object.name}"}        


@router.post("/groups/members/{group_id}", status_code=status.HTTP_200_OK)
async def assist_mods(group_id: UUID, user_id: UUID, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    group_object = db.query(Group).filter(Group.id == group_id).first()

    if group_object.owner_id != user_object.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not authenticated"}
        )
    
    if group_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Group not found!"}
        )
    
    
    user = db.query(User).filter(User.id == user_id).first()
    group_object.mods.append(user)
    db.commit()

    return {"message": f"User {user} is assisted as moderator in group {group_object.name}"}
    

@router.delete("/groups/{group_id}", status_code=status.HTTP_200_OK)
async def delete_group(group_id: UUID, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    group_object = db.query(Group).filter(Group.id == group_id).first()

    if group_object.owner_id != user_object.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not authenticated"}
        )

    if group_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Group not found!"}
        )
    
    db.delete(group_object)
    db.commit()
    return {"Deleted": True}