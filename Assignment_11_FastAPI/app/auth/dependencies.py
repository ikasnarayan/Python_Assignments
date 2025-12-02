from fastapi import Depends
from .jwt_auth import verify_token

def get_current_user(user: str = Depends(verify_token)):
    return user
