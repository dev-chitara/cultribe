from typing import List
from uuid import UUID
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from models.comments import Comment
from schemas.comments import CreateCommentSchema, UpdateCommentSchema, GetCommentSchema
from db_setup import get_db


router = APIRouter(tags=["Comment API"])


@router.get("/comments", status_code=status.HTTP_200_OK)
async def fetch_commments(db: Session=Depends(get_db)):
    comment_object = db.query(Comment).all()
    return comment_object


@router.post("/comments", status_code=status.HTTP_201_CREATED, response_model=GetCommentSchema)
async def create_comment(comment_data: CreateCommentSchema, db: Session=Depends(get_db)):
    comment_object = Comment(**comment_data.model_dump())
    db.add(comment_object)
    db.commit()
    db.refresh(comment_object)
    return comment_object


@router.get("/comments/{comment_id}", status_code=status.HTTP_200_OK, response_model=GetCommentSchema)
async def get_comment(comment_id: UUID, db: Session=Depends(get_db)):
    comment_object = db.query(Comment).filter(Comment.id == comment_id).first()

    if comment_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Comment not found!"})
    
    return comment_object


@router.patch("/comments/{comment_id}", status_code=status.HTTP_200_OK, response_model=GetCommentSchema)
async def update_comment(comment_id: UUID, comment_data: UpdateCommentSchema, db: Session=Depends(get_db)):
    upadte_comment_data = comment_data.model_dump(exclude_none=True)

    comment_query = db.query(Comment).filter(Comment.id == comment_id)
    comment_object = comment_query.first()

    if comment_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Comment not found!"})
    
    comment_query.update(upadte_comment_data)
    db.commit()
    db.refresh(comment_object)
    return comment_object


@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: UUID, db: Session=Depends(get_db)):
    comment_object = db.query(Comment).filter(Comment.id == comment_id).first()

    if comment_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Comment not found!"})
    
    db.delete(comment_object)
    db.commit()
    return {"Deleted": True}