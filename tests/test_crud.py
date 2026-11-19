from fastapi.testclient import TestClient

from app.main import app


def test_full_crud_lifecycle():
    with TestClient(app) as client:
        # 1. Users: POST -> 201, дубликат email -> 409, PATCH -> 200
        u_res = client.post(
            "/v1/users",
            json={
                "email": "pytest_user@example.com",
                "display_name": "Pytest User",
                "role": "operator",
            },
        )
        assert u_res.status_code == 201
        user_id = u_res.json()["id"]

        dup_res = client.post(
            "/v1/users",
            json={"email": "pytest_user@example.com", "display_name": "Duplicate"},
        )
        assert dup_res.status_code == 409

        upd_u = client.patch(f"/v1/users/{user_id}", json={"display_name": "Updated User"})
        assert upd_u.status_code == 200
        assert upd_u.json()["display_name"] == "Updated User"

        # 2. Projects: POST -> 201, GET -> 200
        p_res = client.post("/v1/projects", json={"name": "CRUD Project", "description": "Test"})
        assert p_res.status_code == 201
        project_id = p_res.json()["id"]

        get_p = client.get(f"/v1/projects/{project_id}")
        assert get_p.status_code == 200

        # 3. Labels: POST -> 201
        l_res = client.post("/v1/labels", json={"name": "pytest-label", "color": "#10b981"})
        assert l_res.status_code == 201
        label_id = l_res.json()["id"]

        # 4. Tasks: POST -> 201, фильтр по project_id и status -> 200, PATCH -> 200
        t_res = client.post(
            "/v1/tasks",
            json={
                "project_id": project_id,
                "assignee_id": user_id,
                "label_id": label_id,
                "title": "CRUD Task",
                "status": "open",
                "priority": "high",
            },
        )
        assert t_res.status_code == 201
        task_id = t_res.json()["id"]

        list_t = client.get(f"/v1/tasks?project_id={project_id}&status=open")
        assert list_t.status_code == 200
        assert any(t["id"] == task_id for t in list_t.json())

        upd_t = client.patch(f"/v1/tasks/{task_id}", json={"status": "done"})
        assert upd_t.status_code == 200
        assert upd_t.json()["status"] == "done"

        # 5. Comments: POST -> 201, пустой текст -> 422, DELETE -> 204
        c_res = client.post(
            "/v1/comments",
            json={"task_id": task_id, "author_id": user_id, "body": "Test comment"},
        )
        assert c_res.status_code == 201
        comment_id = c_res.json()["id"]

        bad_c = client.post(
            "/v1/comments",
            json={"task_id": task_id, "author_id": user_id, "body": "   "},
        )
        assert bad_c.status_code == 422

        # Очистка созданных данных (DELETE -> 204, повторный GET -> 404)
        assert client.delete(f"/v1/comments/{comment_id}").status_code == 204
        assert client.get(f"/v1/comments/{comment_id}").status_code == 404
        assert client.delete(f"/v1/tasks/{task_id}").status_code == 204
        assert client.delete(f"/v1/labels/{label_id}").status_code == 204
        assert client.delete(f"/v1/projects/{project_id}").status_code == 204
        assert client.delete(f"/v1/users/{user_id}").status_code == 204
