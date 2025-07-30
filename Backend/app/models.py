from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  
    email = Column(String, unique=True, index=True, nullable=True)  
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  
    status = Column(String, default="active", index=True)            
    percentage_completed = Column(Float, default=0.0)                
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="projects")

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)               
    status = Column(String, default="open", index=True)            
    percentage_completed = Column(Float, default=0.0)                 
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="tasks")
