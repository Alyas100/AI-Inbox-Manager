from celery import Celery

# initialize celery 
# use celery as both broker (task queue) and backend (cahce email)
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# discover the task on that file
celery.autodiscover_tasks(['app.tasks'])
