import uuid
from sqlalchemy import Column, UUID, Text
from base import TimeStamp

class Comment(TimeStamp):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)

    def __str__(self):
        return f"{self.content}"