from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    attempts = relationship("Attempt", back_populates="user")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="subject")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    question = Column(String)
    answer = Column(String)
    images = Column(JSON, default=list)
    ege_number = Column(Integer)

    subject = relationship("Subject", back_populates="tasks")
    attempts = relationship("Attempt", back_populates="task")

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_input = Column(String)
    is_correct = Column(Boolean)

    user = relationship("User", back_populates="attempts")
    task = relationship("Task", back_populates="attempts")