from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import User, Project, Task
from app.db import get_db

router = APIRouter()

@router.get("/tasks/pending")
def get_pending_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.status == "open").all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "status": t.status,
            "percentage_completed": t.percentage_completed,
            "project": t.project.name,
            "owner": t.owner.name if t.owner else None,
        }
        for t in tasks
    ]

@router.get("/projects/{project_name}/status")
def check_project_status(project_name: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.name == project_name).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    now = datetime.now()
    delayed = False
    if project.end_date and project.end_date < now and project.percentage_completed < 100.0:
        delayed = True

    return {
        "project": project.name,
        "delayed": delayed,
        "status" : project.status,
        "percentage_completed": project.percentage_completed,
        "end_date": project.end_date,
    }

@router.get("/users/top-assignee")
def top_assignee(db: Session = Depends(get_db)):
    result = (
        db.query(
            User.name,
            func.count(Task.id).label("task_count")
        )
        .join(Task, Task.owner_id == User.id)
        .group_by(User.id)
        .order_by(func.count(Task.id).desc())
        .first()
    )
    if not result:
        return {"message": "No users or tasks found"}

    name, task_count = result
    return {"top_assignee": name, "task_count": task_count}
