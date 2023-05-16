from celery import Celery
from app.infrastructure.database.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.application.tasks.tasks"]
)