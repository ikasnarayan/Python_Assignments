from passlib.context import CryptContext

# Configure Argon2 with recommended parameters
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,   # 64 MB
    argon2__time_cost=3,         # iterations
    argon2__parallelism=2        # threads
)

def hash_password(password: str) -> str:
    """
    Hash a plain password using Argon2.
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise RuntimeError(f"Password hashing failed: {e}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its Argon2 hash.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise RuntimeError(f"Password verification failed: {e}")
