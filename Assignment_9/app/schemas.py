from pydantic import BaseModel, field_validator

class MovieBase(BaseModel):
    title: str
    director: str
    year: int | None = None

    @field_validator("title", "director")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None

class MovieOut(MovieBase):
    id: int

    class Config:
        from_attributes = True
