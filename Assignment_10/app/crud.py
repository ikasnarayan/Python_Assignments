from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple
from .models import Movie

def count_movies(db: Session, year: int | None = None, genre: str | None = None) -> int:
    query = db.query(func.count(Movie.id))
    if year is not None:
        query = query.filter(Movie.year == year)
    if genre is not None and genre.strip():
        query = query.filter(Movie.genre == genre.strip())
    return query.scalar() or 0

def get_movies_page(
    db: Session,
    page: int,
    page_size: int,
    year: int | None = None,
    genre: str | None = None
) -> List[Movie]:
    offset = (page - 1) * page_size
    query = db.query(Movie)
    if year is not None:
        query = query.filter(Movie.year == year)
    if genre is not None and genre.strip():
        query = query.filter(Movie.genre == genre.strip())
    return query.offset(offset).limit(page_size).all()
