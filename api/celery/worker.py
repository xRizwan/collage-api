from celery import Celery
from fastapi import UploadFile
from api.helpers import merge_images, save_images, OrientationType
from typing import List


celery_app = Celery('collage_api_tasks', backend="rpc://", broker='amqp://guest@localhost//', accept_content = ['json', 'pickle'], result_accept_content = ['json', 'pickle'])
celery_app.set_default()
celery_app.autodiscover_tasks(["api"])

@celery_app.task(name="generate_image")
def generate_image(images: List[UploadFile], orientation: OrientationType, border: int | None, color: str | None):
    saved_images_path = save_images(images)
    generated_image_namge = merge_images(saved_images_path, orientation, border, color)
    return generated_image_namge

# run celery
# celery -A api.celery.worker.celery_app worker --loglevel=info -P eventlet