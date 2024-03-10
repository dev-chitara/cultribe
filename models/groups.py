import uuid
from sqlalchemy import Column, String, UUID, Text, ForeignKey
from base import TimeStamp


class Group(TimeStamp):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(40), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return f"{self.name}"