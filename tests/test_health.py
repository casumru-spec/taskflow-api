from fastapi.testclient import TestClient

from app.main import app


def test_health_and_crud_flow():
    with TestClient(app) as client:
        # 1. Проверка /health
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json() == {"status": "ok"}

        # 2. Проверка POST -> 201
        proj = client.post(
            "/v1/projects",
            json={"name": "CI Test Project", "description": "Created in pytest"},
        )
        assert proj.status_code == 201
        project_id = proj.json()["id"]
        assert proj.json()["name"] == "CI Test Project"

        # 3. Проверка GET несуществующего объекта -> 404
        missing = client.get("/v1/projects/999999")
        assert missing.status_code == 404

        # 4. Проверка неверного ввода -> 422
        invalid = client.post("/v1/projects", json={"unknown_field": 123})
        assert invalid.status_code == 422

        # Очистка тестового проекта
        deleted = client.delete(f"/v1/projects/{project_id}")
        assert deleted.status_code == 204
