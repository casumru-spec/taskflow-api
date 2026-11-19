from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.logging_config import setup_logging
from app.routers import comments, labels, projects, tasks, users

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TaskFlow API starting up (log_level=%s)", settings.log_level)
    logger.debug("Database URL configured for startup check")
    yield
    logger.info("TaskFlow API shutting down")


app = FastAPI(title="TaskFlow API", version="1.0.0", lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug("Incoming request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    if response.status_code >= 500:
        logger.error(
            "Server error %s on %s %s",
            response.status_code,
            request.method,
            request.url.path,
        )
    elif response.status_code >= 400:
        logger.warning(
            "Client error %s on %s %s",
            response.status_code,
            request.method,
            request.url.path,
        )
    else:
        logger.info(
            "Completed %s %s -> %s",
            request.method,
            request.url.path,
            response.status_code,
        )
    return response


@app.exception_handler(IntegrityError)
def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.warning("Database integrity conflict on %s: %s", request.url.path, exc.orig)
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Database integrity conflict: duplicate unique value or foreign key constraint violation."
        },
    )


@app.get("/health", tags=["health"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        logger.debug("Health check database ping succeeded")
        return {"status": "ok"}
    except Exception as exc:
        logger.critical("CRITICAL: Database connection failed during health check: %s", exc)
        raise HTTPException(status_code=503, detail="Database unavailable") from exc


app.include_router(users.router)
app.include_router(projects.router)
app.include_router(labels.router)
app.include_router(tasks.router)
app.include_router(comments.router)
