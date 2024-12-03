from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)  # Optional for DMs
    created_at = Column(DateTime, default=datetime.utcnow)
    is_group = Column(Integer, default=0)  # 0 for DMs, 1 for Group Chats

    def __repr__(self):
        return f"<Conversation(id={self.id}, is_group={self.is_group})>"
