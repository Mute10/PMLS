from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_complete: Optional[bool] = False 


class ProjectCreate(ProjectBase):
    pass
    #__pydantic_fields_set__

class Project(ProjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)