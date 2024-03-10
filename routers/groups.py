import uuid
from sqlalchemy import Column, String, UUID, Text, ForeignKey
from base import TimeStamp


class Group(TimeStamp):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(40), nullable=False)
    description = Column(Text, nullable=False)
    

# 1. Name
# 2. Description
# 3. Created At
# 4. Updated At
# 5. Owner (OneToMany with User)
# 6. Members (ManyToMany With User)
# 7. Mods (ManyToMany With User)