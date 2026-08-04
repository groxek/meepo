from fastapi import APIRouter

router = APIRouter(prefix="/tasks")



@router.get("/")
def test():
    return {"message": "yo"}