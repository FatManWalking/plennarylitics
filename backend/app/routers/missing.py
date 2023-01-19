from fastapi import APIRouter

router = APIRouter()

@router.get("/mps")
def get_mps():
    