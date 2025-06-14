from celery import Celery

celery_app = Celery(
    "sales_trainer",
    broker="redis://localhost:6379/0",   # update if using remote Redis
    backend="redis://localhost:6379/1",
)
celery_app.conf.task_default_queue = "scoring"
