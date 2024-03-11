import uuid
from sqlalchemy import Column, UUID, Text, ForeignKey
from models.base import TimeStamp

class Comment(TimeStamp):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    owner_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(UUID, ForeignKey("posts.id", ondelete="CASCADE"))

    def __str__(self):
        return f"{self.content}"