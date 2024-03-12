from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BaseCommentSchema(BaseModel):
    content: str
    owner_id: UUID | None=None
    post_id: UUID | None=None


class CreateCommentSchema(BaseCommentSchema):
    pass


class UpdateCommentSchema(BaseCommentSchema):
    content: str | None=None
    owner_id: UUID | None=None
    group_id: UUID | None=None


class GetCommentSchema(BaseCommentSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None=None


    class Config:
        from_attributes = True