from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends
from models.posts import Post
from schemas.posts import CreatePostSchema, UpdatePostSchema, GetPostSchema
from common.auth import Auth
from db_setup import get_db


router = APIRouter(tags=["Post API"])

auth = Auth()


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[GetPostSchema])
async def fetch_posts(db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    post_objects = db.query(Post).filter(Post.owner_id == user_object.id).all()
    return post_objects


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=GetPostSchema)
async def create_posts(post_data: CreatePostSchema, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    if post_data.owner_id != user_object.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not authenticated"}
        )
    
    post_object = Post(**post_data.model_dump())
    db.add(post_object)
    db.commit()
    db.refresh(post_object)
    return post_object


@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=GetPostSchema)
async def get_post(post_id: UUID, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    post_object = db.query(Post).filter(Post.id == post_id).first()

    if post_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Post not found!"}
        ) 

    return post_object 


@router.patch("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=GetPostSchema)
async def update_post(post_id: UUID, post_data:UpdatePostSchema, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    update_post_data = post_data.model_dump(exclude_none=True)

    post_query = db.query(Post).filter(Post.id == post_id)
    post_object = post_query.first()

    if post_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Post not found!"}
        )
    
    post_query.update(update_post_data)
    db.commit()
    db.refresh(post_object)
    return post_object


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: UUID, db: Session=Depends(get_db), user_object: str = Depends(auth.get_current_user)):
    post_object = db.query(Post).filter(Post.id == post_id).first()

    if post_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Post not found!"}
        )

    db.delete(post_object)
    db.commit()
    return {"Deleted": True}
                      