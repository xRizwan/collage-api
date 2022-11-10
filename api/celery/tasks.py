from api.celery.celery_app import celery_app
from time import sleep

@celery_app.task(name="add")
def add(x, y):
    sleep(60)
    return x + y

# from celery.result import AsyncResult
# res = AsyncResult("your-task-id")
# res.ready()


# python.exe -m celery --app=tasks:celery_app worker -E 
# python -m flower --app=tasks.celery_app worker -E
# celery -A api.celery.celery_app.current_app worker --loglevel=info -P eventlet