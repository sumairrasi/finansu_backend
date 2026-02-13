
from celery import Celery
import os

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    "amqp://guest:guest@rabbitmq:5672//"
)


CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    "redis://redis:6379/0"
)

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

#  FIX: point to tasks module
celery_app.autodiscover_tasks([
    "app.background.task"
])
