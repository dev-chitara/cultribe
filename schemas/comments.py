from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BaseCommentSchema(BaseModel):
    content: str


class CreateCommentSchema(BaseCommentSchema):
    pass


class UpdateCommentSchema(BaseCommentSchema):
    content: str | None=None


class GetCommentSchema(BaseCommentSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True