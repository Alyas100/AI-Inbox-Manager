from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class EmailMessage(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))   # link to user
    sender = Column(String)
    subject = Column(String)
    body = Column(String)
    date_received = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emails")
