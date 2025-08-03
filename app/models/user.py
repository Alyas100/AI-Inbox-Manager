from sqlalchemy import Column, String, Integer
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.email import EmailMessage 



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)

    emails = relationship("EmailMessage", back_populates="user")

