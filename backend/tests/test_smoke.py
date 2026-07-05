from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_liveness() -> None:
    """Verify that the application serves liveness checks successfully."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "live", "message": "I'm alive."}
