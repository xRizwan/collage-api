from fastapi import UploadFile, File, status
from fastapi.routing import APIRouter
from typing import List
from api.celery.worker import generate_image
from pydantic import BaseModel

class AsyncResultId(BaseModel):
    id: str

router = APIRouter(prefix="/collage")

@router.get("/")
def get_route():
    print("here")
    pass

@router.post("/")
def images(images: List[UploadFile] = File(...)):
    print(len(images))
    
    result = generate_image.apply_async(args=[images], serializer="pickle")
    print(result)

    return AsyncResultId(id=result.id)