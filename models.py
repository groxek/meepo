from sqlalchemy import Column, Integer, String
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    difficulty = Column(String)
    color = Column(String)
    dot_color = Column(String)