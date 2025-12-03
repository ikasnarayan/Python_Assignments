from fastapi import APIRouter, Depends, HTTPException, status
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin Secure"])

@router.get("/data")
def admin_secure_data(user: str = Depends(get_current_user)):
    try:
        # Business logic for admin data
        return {"message": f"Hello {user}, you accessed secured admin data!"}
    except HTTPException:
        # Re‑raise FastAPI HTTPExceptions so they propagate correctly
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch admin data: {e}"
        )
