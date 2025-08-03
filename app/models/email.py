from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class EmailMessage(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message_id = Column(String, unique=True)
    subject = Column(String)
    sender = Column(String)
    body = Column(Text)
    user_email = Column(String, index=True)

    user = relationship("User", back_populates="emails")
