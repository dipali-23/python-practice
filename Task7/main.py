from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from model import Project,Resource,ProjectResource
from datetime import datetime
app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
# Create a project and auto-assign manager
@app.post("/projects/")
def create_project(project: Project, session: Session = Depends(get_session)):
    # Check if the project manager exists
    manager = session.exec(select(Resource).where(Resource.resource_id == project.project_manager_id)).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Project manager does not exist")

    # Create the project
    session.add(project)
    session.commit()
    session.refresh(project)

    # Auto-create entry in ProjectResource table for the manager
    project_resource = ProjectResource(
        project_id=project.project_id,
        resource_id=project.project_manager_id,
        onboard=project.startdate
    )
    session.add(project_resource)
    session.commit()
    # sessiion
    return project

# Get all projects
@app.get("/projects/")
def get_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()

# Create a resource
@app.post("/resources/")
def create_resource(resource: Resource, session: Session = Depends(get_session)):
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource

# Get all resources
@app.get("/resources/")
def get_resources(session: Session = Depends(get_session)):
    return session.exec(select(Resource)).all()

# Assign a resource to a project
@app.post("/project-resource/")
def assign_resource(project_resource: ProjectResource, session: Session = Depends(get_session)):
    # Check if resource exists
    resource = session.exec(select(Resource).where(Resource.resource_id == project_resource.resource_id)).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Assign resource to project
    session.add(project_resource)
    session.commit()
    session.refresh(project_resource)
    return project_resource


@app.put("/projects/{project_id}/status/")
def update_project_status(project_id: int, status: str, session: Session = Depends(get_session)):
    project = session.exec(select(Project).where(Project.project_id == project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = status

    if status == "completed":
        project.enddate = datetime.utcnow()  # Set end date when project is completed

    session.commit()

    if status in ["completed", "onhold"]:
        # Offboard all resources from this project
        resources = session.exec(select(ProjectResource).where(ProjectResource.project_id == project_id)).all()
        for res in resources:
            res.offboard = datetime.utcnow()
            session.add(res)

        session.commit()
        update_bench_resources(session)

    return {"message": f"Project status updated to {status}"}

# If a resource is offboarded from all projects, mark as "bench"
def update_bench_resources(session: Session):
    resources = session.exec(select(Resource)).all()
    for resource in resources:
        active_projects = session.exec(
            select(ProjectResource).where(ProjectResource.resource_id == resource.resource_id, ProjectResource.offboard == None)
        ).all()

        if not active_projects:  # If no active projects
            resource.status = "bench"
            session.add(resource)

    session.commit()

# Get bench resources
@app.get("/resources/bench/")
def get_bench_resources(session: Session = Depends(get_session)):
    return session.exec(select(Resource).where(Resource.status == "bench")).all()


@app.put("/project-resource/{record_id}/offboard/")
def offboard_resource(record_id: int, session: Session = Depends(get_session)):
    project_resource = session.exec(select(ProjectResource).where(ProjectResource.record_id == record_id)).first()
    if not project_resource:
        raise HTTPException(status_code=404, detail="Project resource entry not found")

    project_resource.offboard = datetime.utcnow()
    session.commit()
    return {"message": "Resource offboarded successfully"}


@app.get("/projects/{project_id}/resources/")
def get_project_resources(project_id: int, session: Session = Depends(get_session)):
    resources = session.exec(
        select(Resource).join(ProjectResource).where(ProjectResource.project_id == project_id)
    ).all()

    if not resources:
        raise HTTPException(status_code=404, detail="No resources found for this project")

    return resources
