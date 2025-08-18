from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_genome():
    return {"message": "Variants endpoint works!"}
    