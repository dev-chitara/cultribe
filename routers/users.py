import uuid
from sqlalchemy import Column, String, UUID, Integer, Text
from db_setup import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    phone = Column(Integer(10), nullable=False)
    bio = Column(Text, nullable=False)
    image = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)

    def __str__(self):
        return f"{self.name}"