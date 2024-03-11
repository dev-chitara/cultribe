import uuid
from sqlalchemy import Column, String, UUID, Text, ForeignKey
from sqlalchemy.orm import Relationship
from models.base import TimeStamp
from relationships import post_likes


class Post(TimeStamp):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(80), nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String(80), nullable=False)
    owner_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(UUID, ForeignKey("groups.id", ondelete="CASCADE"))

    comments = Relationship("Comment", backref="post")

    likes = Relationship("User", secondary=post_likes, backref="related_likes")

    def __str__(self):
        return f"{self.title}"