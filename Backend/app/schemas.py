# User Schemas
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    projects: Optional[List["ProjectOut"]] = []
    tasks: Optional[List["TaskOut"]] = []

    class Config:
        orm_mode = True



#Project Schemas
class ProjectBase(BaseModel):
    name: str
    status: Optional[str] = "active"
    percentage_completed: Optional[float] = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    owner: Optional[UserOut] = None
    tasks: Optional[List["TaskOut"]] = []

    class Config:
        orm_mode = True



# Task schemas

class TaskBase(BaseModel):
    name: str
    status: Optional[str] = "open"
    percentage_completed: Optional[float] = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_id: int
    owner_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    owner: Optional[UserOut] = None
    project: Optional[ProjectOut] = None

    class Config:
        orm_mode = True


ProjectOut.model_rebuild()
UserOut.model_rebuild()
TaskOut.model_rebuild()