from sqlalchemy import Column, Integer, String, Text
from .db import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    duration_minutes = Column(Integer)
    notes = Column(Text)
    summary = Column(Text, nullable=True)
