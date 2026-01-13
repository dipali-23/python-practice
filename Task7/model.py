from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# class ProjectManager(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     email: str = Field(unique=True)
#     projects: List["Project"] = Relationship(back_populates="manager")

class ProjectResource(SQLModel, table=True):
    record_id:Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.project_id" )
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.resource_id")
    onboard:datetime
    offboard:Optional[datetime]=None

class Project(SQLModel, table=True):
    project_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    status: str = Field(default="ongoing")
    deadline: Optional[datetime] = None
    startdate:datetime
    enddate:Optional[datetime]=None
    project_manager_id: Optional[int] = Field(default=None, foreign_key="resource.resource_id")
    # manager: Optional[ProjectManager] = Relationship(back_populates="projects")
    resources: List["Resource"] = Relationship(back_populates="projects", link_model=ProjectResource)

class Resource(SQLModel, table=True):
    resource_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str
    status: str = Field(default="working")
    email:str= Field(unique=True)
    isActive:bool=Field(default=True)
    projects: List[Project] = Relationship(back_populates="resources", link_model=ProjectResource)
