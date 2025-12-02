from pydantic import BaseModel
from typing import Optional, List

class MovieOut(BaseModel):
    id: int
    title: str
    year: int
    genre: Optional[str] = None

    class Config:
        orm_mode = True

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int

class NavigationMeta(BaseModel):
    previous_page: Optional[int]
    next_page: Optional[int]
    icons: dict

class PaginatedMoviesResponse(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int
    movies: List[MovieOut]
    navigation: NavigationMeta
