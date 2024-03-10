from sqlalchemy import Column, UUID, ForeignKey, Table
from db_setup import Base

member_users = Table(
    "member_users",
    Base.metadata,
    Column("group_id", UUID, ForeignKey("groups.id"), primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True)
)

mod_users = Table(
    "mod_users",
    Base.metadata,
    Column("group_id", UUID, ForeignKey("groups.id"), primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True)
)

post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("post_id", UUID, ForeignKey("posts.id"), primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True)
)