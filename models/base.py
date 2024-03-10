from datetime import datetime
from sqlalchemy import Column, DateTime
from db_setup import Base


class TimeStamp(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())