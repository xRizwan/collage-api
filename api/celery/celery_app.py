from celery import Celery
from time import sleep

# class CeleryConfig:
#     broker="amqp://guest:guest@localhost:5672/"
#     backend="rpc://"

#     task_serializer = 'json'
#     result_serializer = 'json'
#     accept_content = ['json']
#     enable_utc = True

celery_app = Celery('super', backend="rpc://", broker='amqp://guest@localhost//',)
celery_app.autodiscover_tasks(["api"])
celery_app.set_default()

# celery_app.config_from_object(CeleryConfig)


# celery -A api.celery.celery_app.celery_app worker --loglevel=info -P eventlet