from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import User, Project, Task
from app.db import get_db
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.chains import RetrievalQA


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




# def fetch_projects(db):
#     """Fetch all projects from the database."""
#     return db.query(Project).all()


# def fetch_tasks(db):
#     """Fetch all tasks from the database."""
#     return db.query(Task).all()


# def fetch_users(db):
#     """Fetch all users from the database."""
#     return db.query(User).all()


# def format_projects(projects):
#     """Format a list of Project objects to a readable string consistent with schema."""
#     if not projects:
#         return "No projects found."
#     lines = []
#     for p in projects:
#         end_date = p.end_date.strftime("%Y-%m-%d") if p.end_date else "N/A"
#         status = getattr(p, "status", "Unknown")
#         completed = getattr(p, "percentage_completed", "N/A")
#         owner_name = p.owner.name if p.owner else "No owner"
#         lines.append(
#             f"- {p.name}: {completed}% complete, ends {end_date}, status {status}, owner {owner_name}"
#         )
#     return "\n".join(lines)


# def format_tasks(tasks):
#     """Format a list of Task objects to a readable string consistent with schema."""
#     if not tasks:
#         return "No tasks found."
#     lines = []
#     for t in tasks:
#         status = getattr(t, "status", "Unknown")
#         owner_name = t.owner.name if t.owner else "Unassigned"
#         project_name = t.project.name if t.project else "No project"
#         lines.append(
#             f"- {t.name}: {status}, assigned to {owner_name}, project {project_name}"
#         )
#     return "\n".join(lines)


# def format_users(users):
#     """Format a list of User objects to a readable string consistent with schema."""
#     if not users:
#         return "No users found."
#     lines = [f"- {u.name} ({u.email if u.email else 'No email'})" for u in users]
#     return "\n".join(lines)

# APPROACH 1 -> directly feeding information to LLM

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# @router.post("/chat")
# async def chat_with_context(request: Request, db: Session = Depends(get_db)):
#     body = await request.json()
#     user_message = body.get("message", "").strip()
#     if not user_message:
#         raise HTTPException(status_code=400, detail="Message is required")

        
#     projects = fetch_projects(db)
#     tasks = fetch_tasks(db)
#     users = fetch_users(db)

#     projects_str = format_projects(projects)
#     tasks_str = format_tasks(tasks)
#     users_str = format_users(users)

   
#     data_summary = (
#         f"Projects:\n{projects_str}\n\n"
#         f"Tasks:\n{tasks_str}\n\n"
#         f"Users:\n{users_str}"
#     )
#     prompt_template = ChatPromptTemplate.from_messages([
#         ("system", f"You are a helpful assistant. Use this project data to answer:\n{data_summary} \n answer in english without any special character"),
#         ("human", "{input}"),
#     ])

#     messages = prompt_template.format_messages(input=user_message)

#     response = response = llm.invoke(messages)  

#     return {"response": response.content}


# APPROACH 2 -> using embeddings and vector store for retrieval

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def prepare_documents(db: Session) -> List[Document]:

    projects = db.query(Project).all()
    tasks = db.query(Task).all()
    users = db.query(User).all()

    documents = []

    for p in projects:
        owner_name = p.owner.name if p.owner else "No owner"
        end_date = p.end_date.strftime("%Y-%m-%d") if p.end_date else "N/A"
        text = (f"Project {p.name}, status: {p.status}, "
                f"{p.percentage_completed}% complete, owned by {owner_name}, ends on {end_date}.")
        documents.append(Document(page_content=text, metadata={"type": "project", "id": p.id}))

    for t in tasks:
        owner_name = t.owner.name if t.owner else "Unassigned"
        project_name = t.project.name if t.project else "No project"
        text = (f"Task {t.name}, status: {t.status}, assigned to {owner_name}, "
                f"part of project {project_name}.")
        documents.append(Document(page_content=text, metadata={"type": "task", "id": t.id}))

    for u in users:
        email = u.email if u.email else "No email"
        text = f"User {u.name}, email: {email}."
        documents.append(Document(page_content=text, metadata={"type": "user", "id": u.id}))

    return documents

_vector_store = None

def get_vector_store(db: Session) -> FAISS:
    global _vector_store
    if _vector_store is None:
        docs = prepare_documents(db)
        _vector_store = FAISS.from_documents(docs, embeddings)
    return _vector_store

def get_qa_chain(vector_store: FAISS):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

@router.post("/chat")
async def chat_endpoint(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    user_message = body.get("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    vector_store = get_vector_store(db)
    qa_chain = get_qa_chain(vector_store)

    modified_user_message = user_message + "provide the answer without any special characters except fullstop and format dates properly if present."

    answer = qa_chain.run(modified_user_message)

    return {"response": answer}
