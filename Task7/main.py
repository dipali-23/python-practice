from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from model import Project, Resource, ProjectResource
from datetime import datetime

app = FastAPI()


# Initialize the database on startup
@app.on_event("startup")
def initialize_database():
    SQLModel.metadata.create_all(engine)


# Create a new project and assign a project manager
@app.post("/projects/")
def create_project(project: Project, session: Session = Depends(get_session)):
    # Validate if the project manager exists
    manager = session.exec(select(Resource).where(Resource.resource_id == project.project_manager_id)).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Project manager does not exist")

    # Add the new project to the database
    session.add(project)
    session.commit()
    session.refresh(project)

    # Assign the manager to the project in the ProjectResource table
    manager_assignment = ProjectResource(
        project_id=project.project_id,
        resource_id=project.project_manager_id,
        onboard=project.start_date
    )
    session.add(manager_assignment)
    session.commit()

    return project


# Retrieve all projects
@app.get("/projects/")
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()


# Create a new resource (employee)
@app.post("/resources/")
def create_resource(resource: Resource, session: Session = Depends(get_session)):
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


# Retrieve all resources
@app.get("/resources/")
def list_resources(session: Session = Depends(get_session)):
    return session.exec(select(Resource)).all()


# Assign a resource to a project
@app.post("/project-resource/")
def assign_resource_to_project(assignment: ProjectResource, session: Session = Depends(get_session)):
    # Validate if the resource exists
    resource = session.exec(select(Resource).where(Resource.resource_id == assignment.resource_id)).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Assign resource to project
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment


# Update project status and handle resource offboarding
@app.put("/projects/{project_id}/status/")
def update_project_status(project_id: int, status: str, session: Session = Depends(get_session)):
    project = session.exec(select(Project).where(Project.project_id == project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = status
    if status == "completed":
        project.end_date = datetime.utcnow()

    session.commit()

    if status in ["completed", "onhold"]:
        # Offboard all resources assigned to this project
        assigned_resources = session.exec(select(ProjectResource).where(ProjectResource.project_id == project_id)).all()
        for resource in assigned_resources:
            resource.offboard = datetime.utcnow()
            session.add(resource)

        session.commit()
        update_bench_resources(session)

    return {"message": f"Project status updated to {status}"}


# Mark resources as "bench" if they are not assigned to any active projects
def update_bench_resources(session: Session):
    all_resources = session.exec(select(Resource)).all()
    for resource in all_resources:
        active_projects = session.exec(
            select(ProjectResource).where(ProjectResource.resource_id == resource.resource_id,
                                          ProjectResource.offboard == None)
        ).all()

        if not active_projects:
            resource.status = "bench"
            session.add(resource)

    session.commit()


# Retrieve all resources currently on the bench
@app.get("/resources/bench/")
def list_bench_resources(session: Session = Depends(get_session)):
    return session.exec(select(Resource).where(Resource.status == "bench")).all()


# Offboard a resource from a project
@app.put("/project-resource/{record_id}/offboard/")
def offboard_resource(record_id: int, session: Session = Depends(get_session)):
    project_assignment = session.exec(select(ProjectResource).where(ProjectResource.record_id == record_id)).first()
    if not project_assignment:
        raise HTTPException(status_code=404, detail="Project resource entry not found")

    project_assignment.offboard = datetime.utcnow()
    session.commit()
    return {"message": "Resource offboarded successfully"}


# Retrieve all resources assigned to a specific project
@app.get("/projects/{project_id}/resources/")
def list_project_resources(project_id: int, session: Session = Depends(get_session)):
    assigned_resources = session.exec(
        select(Resource).join(ProjectResource).where(ProjectResource.project_id == project_id)
    ).all()

    if not assigned_resources:
        raise HTTPException(status_code=404, detail="No resources found for this project")

    return assigned_resources
