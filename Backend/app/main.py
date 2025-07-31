from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import api
from .models import User, Project, Task
from .db import Base, engine, get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables in the database if they don't exist
    Base.metadata.create_all(bind=engine)

  
    db: Session = next(get_db())

    # Insert mock data only if users table is empty
    if not db.query(User).first():
        create_mock_data(db)

   
    yield  

   
    db.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://lang-chain-project-assistant.vercel.app",],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(api.router, prefix="/api", tags=["API"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


def create_mock_data(db: Session):
    # Users
    alice = User(name="Alice", email="alice@example.com")
    bob = User(name="Bob", email="bob@example.com")

    now = datetime.now()

    # Projects
    project_alpha = Project(
        name="Project Alpha",
        status="active",
        percentage_completed=45.0,
        start_date=now - timedelta(days=30),
        end_date=now + timedelta(days=15),
        owner=alice
    )

    project_beta = Project(
        name="Project Beta",
        status="active",
        percentage_completed=90.0,
        start_date=now - timedelta(days=60),
        end_date=now - timedelta(days=5),
        owner=bob
    )

    # Tasks
    task1 = Task(
        name="Design UI",
        status="open",
        percentage_completed=20.0,
        start_date=now - timedelta(days=20),
        end_date=now + timedelta(days=10),
        project=project_alpha,
        owner=alice
    )

    task2 = Task(
        name="Develop API",
        status="closed",
        percentage_completed=100.0,
        start_date=now - timedelta(days=25),
        end_date=now - timedelta(days=1),
        project=project_alpha,
        owner=bob
    )

    task3 = Task(
        name="Testing",
        status="open",
        percentage_completed=50.0,
        start_date=now - timedelta(days=10),
        end_date=now + timedelta(days=5),
        project=project_beta,
        owner=bob
    )

    db.add_all([alice, bob, project_alpha, project_beta, task1, task2, task3])
    db.commit()
