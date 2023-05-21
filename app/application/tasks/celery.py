from celery import Celery

from app.domain.shared.config.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://redis:6379/0",
    include=["app.application.tasks.tasks"]
)