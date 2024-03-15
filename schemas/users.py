from uuid import UUID
from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    user_name: str
    name: str
    phone: str
    password: str
    bio: str
    image: str
    city: str
    state: str
    country: str


class CreateUserSchema(BaseUserSchema):
    pass


class UpdateUserSchema(BaseUserSchema):
    user_name: str | None=None
    name: str | None=None
    phone: str | None=None
    password: str | None=None
    bio: str | None=None
    image: str | None=None
    city: str | None=None
    state: str | None=None
    country: str | None=None


class GetUserSchema(BaseUserSchema):
    id: UUID


    class Config:
        from_attributes = True