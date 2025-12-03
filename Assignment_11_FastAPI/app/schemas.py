from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    username: str
    password: constr(min_length=8, max_length=128)  # type: ignore # Argon2 supports long passphrases

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
