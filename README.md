# TaskFlow API

REST API для управления задачами команды на базе FastAPI, PostgreSQL 16, SQLAlchemy 2, Alembic и Docker Compose.

## Запуск проекта

1. Скопируйте шаблон переменных окружения:
   ```bash
   cp .env.example .env
   ```

2. Запустите сборку и контейнеры:
   ```bash
   docker compose up --build -d
   ```

3. Проверьте состояние сервиса и откройте документацию:
   - Проверка здоровья: `http://localhost:8000/health`
   - Swagger UI: `http://localhost:8000/docs`

## Проверка миграций

```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic downgrade base
docker compose exec api alembic upgrade head
```

## Примеры запросов

### 1. Создание пользователя
```bash
curl -X POST http://localhost:8000/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "display_name": "Alice",
    "role": "admin"
  }'
```

### 2. Создание проекта
```bash
curl -X POST http://localhost:8000/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend API",
    "description": "Разработка сервиса TaskFlow"
  }'
```

### 3. Создание задачи и фильтрация
```bash
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "assignee_id": 1,
    "title": "Настроить миграции Alembic",
    "status": "open",
    "priority": "high"
  }'

curl "http://localhost:8000/v1/tasks?project_id=1&status=open"
```
