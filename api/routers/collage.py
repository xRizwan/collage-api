from fastapi import UploadFile, File, status, Form, WebSocket
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.routing import APIRouter
from typing import List
from celery.result import AsyncResult
from api.celery.worker import generate_image
from pydantic import BaseModel, Field
from ..helpers import OrientationType

class AsyncResultId(BaseModel):
    id: str

router = APIRouter(prefix="/collage")

@router.get("/{async_id}")
def get_route(async_id: str):
    res = AsyncResult(async_id)
    is_ready = res.ready()
    print(res)

    if is_ready:
        return JSONResponse(content={"result": "ready"}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"result": "pending"}, status_code=status.HTTP_200_OK)

@router.post("/")
def images_post(
        orientation: OrientationType | None = Form(default="vertical"),
        border: int | None = Form(default=0),
        color: str | None = Form(default="#ffffff"),
        images: List[UploadFile] = File(...),
    ):
    
    result = generate_image.apply_async(args=[images, orientation, border, color], serializer="pickle")
    print(result)

    return AsyncResultId(id=result.id)
