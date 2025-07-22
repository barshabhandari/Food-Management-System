from fastapi import APIRouter

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/")
def get_categories():
    return {"message": "List of categories"} 
