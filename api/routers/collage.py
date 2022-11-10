from fastapi.routing import APIRouter

router = APIRouter(prefix="/collage")

@router.get("/")
def get_route():
    print("here")
    pass
