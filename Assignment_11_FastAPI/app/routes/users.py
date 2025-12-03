from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from .. import models, schemas, database
from ..utils.hashing import hash_password, verify_password
from ..auth.jwt_auth import create_access_token
from ..auth.dependencies import get_current_user
router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", tags=["Users"])
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        new_user = models.User(
            username=user.username,
            hashed_password=hash_password(user.password),
            role="user"  # default role if you want role-based claims
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        # include role in JWT payload if needed
        token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": db_user.username, "role": db_user.role},
            expires_delta=token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            # optional if you add expires_at in schemas.Token
            "expires_at": datetime.utcnow() + token_expires
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}")
