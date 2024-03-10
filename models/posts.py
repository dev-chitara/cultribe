import uuid
from sqlalchemy import Column, String, UUID, Text, ForeignKey
from base import TimeStamp


class Post(TimeStamp):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(80), nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String(80), nullable=False)

    def __str__(self):
        return f"{self.title}"