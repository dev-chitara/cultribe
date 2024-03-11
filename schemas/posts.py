from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BasePostSchema(BaseModel):
    title: str
    content: str
    image: str
    owner_id: UUID
    group_id: UUID


class CreatePostSchema(BasePostSchema):
    pass 


class UpdatePostSchema(BasePostSchema):
    title: str | None=None
    content: str | None=None
    image: str | None=None
    owner_id: UUID
    group_id: UUID


class GetPostSchema(BasePostSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None=None


    class Config:
        from_attributes = True