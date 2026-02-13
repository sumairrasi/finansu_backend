from app.background.worker import celery_app

@celery_app.task
def test_task():
    return "Celery working!"
