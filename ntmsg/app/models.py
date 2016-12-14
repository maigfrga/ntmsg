from pgsqlutils.orm import BaseModel
from sqlalchemy import Column

from sqlalchemy.dialects.postgresql import JSON, UUID


class MessageQueue(BaseModel):
    __tablename__ = 'messages_queue'
    key = Column(UUID(as_uuid=True), nullable=False)
    msg = Column(JSON(), nullable=False)
