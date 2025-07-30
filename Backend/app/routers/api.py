from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import User, Project, Task
from app.db import get_db
from langchain.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI

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




def fetch_projects(db):
    """Fetch all projects from the database."""
    return db.query(Project).all()


def fetch_tasks(db):
    """Fetch all tasks from the database."""
    return db.query(Task).all()


def fetch_users(db):
    """Fetch all users from the database."""
    return db.query(User).all()


def format_projects(projects):
    """Format a list of Project objects to a readable string consistent with schema."""
    if not projects:
        return "No projects found."
    lines = []
    for p in projects:
        end_date = p.end_date.strftime("%Y-%m-%d") if p.end_date else "N/A"
        status = getattr(p, "status", "Unknown")
        completed = getattr(p, "percentage_completed", "N/A")
        owner_name = p.owner.name if p.owner else "No owner"
        lines.append(
            f"- {p.name}: {completed}% complete, ends {end_date}, status {status}, owner {owner_name}"
        )
    return "\n".join(lines)


def format_tasks(tasks):
    """Format a list of Task objects to a readable string consistent with schema."""
    if not tasks:
        return "No tasks found."
    lines = []
    for t in tasks:
        status = getattr(t, "status", "Unknown")
        owner_name = t.owner.name if t.owner else "Unassigned"
        project_name = t.project.name if t.project else "No project"
        lines.append(
            f"- {t.name}: {status}, assigned to {owner_name}, project {project_name}"
        )
    return "\n".join(lines)


def format_users(users):
    """Format a list of User objects to a readable string consistent with schema."""
    if not users:
        return "No users found."
    lines = [f"- {u.name} ({u.email if u.email else 'No email'})" for u in users]
    return "\n".join(lines)

# Initializing Gemini client wrapped by LangChain
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

@router.post("/chat")
async def chat_with_context(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    user_message = body.get("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

        
    projects = fetch_projects(db)
    tasks = fetch_tasks(db)
    users = fetch_users(db)

    projects_str = format_projects(projects)
    tasks_str = format_tasks(tasks)
    users_str = format_users(users)

   
    data_summary = (
        f"Projects:\n{projects_str}\n\n"
        f"Tasks:\n{tasks_str}\n\n"
        f"Users:\n{users_str}"
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"You are a helpful assistant. Use this project data to answer:\n{data_summary} \n answer in normal english "),
        ("human", "{input}"),
    ])

    messages = prompt_template.format_messages(input=user_message)

    response = response = llm.invoke(messages)  

    return {"response": response.content}