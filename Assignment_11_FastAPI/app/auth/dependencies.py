from fastapi import Request, HTTPException, status, Depends
from .jwt_auth import verify_token

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return payload["sub"]
