from fastapi import APIRouter, Depends
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/secure", tags=["Secure"])

@router.get("/data")
def secure_data(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, you accessed secure data!"}
