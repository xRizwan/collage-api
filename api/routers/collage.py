from fastapi import UploadFile, File, status
from fastapi.responses import Response
from fastapi.routing import APIRouter
from typing import List

router = APIRouter(prefix="/collage")

@router.get("/")
def get_route():
    print("here")
    pass

@router.post("/")
def images(images: List[UploadFile] = File(...)):
    print(len(images))

    for image in images:
        try:
            with open(image.filename, 'wb') as f:
                while contents := image.file.read(1024 * 1024):
                    f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            image.file.close()
    
    return Response(status_code=status.HTTP_200_OK)