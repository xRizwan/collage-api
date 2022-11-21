from celery import Celery
from fastapi import UploadFile
from time import sleep
from api.helpers import merge_images, save_images, OrientationType
from typing import List

# class CeleryConfig:
#     broker="amqp://guest:guest@localhost:5672/"
#     backend="rpc://"

#     task_serializer = 'json'
#     result_serializer = 'json'
#     accept_content = ['json']
#     enable_utc = True

celery_app = Celery('collage_api_tasks', backend="rpc://", broker='amqp://guest@localhost//', accept_content = ['json', 'pickle'], result_accept_content = ['json', 'pickle'])
celery_app.set_default()
celery_app.autodiscover_tasks(["api"])

@celery_app.task(name="add")
def add(x, y):
    sleep(60)
    return x + y

@celery_app.task(name="generate_image")
def generate_image(images: List[UploadFile], orientation: OrientationType):
    saved_images_path = save_images(images)
    generated_image_namge = merge_images(saved_images_path, orientation)
    return generated_image_namge


# celery_app.config_from_object(CeleryConfig)


# python -m flower --app=tasks.celery_app worker -E
# celery -A api.celery.worker.celery_app worker --loglevel=info -P eventlet