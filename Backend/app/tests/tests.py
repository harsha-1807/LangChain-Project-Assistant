from fastapi.testclient import TestClient
from app.main import app  

client = TestClient(app)

def test_get_pending_tasks():
    response = client.get("/api/tasks/pending")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_check_project_status():
    response = client.get("/api/projects/Project Alpha/status")
    assert response.status_code == 200
    data = response.json()
    assert "project" in data
    assert "delayed" in data

def test_top_assignee():
    response = client.get("/api/users/top-assignee")
    assert response.status_code == 200
    data = response.json()
    assert "top_assignee" in data
    assert "task_count" in data
