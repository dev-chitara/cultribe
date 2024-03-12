from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BaseGroupSchema(BaseModel):
    name: str
    description: str
    owner_id: UUID


class CreateGroupSchema(BaseGroupSchema):
    pass


class UpdateGroupSchema(BaseGroupSchema):
    name: str | None=None
    description: str | None=None
    owner_id: UUID | None=None


class GetGroupSchema(BaseGroupSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None


    class Config:
        from_attributes = True