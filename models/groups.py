import uuid
from sqlalchemy import Column, String, UUID, Text, ForeignKey
from sqlalchemy.orm import Relationship
from base import TimeStamp
from relationships import member_users, mod_users


class Group(TimeStamp):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(40), nullable=False)
    description = Column(Text, nullable=False)
    owner_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"))

    posts = Relationship("Post", backref="group")
    
    members = Relationship("User", secondary=member_users, backref="related_users")
    mods = Relationship("User", secondary=mod_users, backref="related_mods")

    def __str__(self):
        return f"{self.name}"